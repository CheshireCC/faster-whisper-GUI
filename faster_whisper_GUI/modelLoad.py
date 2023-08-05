# coding:utf-8

import time
import os
from threading import Thread
from typing import (List, Optional, Union)

from faster_whisper import WhisperModel

def loadModel(model_size_or_path: str,
        device: str = "auto",
        device_index: Union[int, List[int]] = 0,
        compute_type: str = "default",
        cpu_threads: int = 0,
        num_workers: int = 1,
        download_root: Optional[str] = None,
        local_files_only: bool = False,):
    
    if os.path.isdir(model_size_or_path):
        print("Load local model", end="")
    
    else:
        print("download online model")
    
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
            print(".", end="", flush=True)
            time.sleep(0.5)         
        else:
            pass       
    

    try:
        model = model_dict["model"]

        print("\nLoad over")
        print(model_size_or_path)
        print(f"{'max_length: ':23}",model.max_length)
        print(f"{'num_samples_per_token: ':23}", model.num_samples_per_token)
        print("time_precision: ", model.time_precision)
        print("tokens_per_second: ", model.tokens_per_second)
        print("input_stride: ", model.input_stride)

        
    except:
        print("Failed to load model")
        return None
    
    return model