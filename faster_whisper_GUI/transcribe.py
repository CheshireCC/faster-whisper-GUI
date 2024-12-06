# coding:utf-8

# from threading import Thread
from concurrent import futures
import os
from typing import List
import time
import codecs
import torch
import numpy as np 
import av
import json
import hashlib

from faster_whisper import WhisperModel
from faster_whisper.transcribe import TranscriptionInfo

import webvtt
from PySide6.QtCore import (QThread, Signal, QDateTime)
from pyaudio import (PyAudio, paInt16, paInt24)
import wave

from .config import (
                    Language_dict
                    , SUBTITLE_FORMAT
                    , Language_without_space
                )

from .seg_ment import segment_Transcribe
from .util import (
                    secondsToHMS, 
                    secondsToMS, 
                    WhisperParameters
                )

from .config import ENCODING_DICT, Task_list


class AudioStreamTranscribeWorker(QThread):
    Signal_process_over = Signal()
    def __init__(self
                , parent = None
                , model : WhisperModel = None
                , parameters : dict = None
                , vad_filter : bool = False
                , vad_parameters : dict = None
                , num_workers : int = 1
                , output_format : str = "srt"
                , output_dir : str = ""
            ) -> None:
        super().__init__(parent)

class CaptureAudioWorker(QThread):
    Signal_process_over = Signal(np.ndarray)

    def __init__(self
                , parent=None
                , rate = 48000
                , channels = 2
                , dType = 16
            ) -> None:
        
        super().__init__(parent)
        self.rate = rate
        self.channels = channels
        self.dType = dType
        self.pa = PyAudio()
        self.is_running = False
        # self.timer = QTimer()
        self.format_capture = {16:paInt16, 24:paInt24}
        self.buffer_size = 2048
    
    def run(self):
        self.is_running = True
        # print("打开输入流...")
        # print(f"format_capture : {self.format_capture[self.dType]}")
        #if self.dType == 16:
        stream = self.pa.open(format=self.format_capture[self.dType]
                            , channels=self.channels
                            , rate=self.rate
                            , input=True
                            , frames_per_buffer=self.buffer_size
                        )
        stream.start_stream()

        currentDateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd-hh-mm-ss")
        # print(currentDateTime)

        temp_path = r"./temp"
        if not os.path.exists(os.path.abspath(temp_path)):
            os.mkdir(os.path.abspath(temp_path))
        # print(f"temp path : {temp_path}")

        wav_path = os.path.join(os.path.abspath(temp_path)
                                ,f"{currentDateTime}.wav"
                            ).replace("\\", "/")
        # print(f"file: {wav_path}")

        wf = wave.open(wav_path, 'wb')  # 创建一个音频文件
        # print(f"set channels : {2}")
        wf.setnchannels(self.channels)  # 设置声道数为2
        # print(f"set sampwidth : {self.dType / 8}")
        wf.setsampwidth(int(self.dType / 8))  # 设置采样深度为
        # print(f"set rate : {self.rate}")
        wf.setframerate(self.rate)  # 设置采样率为 16000
        record_buf = []
        while self.is_running:
            ##发射信号
            # self.sinOut.emit(str(a))
            # print("===========================================================")
            # print(datetime.datetime.now())
            audio_data = stream.read(self.buffer_size)  # 读出声卡缓冲区的音频数据
            a = np.ndarray(buffer=audio_data, dtype={16:np.int16, 24:np.int32}[self.dType], shape=(self.buffer_size,))
            # print(a.shape)
            # 将数据写入创建的音频文件
            record_buf.append(audio_data)
            time.sleep(5)

        wf.writeframes("".encode().join(record_buf))
        wf.close()
        stream.stop_stream()
        stream.close()

    def stop(self):
        self.is_running = False

