from PySide6.QtCore import QTranslator
from resource import rc_Translater
import locale

import json

try:
    config_json = json.load(open("./fasterWhisperGUIConfig.json", "r", encoding="utf-8"))
    language_config = config_json["setting"]["language"]
except:
    language_config = 2

if language_config == 0:
    language = "zh"
elif language_config == 1:
    language = "en"
else:
    # 获取当前计算机语言
    language_localtion, _ = locale.getdefaultlocale()
    language = language_localtion.split("_")[0]
    print(f"current computer language region-format: {language_localtion}")

print(f"language: {language}")

def __translator() -> QTranslator:
    translator = QTranslator()
    if language != "zh" :  
        try:
            translator.load(":/resource/Translater/en.qm")
            # splash.showMessage("set Language: English") #, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, Qt.white)
        except Exception as e:
            print(f"load translator files error: {str(e)}")
            translator.load("")
    else:
        translator.load("")

    return translator

TRANSLATOR = __translator()
