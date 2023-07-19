'''
Author: CheshireCC 36411617+CheshireCC@users.noreply.github.com
Date: 2023-07-18 22:27:35
LastEditors: CheshireCC 36411617+CheshireCC@users.noreply.github.com
LastEditTime: 2023-07-18 22:48:44
FilePath: \fatser_whsiper_GUI\faster_whsiper_GUI\FasterWhisperGUI.py
Description: 
'''
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
import sys
from UI_MainWindows import mainWin

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


