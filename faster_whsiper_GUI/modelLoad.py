'''
Author: CheshireCC 
Date: 2023-07-19 22:55:25
LastEditors: CheshireCC 
LastEditTime: 2023-07-20 23:29:08
FilePath: \fatser_whsiper_GUI\faster_whsiper_GUI\modelLoad.py
Description: 
'''

from typing import List, Optional, Union
from faster_whisper import WhisperModel
import faster_whisper
import time
import os
from threading import Thread

def loadModel(model_size_or_path: str,
        device: str = "auto",
        device_index: Union[int, List[int]] = 0,
        compute_type: str = "default",
        cpu_threads: int = 0,
        num_workers: int = 1,
        download_root: Optional[str] = None,
        local_files_only: bool = False,):
    
    if os.path.isdir(model_size_or_path):
        print("加载本地模型", end="")
    
    else:
        print("下载网络模型")
    
    model_dict = {}
    def go(model : dict):
        model_ = WhisperModel(model_size_or_path, 
                            device=device, 
                            device_index=device_index,
                            compute_type=compute_type,
                            cpu_threads=cpu_threads,
                            num_workers=num_workers,
                            download_root=download_root,
                            local_files_only=local_files_only)
        model["model"] = model_

    Thread_go = Thread(target=go, daemon=True, args=[model_dict])
    Thread_go.start()

    while(Thread_go.is_alive()):
        if os.path.isdir(model_size_or_path):
            for i in range(6):
                print(".", end="", flush=True)
                time.sleep(0.2)         
        else:
            pass       
    

    try:
        model = model_dict["model"]

        print("\n模型加载完成")
        print(model_size_or_path)
        print("max_length: ",model.max_length)
        print("num_samples_per_token: ", model.num_samples_per_token)
        print("time_precision: ", model.time_precision)
        print("tokens_per_second: ", model.tokens_per_second)
        print("input_stride: ", model.input_stride)
        
    except:
        print("加载失败！")
        return None
    
    return model