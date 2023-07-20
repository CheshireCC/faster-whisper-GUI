'''
Author: CheshireCC 36411617+CheshireCC@users.noreply.github.com
Date: 2023-07-19 22:55:25
LastEditors: CheshireCC 36411617+CheshireCC@users.noreply.github.com
LastEditTime: 2023-07-20 13:34:12
FilePath: \fatser_whsiper_GUI\faster_whsiper_GUI\modelLoad.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from typing import List, Optional, Union
from faster_whisper import WhisperModel
import faster_whisper
import os


def loadModel(model_size_or_path: str,
        device: str = "auto",
        device_index: Union[int, List[int]] = 0,
        compute_type: str = "default",
        cpu_threads: int = 0,
        num_workers: int = 1,
        download_root: Optional[str] = None,
        local_files_only: bool = False,):
    
    if os.path.isdir(model_size_or_path):
        print("加载本地模型...")
    
    else:
        print("下载网络模型...")

    model = WhisperModel(model_size_or_path, 
                            device=device, 
                            device_index=device_index,
                            compute_type=compute_type,
                            cpu_threads=cpu_threads,
                            num_workers=num_workers,
                            download_root=download_root,
                            local_files_only=local_files_only)
    
    print("模型加载完成")
    print(model_size_or_path)
    print("max_length: ",model.max_length)
    print("num_samples_per_token: ", model.num_samples_per_token)
    print("time_precision: ", model.time_precision)
    print("tokens_per_second: ", model.tokens_per_second)
    print("input_stride: ", model.input_stride)
    
    return model