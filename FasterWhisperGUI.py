'''
Author: CheshireCC 
Date: 2023-07-18 22:27:35
LastEditors: CheshireCC 36411617+CheshireCC@users.noreply.github.com
LastEditTime: 2023-07-25 18:52:01
FilePath: \fatser_whsiper_GUI\faster_whsiper_GUI\FasterWhisperGUI.py
Description: main program 
'''

# print(1)
import os
import sys

# print(2)
# 修复程序路径依赖
BASE_DIR = os.path.dirname(os.path.abspath( __file__))
sys.path.append(os.path.join(BASE_DIR, 'resource'))
sys.path.append(os.path.join(BASE_DIR, 'faster_whisper_GUI'))

# print(3)
# from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

# print(4)
from faster_whisper_GUI.UI_MainWindows import mainWin


# 主程序入口
if __name__ == "__main__":

    # print(__name__)
    # enable dpi scale
    # QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # print("app")
    # 启动一个Qt程序，并使用传入的系统参数
    app = QApplication(sys.argv)

    # 实例化窗体
    mainWindows = mainWin()

    # 显示窗体
    mainWindows.show()

    # 退出程序，并使用app实例的退出代码
    sys.exit(app.exec())


