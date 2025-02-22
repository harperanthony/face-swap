from typing import Any
import insightface
import threading
import modules.globals
from modules.face_analyser import get_one_face
from modules.typing import Frame
from modules.utilities import (
    resolve_relative_path,
)

FACE_SWAPPER = None
THREAD_LOCK = threading.Lock()
NAME = "DLC.FACE-SWAPPER"

def get_face_swapper() -> Any:
    global FACE_SWAPPER

    with THREAD_LOCK:
        if FACE_SWAPPER is None:
            model_path = resolve_relative_path("../inswapper_128_fp16.onnx")
            FACE_SWAPPER = insightface.model_zoo.get_model(
                model_path, providers=modules.globals.execution_provider
            )
    return FACE_SWAPPER


def swap_face(source_face, target_face, temp_frame: Frame) -> Frame:
    face_swapper = get_face_swapper()

    # Apply the face swap
    swapped_frame = face_swapper.get(
        temp_frame, target_face, source_face, paste_back=True
    )

    return swapped_frame


def process_frame(source_face, temp_frame: Frame) -> Frame:
    target_face = get_one_face(temp_frame)
    if target_face:
        temp_frame = swap_face(source_face, target_face, temp_frame)
    return temp_frame