# coding:utf-8

import os 
import time
from threading import Thread

from ctranslate2.converters import TransformersConverter as cvter

from PySide6.QtCore import QCoreApplication

from .config import Model_names

def __tr(text:str) -> str:
    return QCoreApplication.translate("ConvertModel", text)

def ConvertModel(model_name_or_path:str,cache_dir: str, output_dir:str, quantization:str, use_local_file : bool = True):

    # model_name_or_path = "base"

    # 处理模型文件名称或者路径为合适路径
    if (not os.path.isdir(model_name_or_path)) and use_local_file :
        model_path = os.path.join(cache_dir, "models--openai--whisper-" + model_name_or_path.replace(".","-"), "snapshots").replace("\\","/")
        if os.path.exists(model_path):
            # print(model_path)
            model_path_hash = os.listdir(model_path)[0]

            # print(model_path_hash)
            model_path = os.path.join(model_path, model_path_hash).replace("\\", "/")

            # print(model_path)
            # print(os.listdir(model_path))
            if os.path.exists(model_path):
                model_name_or_path = model_path

            print(__tr('Use local file is True, found applicable local cache:'))
            print(f"  {model_name_or_path}")
            
        else:
            if not (model_name_or_path in Model_names):
                print(__tr('Not a valid model name:'))
                print(f"  {model_name_or_path}")
                return
            else:
                model_name_or_path = "openai/whisper-" + model_name_or_path
                print(__tr('No valid local cache was found and will download:'))
                print(f"  {model_name_or_path}")
    else:
        if not (model_name_or_path in Model_names):
            print(__tr('Not a valid model name:'))
            print(f"  {model_name_or_path}")

            return
        else:
            model_name_or_path = "openai/whisper-" + model_name_or_path
            print(__tr('Download model: '))
            print(f"  {model_name_or_path} ")

    print(__tr('target model: '))
    print(f"  {model_name_or_path}")
    print(__tr("Initializing"), end="")
    
    cvter_01 = {}
    def go(cvter_ : dict):
        cvter_1 = cvter(model_name_or_path=model_name_or_path, 
                            copy_files=["tokenizer.json"])
        cvter_["result"] = cvter_1

    Thread_go = Thread(target=go, daemon=True, args=[cvter_01])
    Thread_go.start()

    while(Thread_go.is_alive()):
        if os.path.isdir(model_name_or_path):
            print(".", end="", flush=True)
            time.sleep(0.5)
        else:
            pass
    try:
        cvter_01 = cvter_01["result"]
        print(__tr("\nInitialization complete!"))
    except:
        print(__tr("\nFailed to complete initialization!"))
        return
    
    print(__tr("Convert"),end="")

    def go_2():
        cvter_01.convert(output_dir=output_dir, quantization=quantization, force=True)
    
    Thread_go_2 = Thread(target=go_2, daemon=True)
    Thread_go_2.start()

    while(Thread_go_2.is_alive()):
        print(".", end="", flush=True)
        time.sleep(0.5)

    print(__tr("\nOver"))

    
