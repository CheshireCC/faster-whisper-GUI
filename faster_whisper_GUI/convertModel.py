'''
Author: CheshireCC 
Date: 2023-07-20 20:15:57
LastEditors: CheshireCC 
LastEditTime: 2023-07-29 22:14:05
FilePath: \fatser_whsiper_GUI\faster_whsiper_GUI\convertModel.py
Description: 转换文件
'''

import os 
import time
from threading import Thread

from ctranslate2.converters import TransformersConverter as cvter

from .config import Model_names


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

            print(f"使用本地文件已开启，找到适用的本地缓存 {model_name_or_path}")
            
        else:
            if not (model_name_or_path in Model_names):
                print(f"{model_name_or_path} 不是有效的模型名称！")
                return
            else:
                model_name_or_path = "openai/whisper-" + model_name_or_path
                print(f"未找到有效本地缓存，将下载 {model_name_or_path} 模型")
    else:
        if not (model_name_or_path in Model_names):
            print(f"{model_name_or_path} 不是有效的模型名称！")
            return
        else:
            model_name_or_path = "openai/whisper-" + model_name_or_path
            print(f"下载模型 : {model_name_or_path} ")

    print(f"目标模型 : {model_name_or_path}")
    print("初始化转换器", end="")
    
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
        print("\n初始化完成！")
    except:
        print("\n初始化失败！")
        return
    
    print("开始转换",end="")

    def go_2():
        cvter_01.convert(output_dir=output_dir, quantization=quantization, force=True)
    
    Thread_go_2 = Thread(target=go_2, daemon=True)
    Thread_go_2.start()

    while(Thread_go_2.is_alive()):
        print(".", end="", flush=True)
        time.sleep(0.5)

    print("\n处理结束")

    