class OutputWorker(QThread):
    signal_write_over = Signal()

    def __init__(self, 
                    segments_path_info:list, 
                    output_dir:str, 
                    format:str, 
                    output_code = "UTF-8",
                    aggregate_contents = False,
                    parent=None
                ) -> None:
        
        super().__init__(parent)
        self.is_running = False
        self.segments_path_info = segments_path_info
        self.format = format
        self.output_dir = output_dir
        self.output_code = output_code
        self.aggregate_contents = aggregate_contents

    def stop(self):
        self.is_running = False
        # self.signal_process_over.emit()

    def run(self):
        self.is_running = True
        output_format = self.format
        output_dir = self.output_dir

        # 检查输出目录
        if output_dir != "" and not os.path.exists(output_dir):
            print(f"\nCreate output dir : {output_dir}")
            # 给定的输出目录不存在时 创建输出目录
            os.makedirs(output_dir)
        
        if self.segments_path_info is None:
            return
        
        # 后续处理
        for segments, path, info in self.segments_path_info:

            if self.output_dir == "":
                output_dir,_ = os.path.split(path)

            print("Output...")
            # 输出到字幕文件
            if output_format.lower() == "all":
                output_format_ = SUBTITLE_FORMAT
            else:
                output_format_ = [output_format]
            for format in output_format_:
                file_out = getSaveFileName( path
                                            , format=format
                                            , rootDir=output_dir
                                        )
                writeSubtitles(outputFileName=file_out
                            , segments=segments
                            , format=format
                            , language=info.language
                            , fileName=path
                            , file_code = self.output_code
                            , aggregate_contents = self.aggregate_contents
                        )

        print("\n【Over】")
        self.signal_write_over.emit()
        self.stop()

