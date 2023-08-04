'''
Author: CheshireCC 
Date: 2023-07-18 22:27:35
LastEditors: CheshireCC 36411617+CheshireCC@users.noreply.github.com
LastEditTime: 2023-08-05 00:40:36
FilePath: \fatser_whsiper_GUI\faster_whsiper_GUI\FasterWhisperGUI.py
Description: main program 
'''

import os
import sys
import locale


# 修复程序路径依赖
BASE_DIR = os.path.dirname(os.path.abspath( __file__))
sys.path.append(os.path.join(BASE_DIR, 'resource'))
sys.path.append(os.path.join(BASE_DIR, 'faster_whisper_GUI'))

# from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator


from faster_whisper_GUI.UI_MainWindows import mainWin
from resource import rc_Translater


# 主程序入口
if __name__ == "__main__":

    # 启动一个Qt程序，并使用传入的系统参数
    app = QApplication(sys.argv)

    # 获取当前计算机语言
    language, _ = locale.getdefaultlocale()

    # print(language)
    # 非中文时加载语言翻译文件，进行国际化
    if language != "zh_CN":
        translator = QTranslator(app)
        if translator.load(":/resource/Translater/en.qm"):
            app.installTranslator(translator)
    
    # 实例化窗体
    mainWindows = mainWin()

    # 显示窗体
    mainWindows.show()

    # 退出程序，并使用app实例的退出代码
    sys.exit(app.exec())


