from resource import rc_Image

from qfluentwidgets import (FluentIconBase, Theme, getIconColor)

from enum import Enum



class FasterWhisperGUIIcon(FluentIconBase, Enum):
    VAD_PAGE = "wave-16x16"
    TRANSCRIPTION_PAGE = "robot-16x16"
    PROCESS = "speak"
    HEAD_PHONE= "headphone"
    DEMUCS = "Demucs"

    def png(self, theme=Theme.AUTO):
        return f':/resource/Image/{self.value}_{getIconColor(theme)}.png'

    def path(self, theme=Theme.AUTO):
        return f':/resource/Image/{self.value}_{getIconColor(theme)}.svg'
    
