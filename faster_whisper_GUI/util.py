import datetime

def outputWithDateTime(text:str):
    dateTime_ = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    print(f"\n=========={dateTime_}==========")
    print(f"=========={text}==========\n")