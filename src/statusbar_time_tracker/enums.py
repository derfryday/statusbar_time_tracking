from enum import Enum


class WorkState(str, Enum):
    work = "working"
    pause = "pause"
    error = "ERROR"
