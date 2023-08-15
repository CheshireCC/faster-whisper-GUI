# coding:utf-8

# from threading import Thread
from concurrent import futures
import os
from typing import List
import av

from faster_whisper import WhisperModel, Segment
import webvtt

from .config import Language_dict, SUbTITLE_FORMAT

class segment_Transcribe():
    def __init__(self, start:float = 0, end: float = 0, text:str = "", words : list = None):
        self.start = start
        self.end = end
        self.text = text
        self.words = words
    
    def __init__(self, segment: Segment):
        self.start = segment.start
        self.end = segment.end
        self.text = segment.text
        try:
            self.words = segment.words
        except:
            self.words = None


def Transcribe(model: WhisperModel, 
               parameters: dict, 
               vad_filter: bool, 
               vad_parameters: dict, 
               num_worker:int = 1, 
               output_format: str = "srt", 
               output_dir:dir = ""):
    '''
        parameters: dict, parameters of fasterWhisper 
        vad_filter: bool, if true, use VAD model
        vad_parameters: dict, parameters of VAD model
        num_worker:int = 1, 
        output_format: str = "srt", 
        output_dir:dir = ""
    '''

    # 检查输出目录
    if os.path.exists(output_dir):
        pass
    else:
        os.mkdir(output_dir)
        print(f"\nCreate output dir : {output_dir}")

    files = parameters["audio"]
    
    # 忽略掉输入文件中可能存在的所有的字幕文件
    files = [file for file in files if file.split(".")[-1].upper() not in SUbTITLE_FORMAT]
    ingnore_files = [file for file in files if file.split(".")[-1].upper() in SUbTITLE_FORMAT]
    
    # print
    if len(ingnore_files) != 0:
        new_line = "\n              "
        print(f"ignore files: {new_line.join(ingnore_files)}")
    
    
    def transcribe_file(file):
        print("\n\n")
        print(f"current task: {file}")
        print("  尝试解析文件")
        try:
                container = av.open(file) # 尝试打开文件      
                print("  解析成功！")
                container.close()
        except av.AVError as e: # 捕获异常
                print(f'    {file.split("/")[-1]} 不是一个有效的音视频文件\n    错误信息：{e}')
                print(f"    ignore File : {file} \n")
                return None
        
        segments, info = model.transcribe(
                                        audio=file,
                                        language=parameters["language"],
                                        task=parameters["task"],
                                        beam_size=parameters["beam_size"],
                                        best_of=parameters["best_of"],
                                        patience=parameters["patience"],
                                        length_penalty=parameters["length_penalty"],
                                        temperature=parameters["temperature"],
                                        compression_ratio_threshold=parameters["compression_ratio_threshold"],
                                        log_prob_threshold=parameters["log_prob_threshold"],
                                        no_speech_threshold=parameters["no_speech_threshold"],
                                        condition_on_previous_text=parameters["condition_on_previous_text"],
                                        initial_prompt=parameters["initial_prompt"],
                                        prefix=parameters["prefix"],
                                        suppress_blank=parameters["suppress_blank"],
                                        suppress_tokens=parameters["suppress_tokens"],
                                        without_timestamps=parameters["without_timestamps"],
                                        max_initial_timestamp=parameters["max_initial_timestamp"],
                                        word_timestamps=parameters["word_timestamps"],
                                        prepend_punctuations=parameters["prepend_punctuations"],
                                        append_punctuations=parameters["append_punctuations"],
                                        vad_filter=vad_filter,
                                        vad_parameters=vad_parameters
                                    )
        try:
            print(f"Detected language {Language_dict[info.language]} with probability {info.language_probability*100:.2f}%")
        
        except:
            print(f"{file} 处理失败!")
            return
        
        # segments = list(segments)
        segmentsTranscribe : List[segment_Transcribe] = []
        # 遍历生成器，并获取转写内容
        print(f"Transcription for {file.split('/')[-1]}")
        for segment in segments:
            print('  [' + str(round(segment.start),5) + 's --> ' + str(round(segment.end, 5)) + 's] ' + segment.text.lstrip())
            segmentsTranscribe.append(segment_Transcribe(segment))#.start, segment.end, segment.text))

        return info, segmentsTranscribe

    # 在线程池中并发执行相关任务，默认状况下使用单 GPU 该并发线程数为 1 ，
    # 提高线程数并不能明显增大吞吐量， 且可能因为线程调度的原因反而造成转写时间变长
    # 多 GPU 或多核心 CPU 可通过输入设备号列表并增大并发线程数的方式增加吞吐量，实现多任务并发处理
    # 但会造成内存或显存占用增多
    with futures.ThreadPoolExecutor(num_worker) as executor:
        results = executor.map(transcribe_file, files)
        new_line = "\n"
        for path, results in zip(files, results):
            (info, segments) = results
            if segments == None:
                continue

            # print(
            #         f"\nTranscription for {path.split('/')[-1]}:\n{new_line.join('[' + str(segment.start) + 's --> ' + str(segment.end) + 's] ' + segment.text for segment in segments)}"
            #     )
            
            print("Output...")

            if output_format == "All" and not(parameters["without_timestamps"]):
                for format in SUbTITLE_FORMAT:
                    file_out = getSaveFileName( path
                                                , not(parameters["without_timestamps"])
                                                , format=format
                                                , rootDir=output_dir
                                            )
                    writeSubtitles(file_out
                                    ,segments=segments
                                    , format=format
                                    , language=info.language
                                )
            else:
                file_out = getSaveFileName( path
                                            , not(parameters["without_timestamps"])
                                            , format=output_format
                                            , rootDir=output_dir
                                        )
                writeSubtitles(file_out
                                , segments=segments
                                , format=output_format
                                , language=info.language
                            )
            segments = None
            
    print("\n【Over】")

