# coding:utf-8

import datetime

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
        S[1] = "0" + S[1]
    if len(S[1]) >= 3:
        S[1] = S[1][:2]

    S:str = ".".join(S)

    return M + ":" + S


