# coding: utf-8
from enum import Enum

from qfluentwidgets import (
                            StyleSheetBase
                            , Theme
                            , qconfig
                        )

from resource import rc_qss

class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    MAIN_WINDOWS = "mainWindows"
    NAVIGATION_INTERFACE = "navigationBaseInterface"
    TAB_INTERFSCE = "tabInterface"
    FILE_LIST = "fileListWidget"
    HOME_ITEM = "homeItemLabel"
    DENUCE_INTERFACE = "demucsInterface"
    OUTPUT_GROUP_WIDGET = "outputGroupWidget"


    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/resource/qss/{self.value}_{theme.value.lower()}.qss"