class TranscribeWorker(QThread):
    signal_process_over = Signal(list)

    def __init__(self
                ,parent=None
                ,model : WhisperModel = None
                ,parameters : WhisperParameters = None
                ,vad_filter : bool = False
                ,vad_parameters : dict = None
                ,num_workers : int = 1
            ) -> None:
        
        super().__init__(parent)

        self.is_running = False
        self.model = model
        self.parameters = parameters
        self.vad_filter = vad_filter
        self.vad_parameters = vad_parameters
        self.num_workers = num_workers

        self.segments_path_info = []
        
        
    def transcribe_file(self, file) -> (TranscriptionInfo, List): # type: ignore
        # try:
        #     is_av_file = self.try_decode_avFile(file)
        #     if not is_av_file:
        #         return (None,None)
        # except Exception as e: # 捕获异常
        #     print(f'    {file.split("/")[-1]} 不是一个有效的音视频文件\n')
        #     print(f"    error:{str(e)}")
        #     print(f"    ignore File : {file} \n")
        #     return (None, None)

        print("开始处理音频...")
        segments, info = self.model.transcribe(
                                                audio=file,
                                                language=self.parameters["language"],
                                                task=Task_list[int(self.parameters["task"])],
                                                log_progress = False,
                                                beam_size=self.parameters["beam_size"],
                                                best_of=self.parameters["best_of"],
                                                patience=self.parameters["patience"],
                                                length_penalty=self.parameters["length_penalty"],
                                                temperature=self.parameters["temperature"],
                                                compression_ratio_threshold=self.parameters["compression_ratio_threshold"],
                                                log_prob_threshold=self.parameters["log_prob_threshold"],
                                                no_speech_threshold=self.parameters["no_speech_threshold"],
                                                condition_on_previous_text=self.parameters["condition_on_previous_text"],
                                                initial_prompt=self.parameters["initial_prompt"],
                                                prefix=self.parameters["prefix"],
                                                repetition_penalty=self.parameters["repetition_penalty"],
                                                no_repeat_ngram_size=self.parameters["no_repeat_ngram_size"],
                                                prompt_reset_on_temperature = self.parameters["prompt_reset_on_temperature"],
                                                suppress_blank=self.parameters["suppress_blank"],
                                                suppress_tokens=self.parameters["suppress_tokens"],
                                                without_timestamps=self.parameters["without_timestamps"],
                                                max_initial_timestamp=self.parameters["max_initial_timestamp"],
                                                word_timestamps=self.parameters["word_timestamps"],
                                                prepend_punctuations=self.parameters["prepend_punctuations"],
                                                append_punctuations=self.parameters["append_punctuations"],
                                                multilingual = self.parameters["multilingual"],
                                                max_new_tokens=self.parameters["max_new_tokens"],
                                                chunk_length=self.parameters["chunk_length"],
                                                clip_timestamps=self.parameters["clip_timestamps"],
                                                hallucination_silence_threshold=self.parameters["hallucination_silence_threshold"],
                                                hotwords = self.parameters["hotwords"],
                                                language_detection_threshold = self.parameters["language_detection_threshold"],
                                                language_detection_segments = self.parameters["language_detection_segments"],
                                                vad_filter=self.vad_filter,
                                                vad_parameters=self.vad_parameters
                                            )
        
        try:
            self.detect_Audio_info(info)
        except Exception as e:
            print(f"{file} 处理失败!")
            print(str(e))
            return (None, None)

        # segments = list(segments)
        segmentsTranscribe : List[segment_Transcribe] = []
        # 遍历生成器，并获取转写内容
        print(f"Transcription for {file.split('/')[-1]}")

        for segment in segments:
            # 退出进程标识
            # print(self.is_running)
            if not self.is_running:
                # self.signal_process_over.emit(self.segments_path_info)
                return info, None

            print(
                    f'  [{str(round(segment.start, 5))}s --> {str(round(segment.end, 5))}s] {segment.text.lstrip()}'
                )
            segmentsTranscribe.append(segment_Transcribe(segment))#.start, segment.end, segment.text))

        # if not self.is_running:
        #     self.signal_process_over.emit()
        return info, segmentsTranscribe

    def detect_Audio_info(self, info):
        if info.language != "zh":
            language = Language_dict[info.language]
            if language:
                language = language.capitalize()
        else:
            language = "Chinese" 
        language_probability = info.language_probability
        duration = info.duration
        duration = secondsToHMS(duration).replace(",", ".")
        duration_after_vad = info.duration_after_vad
        duration_after_vad = secondsToHMS(duration_after_vad).replace(",", ".")
        print(f"  Detected language [{language}] with probability [{language_probability*100:.2f}%]")
        print(f"  Audio duration     —— [{duration}] ")
        print(f"  after VAD duration —— [{duration_after_vad}]")


    def try_decode_avFile(self, file) -> bool:
        '''
        尝试解析输入文件，并获取文件类型
        '''

        flag = False

        print("\n")
        print(f"current task: {file}")
        print("  尝试解析文件")
        container = av.open(file, metadata_errors="ignore") # 尝试打开文件      
        av_cont = container.streams
        for stream in av_cont:
            if stream.codec_context.type == "audio":
                flag = True
                break

        if not flag:
            print("  解析失败！目标文件不是有效的音视频文件")
            
        container.close()
        return flag
    
    def run(self) -> None:
        self.is_running = True

        # 检查临时目录
        if not(os.path.exists(r"./temp")):
            os.mkdir(r"./temp")

        # model = self.model 
        parameters = self.parameters
        # vad_filter = self.vad_filter 
        # vad_parameters = self.vad_parameters 
        num_workers = self.num_workers

        files = parameters["audio"]

        # 忽略掉输入文件中可能存在的所有的字幕文件
        files = [file for file in files if file.split(".")[-1].upper() not in SUBTITLE_FORMAT]
        if ingnore_files := [
            file
            for file in files
            if file.split(".")[-1].upper() in SUBTITLE_FORMAT
        ]:
            new_line = "\n              "
            print(f"ignore files: {new_line.join(ingnore_files)}")

        self.segments_path_info = []
        # 在线程池中并发执行相关任务，默认状况下使用单 GPU 该并发线程数为 1 ，
        # 提高线程数并不能明显增大吞吐量， 且可能因为线程调度的原因反而造成转写时间变长
        # 多 GPU 或多核心 CPU 可通过输入设备号列表并增大并发线程数的方式增加吞吐量，实现多任务并发处理
        # 但会造成内存或显存占用增多
        with futures.ThreadPoolExecutor(num_workers) as executor:
            results = executor.map(self.transcribe_file, files)
            new_line = "\n"

            for path, results in zip(files, results):
                # print(self.is_running)
                if not self.is_running:
                    self.signal_process_over.emit(self.segments_path_info)
                    return
                
                (info, segments) = results

                if segments is None:
                    continue

                self.segments_path_info.append((segments, path, info))
                        # print(
                        #         f"\nTranscription for {path.split('/')[-1]}:\n{new_line.join('[' + str(segment.start) + 's --> ' + str(segment.end) + 's] ' + segment.text for segment in segments)}"
                        #     )
                
                # 保存临时文件
                temp_output_save_file = getSaveFileName(audioFile=path, format="SRT", rootDir=r"./temp")
                writeSubtitles(temp_output_save_file, segments=segments, format="SRT",language=info.language, fileName=path)
                print(f"save temp file: {os.path.abspath(temp_output_save_file)}")
                
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        print("\n【Over】")
        self.signal_process_over.emit(self.segments_path_info)

        return
        
    def stop(self):
        self.is_running = False
        # self.signal_process_over.emit()

