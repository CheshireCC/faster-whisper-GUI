from threading import Thread
import time
import os

from faster_whisper import WhisperModel

from .config import Language_dict


def Transcribe(model: WhisperModel, parameters: dict, vad_filter: bool, vad_parameters: dict):

    segmenter_info = {}

    def go(result: dict):
        if vad_filter:
            result["segment"], result["info"] = model.transcribe(
                audio=parameters["audio"],
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
        else:
            result["segment"], result["info"] = model.transcribe(
                audio=parameters["audio"],
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
                vad_filter=vad_filter
            )

    print("解析文件", end="")
    thread_go = Thread(target= go, daemon=Thread, args=[segmenter_info])
    thread_go.start()

    while(thread_go.is_alive()):
        print(".", end="")
        time.sleep(0.5)
    
    
    try:
        info = segmenter_info["info"]
        print("\n")
        print(f"Detected language {Language_dict[info.language]} with probability {info.language_probability*100:.2f}%")
        # print(segmenter_info["info"])
    except:
        print("文件解析失败！")
        return
    
    print("开始转写：")
    srtFile = getSaveFileName(parameters["audio"], not(parameters["without_timestamps"]))
    index = 1
    with open(srtFile, "w") as f:
        for segment in segmenter_info["segment"]:
            start_time = segment.start
            end_time = segment.end
            text = segment.text
            print("[%.2fs -> %.2fs] %s" % (start_time, end_time, text))

            if not parameters['without_timestamps']:
                start_time = secondsToHMS(start_time)
                end_time = secondsToHMS(end_time)
                f.write(f"{index} \n {start_time} -> {end_time} \n {text} \n\n")
                
            else:
                f.write(f"{text} \n\n")
            
            index += 1
                
        print("【结束】")
    
    del segmenter_info

def getSaveFileName(audioFile: str, isSrt : bool):
    path, fileName = os.path.split(audioFile)
    fileName = fileName.split(".")
    if isSrt:
        fileName[-1] = "srt"
    else:
        fileName[-1] = "txt"

    fileName = ".".join(fileName)

    saveFileName = os.path.join(path, fileName).replace("\\", "/")

    return saveFileName


def secondsToHMS(t:str) -> str:
    try:
        t_f = float(t)
    except:
        print("time transform error")
        return
    
    H = int(t_f // 3600)
    M = int((t_f - H * 3600) // 60)
    S = (t_f - H *3600 - M *60)
    
    H = str(H)
    M = str(M)
    S = str(round(S,2))
    
    if len(H) < 2:
        H = "0" + H
    if len(M) < 2:
        M = "0" + M
    
    return H + ":" + M + ":" + S





