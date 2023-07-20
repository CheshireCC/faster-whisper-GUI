'''
Author: CheshireCC 
Date: 2023-07-18 22:27:35
LastEditors: CheshireCC 
LastEditTime: 2023-07-20 23:33:10
FilePath: \fatser_whsiper_GUI\faster_whsiper_GUI\FasterWhisperGUI.py
Description: main program 
'''
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
import sys
from faster_whsiper_GUI.UI_MainWindows import mainWin

# import necessary models
from PySide6.QtWidgets import QApplication
import sys

# 主程序入口
if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 启动一个Qt程序，并使用传入的系统参数
    app = QApplication(sys.argv)
    # 实例化窗体
    mainWin = mainWin()
    # 显示窗体
    mainWin.show()
    # 退出程序，并使用app实例的退出代码
    sys.exit(app.exec())