# ---------------------------------------------------------------------------------------------------------------------------

def writeSubtitles(outputFileName:str, 
                    segments:List[segment_Transcribe], 
                    format:str, 
                    language:str="",
                    fileName = "",
                    file_code = "UTF-8",
                    aggregate_contents = False
                ):
    
    file_code = ENCODING_DICT[file_code]

    if format == "SRT":
        writeSRT(outputFileName, segments, file_code = file_code)
    elif format == "TXT":
        writeTXT(outputFileName, segments, file_code=file_code, aggregate_contents = aggregate_contents)
    elif format == "VTT":
        writeVTT(outputFileName, segments,language=language, file_code=file_code)
    elif format == "LRC":
        wirteLRC(outputFileName, segments,language=language, file_code=file_code)
    elif format == "SMI":
        writeSMI(outputFileName, segments, language=language, avFile=fileName, file_code=file_code)
    elif format == "JSON":
        writeJson(outputFileName, segments, language=language, avFile=fileName, file_code=file_code)
    elif format == "ASS":
        writeASS(outputFileName, segments, file_code=file_code)

    print(f"write over | {os.path.abspath(outputFileName)}")
    
def writeJson(fileName:str, segments:List[segment_Transcribe], language:str,avFile="", file_code="utf8"):

    _id = getMd5HashId(avFile, file_code=file_code)
    
    result = {
                "id": _id,
                "title": os.path.split(avFile)[-1],
                "format": "SubRip",
                "templates": {
                                "default": "__CONTENT__",
                                "italic": "<i>__CONTENT__<\/i>"
                            },
                "styles": {
                            "default": "font-style: 10px; line-height: 1; color: #FFF;"
                            }
                }
    
    result["data"] = []
    
    for segment in segments:
        start_time_HNS = secondsToHMS(segment.start)
        end_time_HMS = secondsToHMS(segment.end)

        result["data"].append(
                                {
                                "trigger": segment.start * 1000,
                                "lang": language,
                                "styles": [
                                    "default"
                                ],
                                "templates": [
                                    "default"
                                ],
                                "start": {
                                    "time": segment.start * 1000,
                                    "hour": int(start_time_HNS.split(":")[0]),
                                    "mins": int(start_time_HNS.split(":")[1]),
                                    "secs": int(start_time_HNS.split(":")[2].split(",")[0]),
                                    "ms": int(start_time_HNS.split(":")[2].split(",")[0])
                                },
                                "end": {
                                    "time": segment.end * 1000,
                                    "hour": int(end_time_HMS.split(":")[0]),
                                    "mins": int(end_time_HMS.split(":")[1]),
                                    "secs": int(end_time_HMS.split(":")[2].split(",")[0]),
                                    "ms": int(end_time_HMS.split(":")[2].split(",")[0])
                                },
                                "duration": {
                                    "secs": round(segment.end - segment.start, 3),
                                    "ms": round(segment.end - segment.start, 3) * 1000
                                },
                                "content": segment.text,
                                "meta": {
                                    "original": {
                                        "start": start_time_HNS,
                                        "end": end_time_HMS
                                    }
                                },
                                "words":[{"start":word.start,"end":word.end,"word":word.word,"probability":word.probability }for word in segment.words],
                                "speaker":segment.speaker or "",
                            }
                        )
    with open(os.path.abspath(fileName),'w',encoding=file_code) as fp:
    
        json.dump(
                    result,
                    fp,
                    ensure_ascii=False,
                    indent=4
                )
    

