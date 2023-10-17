from typing import List
from .seg_ment import segment_Transcribe

def readSRTFileToSegments(file:str) -> List[segment_Transcribe]:

    segments = []

    with open(file, "r", encoding="utf8") as f:
        timesStample = None
        content = None

        str_content = "a"
        while(str_content):
            for i in range(4):
                str_content = f.readline()
                
                if i == 1:
                    timesStample = str_content.split("-->")
                elif i == 2:
                    content = str_content.strip()
                elif i == 3:
                    # 避免异常退出 导致内容不完整
                    str_content = " "

                if not str_content:
                    return segments

            # 假设获取 speaker
            content_ = content.split(":")
            speaker = None

            if len(content_) > 1:
                speaker = content_[0]
                content = ":".join(content_[1:])

            else:
                content = content_[0]

            # 创建 segment_Transcribe 对象
            segment = segment_Transcribe(
                                start=HMSToSeconds(timesStample[0]), 
                                end=HMSToSeconds(timesStample[1]), 
                                text=content,
                                words=[],
                                speaker=speaker
                            )
            
            # 向列表中添加对象
            segments.append(segment)

    return segments
    

def HMSToSeconds(HMS:str) -> float:
    # print(HMS)
    H,M,S = HMS.split(":")
    return round(int(H.strip()) * 60 * 60 + int(M.strip()) * 60 + float(S.strip().replace(",",".")),2)
