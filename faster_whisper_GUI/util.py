# coding:utf-8

import datetime

from typing import List, TypedDict, Union

class WhisperParameters(TypedDict):
    language:str = ""
    task:str = "transcribe"
    beam_size:int = 5
    best_of:int = 5
    patience:float = 0.0
    length_penalty:float = 1.0
    temperature:list = [0.0]
    compression_ratio_threshold:float = 1.0
    log_prob_threshold:float = -1.0
    no_speech_threshold:float = 0.6
    condition_on_previous_text:str = ""
    initial_prompt:list = []
    prefix:str = ""
    repetition_penalty:bool = False
    no_repeat_ngram_size:int = 0
    prompt_reset_on_temperature:float = 0.5
    suppress_blank:bool = True
    suppress_tokens:list = []
    without_timestamps:bool = False
    max_initial_timestamp:float = 0.0
    word_timestamps:bool = False
    prepend_punctuations:str = ""
    append_punctuations: str = ""
    max_new_tokens:int = None
    chunk_length:int = None
    clip_mode:int = 0
    clip_timestamps:Union[str, List[float]] = "0"
    hallucination_silence_threshold:float = None
    hotwords: str = None
    language_detection_threshold:float = None
    language_detection_segments:int = 2

def outputWithDateTime(text:str):
    dateTime_ = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    print(f"\n=========={dateTime_}==========")
    print(f"=========={text}==========\n")

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
    
    # 当只有整数秒数值的时候
    if len(S) < 2 :
        S.append("000")
    
    # 当整数位秒数值不够两位时，向前填充0
    S[0] = S[0].zfill(2)
    
    # 当小数位秒数值不够三位时，向后填充0
    S[1] = S[1].ljust(3, "0")
    
    S = ",".join(S)
    
    # H 与 M 至少有两位
    H = H.zfill(2)
    M = M.zfill(2)
    
    return H + ":" + M + ":" + S

# ---------------------------------------------------------------------------------------------------------------------------
def HMSToSeconds(t:str) -> float:

    hh,mm,ss = t.split(":")
    ss = ss.replace(",",".")

    return float(hh) * 3600 + float(mm) * 60 + float(ss)


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
        S[1] =   S[1] + "0"
    if len(S[1]) >= 3:
        S[1] = S[1][:2]

    S:str = ".".join(S)

    return M + ":" + S

def MSToSeconds(t:str) -> float:
    
    mm,ss = t.split(":")
    ss = ss.replace(",",".")

    return float(mm) * 60 + float(ss)
