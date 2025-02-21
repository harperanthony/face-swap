import sys
import platform
import shutil
import argparse
import torch
import tensorflow

import modules.globals
# import modules.swap as swap
import modules.server as swap
from modules.utilities import (
    resolve_relative_path,
    conditional_download
)

def parse_args() -> None:
    program = argparse.ArgumentParser()
    program.add_argument('--video-quality', help='adjust output video quality', dest='video_quality', type=int, default=10, choices=range(52), metavar='[0-51]')
    program.add_argument('--max-memory', help='maximum amount of RAM in GB', dest='max_memory', type=int, default=4)
    program.add_argument('--execution-threads', help='number of execution threads', dest='execution_threads', type=int, default=768)

    args = program.parse_args()

    modules.globals.video_quality = args.video_quality
    modules.globals.max_memory = args.max_memory
    modules.globals.execution_threads = args.execution_threads

def limit_resources() -> None:
    # prevent tensorflow memory leak
    gpus = tensorflow.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tensorflow.config.experimental.set_memory_growth(gpu, True)
    # limit memory usage
    if modules.globals.max_memory:
        memory = modules.globals.max_memory * 1024 ** 3
        if platform.system().lower() == 'windows':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetProcessWorkingSetSize(-1, ctypes.c_size_t(memory), ctypes.c_size_t(memory))
        else:
            import resource
            resource.setrlimit(resource.RLIMIT_DATA, (memory, memory))


def release_resources() -> None:
    if modules.globals.execution_provider == 'CUDAExecutionProvider':
        torch.cuda.empty_cache()


def pre_check() -> bool:
    # Check Python version
    if sys.version_info < (3, 9):
        update_status('Python version is not supported - please upgrade to 3.9 or higher.')
        return False
    
    # Check if ffmpeg is installed
    if not shutil.which('ffmpeg'):
        update_status('ffmpeg is not installed.')
        return False
    
    # Example of downloading a file (replace with actual logic)
    download_directory_path = resolve_relative_path("../")
    conditional_download(
        download_directory_path,
        [
            "https://huggingface.co/hacksider/deep-live-cam/resolve/main/inswapper_128_fp16.onnx?download=true"
        ],
    )
    
    return True


def update_status(message: str, scope: str = 'DLC.CORE') -> None:
    print(f'[{scope}] {message}')

def run() -> None:
    parse_args()
    if not pre_check():
        return
    limit_resources()
    swap.start()
