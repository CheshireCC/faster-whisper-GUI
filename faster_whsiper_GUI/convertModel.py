
from ctranslate2.converters import TransformersConverter as cvter
import os 
from .config import Model_names
import time
from threading import Thread

def ConvertModel(model_name_or_path:str,cache_dir: str, output_dir:str, quantization:str, use_local_file : bool = True):

    model_name_or_path = "base"

    if (not os.path.isdir(model_name_or_path)) and use_local_file :
        model_path = os.path.join(cache_dir, "models--openai--whisper-" + model_name_or_path, "snapshots").replace("\\","/")
        if os.path.exists(model_path):
            # print(model_path)
            model_path_hash = os.listdir(model_path)[0]

            # print(model_path_hash)
            model_path = os.path.join(model_path, model_path_hash).replace("\\", "/")

            # print(model_path)
            # print(os.listdir(model_path))

            model_name_or_path = model_path
            
        else:
            if not (model_name_or_path in Model_names):
                print(f"{model_name_or_path} 不是有效的模型名称！")
                return
    else:
        if not (model_name_or_path in Model_names):
            print(f"{model_name_or_path} 不是有效的模型名称！")
            return

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
    
    Thread_go = Thread(target=go_2, daemon=True)
    Thread_go.start()

    while(Thread_go.is_alive()):
        print(".", end="", flush=True)
        time.sleep(0.5)

    print("\n处理结束")