def writeSubtitles(fileName:str, segments:List[segment_Transcribe], format:str, language:str=""):
    
    if format == "SRT":
        writeSRT(fileName, segments)
    elif format == "TXT":
        writeTXT(fileName, segments)
    elif format == "VTT":
        writeVTT(fileName, segments)
    elif format == "LRC":
        wirteLRC(fileName, segments)
    elif format == "SMI":
        writeSMI(fileName, segments, language=language)

    
    print(f"write over | {fileName}")

def writeSMI(fileName:str, segments:List[segment_Transcribe], language:str):

    # 获取音频或视频的名称
    _, baseName = os.path.split(fileName)
    baseName = baseName.split('.')[0]
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
    # 样式
    smi += "<STYLE TYPE=\"text/css\">\n"
    smi += "<!--\n"
    smi += "P { font-family: Arial; font-weight: normal; color: white; background-color: black; text-align: center; }\n"
    smi += f"#{language_type_CC} {'{'} name: {Language_dict[language]}; lang: {language}; SAMIType: CC; {'}'}\n"
    smi += "-->\n"
    smi += "</STYLE>\n"
    smi += "</HEAD>\n"
    # 添加 smi 字幕的内容和时间信息
    smi += "<BODY>\n"
    # 遍历字幕列表，每个字幕是一个字典，包含 start, end, text, words 四个键
    for segment in segments:
        # 添加字幕段的开始时间标签，格式为 <SYNC Start=毫秒数>
        smi += f"<SYNC Start={segment.start * 1000}><P Class={language_type_CC}>\n"
        # 添加字幕段的文本内容标签，格式为 <P Class=样式类名>文本内容
        # 如果有单词级时间戳，则在每个单词后面添加 <SPAN Class=样式类名>标签和时间戳
        if segment.words:
            smi += f"<P Class={language_type_CC}>"
            for word in segment.words:
                smi += f"<SPAN Class={language_type_CC}>{word.word}</SPAN><{secondsToHMS(word.end).replace(',','.')}>"
                # smi += f"<SPAN Class={language_type_CC}>{word.word}</SPAN><{secondsToHMS(word.start).replace(',','.')}>"
                #smi += f"{word.word}<SPAN Class={language_type_CC}>{secondsToHMS(word.start).replace(',','.')}</SPAN>"
            smi += "\n"
        else:
            smi += f"<P Class={language_type_CC}>{segment.text}\n"
        # 添加字幕段的结束时间标签，格式为 <SYNC Start=毫秒数>
        smi += f"<SYNC Start={segment.end * 1000}><P Class={language_type_CC}> \n"
    # 添加 smi 字幕的尾部标签
    smi += "</BODY>\n"
    smi += "</SAMI>\n"

    # 使用 utf-8 重新编码字幕字符串
    smi:str = smi.encode("utf8").decode("utf8")
    # 将SMI字幕写入文件
    with open(fileName, "w", encoding="utf-8") as f:
        f.write(smi)
    # return smi