def writeSMI(fileName:str, segments:List[segment_Transcribe], language:str, avFile = "",file_code="utf8"):

    subtitle_color_list = ["white", "red", "blue", "green", "yellow", "cyan", "magenta"]

    # 获取音频或视频的名称
    _, fileName_ = os.path.split(fileName)
    baseName = fileName_.split('.')[0]

    if avFile:
        # 带有扩展名的文件名
        _, fileName_ = os.path.split(avFile)
    else:
        fileName_ = ""

    # 创建字幕的样式类
    language_type_CC = f"{language.upper()}CC"

    # 创建一个空的 smi 字幕字符串
    smi = ""
    # 添加 smi 字幕的头部标签
    smi += "<SAMI>\n"
    # 添加 smi 字幕的元数据和样式信息
    smi += "<HEAD>\n"
    # 标题
    smi += f"<TITLE>{baseName}</TITLE>\n"
    # 参数
    smi += "<SAMIParam>\n"
    smi += f"  Media {'{'}{fileName_}{'}'}\n"
    smi += "  Metrics {time:ms;}\n"
    smi += "  Spec {MSFT:1.0;}\n"
    smi += "</SAMIParam>\n"
    # 样式
    smi += "<STYLE TYPE=\"text/css\">\n"
    smi += "<!--\n"
    smi += "  P { font-family: Arial; font-weight: normal; color: white; background-color: black; text-align: center; }\n"
    speakers = ["SUB"]
    for segment in segments:
        try:
            speaker = segment.speaker
        except:
            speaker = "SUB"
        if not(speaker in speakers):
            speakers.append(speaker)
    if len(speakers) > 1:
        i = 0
        for speaker in speakers:
            smi += f"  #{speaker} {'{'} color: {subtitle_color_list[i]}; {'}'}\n"
            i += 1
    else:
        smi += "  #SUB{color: white; background-color: black; font-family: Arial; font-size: 12pt; font-weight: normal; text-align: left;}"
    if language != "zh":
        smi += f"  .{language_type_CC} {'{'} name: {Language_dict[language].capitalize()}; lang: {language}; SAMIType: CC; {'}'}\n"
    else:
        smi += f"  .{language_type_CC} {'{'} name: {'Chinese'}; lang: {language}; SAMIType: CC; {'}'}\n"
    smi += "-->\n"
    smi += "</STYLE>\n"
    smi += "</HEAD>\n"
    # 添加 smi 字幕的内容和时间信息
    smi += "<BODY>\n"
    # 遍历字幕列表，每个字幕是一个字典，包含 start, end, text, words 四个键
    for segment in segments:
        try:
            speaker = segment.speaker
            if not(speaker is None):
                speaker = segment.speaker
            else:
                speaker = "SUB"
        except:
            speaker = "SUB"
        
        # 添加字幕段的开始时间标签，格式为 <SYNC Start=毫秒数>
        smi += f"<SYNC Start={segment.start * 1000}>\n"
        # 添加字幕段的文本内容标签，格式为 <P Class=样式类名>文本内容
        # 如果有单词级时间戳，则在每个单词后面添加 <SPAN Class=样式类名>标签和时间戳
        if segment.words:
            if speaker != "SUB" and not(speaker is None):
                smi += f"  <P Class={language_type_CC}>{speaker}: "
            else:
                smi += f"  <P Class={language_type_CC}>"
            for word in segment.words:
                if not(language in Language_without_space):
                    word_text = word.word + " "
                else:
                    word_text = word.word

                # word_text = word.word
                try:
                    if word.end >= segment.start and word.end <= segment.end:
                        smi += f"<{secondsToHMS(word.start).replace(',','.')}><SPAN Class={language_type_CC}>{word_text}</SPAN>"
                    else:
                        smi += f"<SPAN Class={language_type_CC}>{word_text}</SPAN>"    
                    # smi += f"<SPAN Class={language_type_CC}>{word.word}</SPAN><{secondsToHMS(word.start).replace(',','.')}>"
                    # smi += f"{word.word}<SPAN Class={language_type_CC}>{secondsToHMS(word.start).replace(',','.')}</SPAN>"
                except:
                    smi += f"<SPAN Class={language_type_CC}>{word_text}</SPAN>"
            smi += "</P>\n"
        else:
            if speaker != "SUB" and not(speaker is None):
                smi += f"<P Class={language_type_CC}>{speaker}: {segment.text}</P>\n"
            else:
                smi += f"<P Class={language_type_CC}>{segment.text}</P>\n"

        # 添加字幕段的结束时间标签，格式为 <SYNC Start=毫秒数>
        smi += f"</SYNC>\n"
    # 添加 smi 字幕的尾部标签
    smi += "</BODY>\n"
    smi += "</SAMI>\n"

    # 使用 utf-8 重新编码字幕字符串
    smi:str = smi.encode("utf8").decode("utf8")

    # 将SMI字幕写入文件
    # f = codecs.open(fileName, "w",encoding=file_code)
    with codecs.open(fileName, "w", encoding=file_code) as f:
        f.write(smi)
    
    # return smi

