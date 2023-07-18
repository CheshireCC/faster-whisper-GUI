'''
Author: CheshireCC 36411617+CheshireCC@users.noreply.github.com
Date: 2023-07-18 22:27:35
LastEditors: CheshireCC 36411617+CheshireCC@users.noreply.github.com
LastEditTime: 2023-07-18 22:48:44
FilePath: \fatser_whsiper_GUI\faster_whsiper_GUI\FasterWhisperGUI.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from PySide6.QtCore import QDataStream, QFile, Slot
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QSizePolicy
import sys

from PySide6.QtGui import QPixmap

from qframelesswindow import FramelessWindow as FW

from UI_MainWindows import mainWin

# import necessary models
from PySide6.QtWidgets import QApplication
import sys

# 主程序入口
if __name__ == "__main__":
    # 启动一个Qt程序，并使用传入的系统参数
    app = QApplication(sys.argv)
    # 实例化窗体
    mainWin = mainWin()
    # 显示窗体
    mainWin.show()
    # 退出程序，并使用app实例的退出代码
    sys.exit(app.exec())

    