def wirteLRC(fileName:str, segments:List[segment_Transcribe]):
    _, baseName = os.path.split(fileName)
    baseName = baseName.split(".")[0]
    with open(fileName, "w", encoding="utf8") as f:
        f.write(f"[ti:{baseName}]\n")
        f.write(f"[re:FasterWhisperGUI]\n")
        f.write(f"[offset:0]\n\n")

        for segment in segments:
            
            start:str = secondsToMS(segment.start)
            
            if segment.words:
                text = f"[{secondsToMS(segment.start)}]"
                length = len(segment.words)
                for i in range(0, length):
                    word = segment.words[i]
                    text += f"<{secondsToMS(word.start)}>{word.word}"
                text += f"<{secondsToMS(segment.end)}>"
            else:
                text:str = f"[{secondsToMS(segment.start)}]{segment.text}"

            # 重编码为 utf-8 
            text:str = text.encode("utf8").decode("utf8")

            f.write(f"{text} \n")

def writeVTT(fileName:str, segments:List[segment_Transcribe]):
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
        if segment.words:
            text = ""
            for i in range(0, len(segment.words)):
                word = segment.words[i]

                # if i == 0:
                if i == len(segment.words) - 1:
                    text += f"{word.word}"
                else:
                    text += f"{word.word}<{secondsToHMS(word.end).replace(',','.')}>"
                    # text += f"<{secondsToHMS(word.start).replace(',','.')}>{word.word}"
        else:
            text = segment.text
        text:str = text.encode("utf8").decode("utf8")
        cue.text = text
        # 将字幕段添加到 VTT 字幕对象中
        vtt.captions.append(cue)
    
    vtt.save(fileName)


def writeTXT(fileName:str, segments):
    with open(fileName, "w", encoding="utf8") as f:
        for segment in segments:
            
            text:str = segment.text
            # 重编码为 utf-8 
            text:str = text.encode("utf8").decode("utf8")

            f.write(f"{text} \n\n")


def writeSRT(fileName:str, segments):
    index = 1
    with open(fileName, "w", encoding="utf8") as f:
        for segment in segments:
            start_time:float = segment.start
            end_time:float = segment.end
            text:str = segment.text
            # 重编码为 utf-8 
            text:str = text.encode("utf8").decode("utf8")

            start_time:str = secondsToHMS(start_time)
            end_time:str = secondsToHMS(end_time)
            f.write(f"{index}\n{start_time} --> {end_time}\n{text.lstrip()}\n\n")
            
            index += 1

def getSaveFileName(audioFile: str, isSrt : bool, format:str = "srt", rootDir:str = ""):
    path, fileName = os.path.split(audioFile)
    fileName = fileName.split(".")

    fileName[-1] = format.lower()
    if isSrt:
        pass
    else:
        fileName[-1] = "txt"

    fileName = ".".join(fileName)

    if rootDir != "":
        path = rootDir

    saveFileName = os.path.join(path, fileName).replace("\\", "/")
    return saveFileName


def secondsToHMS(t) -> str:
    try:
        t_f:float = float(t)
    except:
        print("time transform error")
        return
    
    H = int(t_f // 3600)
    M = int((t_f - H * 3600) // 60)
    S = (t_f - H *3600 - M *60)
    
    
    H = str(H)
    M = str(M)
    S = str(round(S,4))
    S = S.replace(".", ",")
    S = S.split(",")
    
    if len(S) < 2 :
        S.append("000")
    
    if len(S[0]) < 2:
        S[0] = "0" + S[0]
    
    while(len(S[1]) < 3):
        S[1] = S[1] + "0"
    
    S = ",".join(S)
    
    if len(H) < 2:
        H = "0" + H
    if len(M) < 2:
        M = "0" + M
    
    return H + ":" + M + ":" + S

def secondsToMS(t) -> str:
    try:
        t_f:float = float(t)
    except:
        print("time transform error")
        return
    
    M = t_f // 60
    S = t_f - M * 60

    M = str(int(M))
    if len(M)<2:
        M = "0" + M

    S = str(round(S,4))
    S = S.split(".")

    if len(S) < 2:
        S.append("00")
    
    if len(S[0]) < 2:
        S[0] = "0" + S[0]
    if len(S[1] ) < 2:
        S[1] = "0" + S[1]

    S:str = ".".join(S)

    return M + ":" + S