def wirteLRC(fileName:str, segments:List[segment_Transcribe],language:str,file_code="utf8"):
    _, baseName = os.path.split(fileName)
    baseName = baseName.split(".")[0]
    with codecs.open(fileName, "w", encoding=file_code) as f:
        f.write(f"[ti:{baseName}]\n")
        f.write(f"[re:FasterWhisperGUI]\n")
        f.write(f"[offset:0]\n\n")

        for segment in segments:
            
            start:str = secondsToMS(segment.start)
            try:
                speaker = segment.speaker + ": "
            except:
                speaker = ""

            if segment.words:
                
                text = f"[{start[:8]}]" + speaker
                length = len(segment.words)
                for i in range(length):
                    word = segment.words[i]
                    if not(language in Language_without_space):
                        word_text = word.word + " "
                    else:
                        word_text = word.word
                    try:
                        if word.start >= segment.start and word.start <= segment.end:
                            text += f"<{secondsToMS(word.start)[:8]}>{word_text}"
                        else:
                            text += f"{word_text}"
                    except:
                        text += f"{word_text}"
                text += f"<{secondsToMS(segment.end)[:8]}>"
            else:
                text:str = f"[{start[:8]}]{speaker}{segment.text}"

            # 重编码为 utf-8 
            text:str = text.encode("utf8").decode("utf8")

            f.write(f"{text} \n")

def writeVTT(fileName:str, segments:List[segment_Transcribe],language:str,file_code="utf8"):
    # 创建一个空的 VTT 字幕对象
    _, baseName = os.path.split(fileName)
    vtt = webvtt.WebVTT()
    # 遍历字幕列表，每个字幕是一个字典，包含 start, end, text, words 四个键
    for segment in segments:
        # 创建一个空的字幕段对象
        cue = webvtt.Caption()
        # 设置字幕段的开始时间和结束时间，格式为 HH:MM:SS.mmm
        cue.start = secondsToHMS(segment.start).replace(",",".")
        cue.end = secondsToHMS(segment.end).replace(",", ".")
        # 设置字幕段的文本内容，如果有单词级时间戳，则输出时间戳和单词
        text = ""
        try:
            speaker = segment.speaker + ": "
        except:
            speaker = ""

        if segment.words:
            text = speaker + text
            for i in range(len(segment.words)):
                word = segment.words[i]
                if not(language in Language_without_space):
                    word_text = word.word + " "
                else:
                    word_text = word.word

                # if i == 0:
                if i == len(segment.words) - 1:
                    text += f"{word_text}"
                else:
                    try:
                        if word.end >= segment.start and word.end <= segment.end:
                            text += f"{word_text}<{secondsToHMS(word.end).replace(',','.')}>"
                        else:
                            text += f"{word_text}"
                        # text += f"<{secondsToHMS(word.start).replace(',','.')}>{word.word}"
                    except:
                        text += f"{word_text}"
        else:
            text = speaker + segment.text
        text:str = text.encode("utf8").decode("utf8")
        cue.text = text
        # 将字幕段添加到 VTT 字幕对象中
        vtt.captions.append(cue)
        
    vtt.save(fileName, file_code)

def writeTXT(fileName:str, segments, file_code="utf8", aggregate_contents=False):
    with codecs.open(fileName, "w", encoding=file_code) as f:
        speaker_temp = ""

        for segment in segments:
            
            text:str = segment.text
            try:
                speaker = segment.speaker + ": "
            except:
                speaker = ""
            
            if speaker_temp != speaker and aggregate_contents:
                f.write(f"\n{speaker.encode('utf8').decode('utf8')} \n")
                speaker_temp = speaker
            elif not aggregate_contents:
                text = speaker + text

            # 重编码为 utf-8 
            text:str = text.encode("utf8").decode("utf8")
            f.write(f"{text} \n")

            # text = speaker + text

            

def writeSRT(fileName:str, segments, file_code="UTF-8"):
    index = 1
    # encoding = ENCODING_DICT[file_code]
    with codecs.open(fileName, "w", encoding=file_code) as f:
        for segment in segments:
            start_time:float = segment.start
            end_time:float = segment.end
            text:str = segment.text

            try:
                speaker = segment.speaker + ": "
            except:
                speaker = ""

            text = speaker + text

            # 重编码为 utf-8 
            text:str = text.encode("utf8").decode("utf8")

            start_time:str = secondsToHMS(start_time)
            end_time:str = secondsToHMS(end_time)
            f.write(f"{index}\n{start_time} --> {end_time}\n{text.lstrip()}\n\n")
            
            index += 1
    
def writeASS(fileName:str, segments, file_code="UTF-8"):
    with codecs.open(fileName, "w", encoding=file_code) as f:
        f.write("[Script Info]\n")
        f.write("; This file was generated by FasterWhisperGUI\n")
        f.write("; https://github.com/CheshireCC/faster-whisper-GUI\n")
        f.write("Original Script: FasterWhisperGUI\n")
        f.write("ScriptType: v4.00+\n")
        f.write("Collisions: Normal\n")
        f.write("PlayDepth: 0\n")
        f.write("Timer: 100.0000\n")
        f.write("WrapStyle: 0\n")

        f.write("\n[V4+ Styles]\n")
        f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write("Style: fwgDefault, Microsoft YaHei, 16, &H00FFFFFF, &H00FFFFFF, &H00000000, &H00000000, 0, 0, 0, 0, 100, 100, 0.00, 0.00, 1, 1, 0, 2, 20, 20, 20, 1\n")
        
        f.write("\n[Events]\n")
        f.write("Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n")
        for segment in segments:
            f.write(f'Dialogue: 0,{secondsToHMS(segment.start).replace(",",".")[:-1]},{secondsToHMS(segment.end).replace(",",".")[:-1]},fwgDefault,{segment.speaker},0000,0000,0000,,{segment.text}\n')


def getSaveFileName(audioFile: str, format:str = "srt", rootDir:str = ""):
    path, fileName = os.path.split(audioFile)
    fileName = fileName.split(".")

    fileName[-1] = format.lower()

    fileName = ".".join(fileName)

    if rootDir != "":
        path = rootDir

    saveFileName = os.path.join(path, fileName).replace("\\", "/")
    return saveFileName

def getMd5HashId(fileName:str, file_code) -> str:
    
    md5 = hashlib.md5()
    md5.update(fileName.encode(file_code))
    id = md5.hexdigest()
    return id

