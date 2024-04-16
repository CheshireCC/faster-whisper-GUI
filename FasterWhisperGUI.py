# coding:utf-8

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath( __file__))

# 修复环境变量 - python 文件夹
python_dir = ";" + os.path.join(BASE_DIR, 'python')
os.environ["path"] += python_dir

# 修复环境变量 - bin 文件夹
bin_dir = ";" + os.path.join(BASE_DIR, 'bin')
os.environ["path"] += bin_dir

from PySide6.QtCore import Qt
from PySide6.QtGui import (QFont, QPixmap)
from PySide6.QtWidgets import (QApplication, QSplashScreen, QVBoxLayout)

from qfluentwidgets import ProgressBar

class MySplashScreen(QSplashScreen):
    # 鼠标点击事件
    def mousePressEvent(self, event):
        pass

from resource import rc_Image

# 启动一个Qt程序，并使用传入的系统参数
app = QApplication(sys.argv)
app.setObjectName("FasterWhisperGUIAPP")

#设置启动界面
splash = MySplashScreen()

#初始图片
splash.setPixmap(QPixmap(r":/resource/Image/SplashScreen_0.4.0.png")) 

# 设置字体
splash.setFont(QFont('Segoe UI', 15))

#初始文本
splash.showMessage("Loading...", Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom, Qt.white)

# splash.setStyleSheet("MySplashScreen{border-radius: 10px;}")

ly = QVBoxLayout(splash)
splash.setLayout(ly)

pb = ProgressBar(splash)
pb.setMaximum(100)
pb.setMinimum(0)

ly.addWidget(pb,alignment=Qt.AlignmentFlag.AlignBottom)
ly.addSpacing(20)

# 显示启动界面
splash.show()

app.processEvents()  # 处理主进程事件

# print输出重定向到文件
log_f = open('fasterwhispergui.log', 'w', buffering=1)
sys.stdout = log_f
sys.stderr = log_f

from faster_whisper_GUI.version import __version__
from faster_whisper_GUI.util import outputWithDateTime

log_f.write(f"\nfaster_whisper_GUI: {__version__}")

outputWithDateTime("Start")

import logging

# faster_whisper 模块日志
logger_faster_whisper = logging.getLogger("faster_whisper")
logger_faster_whisper.setLevel(logging.DEBUG)
faster_whisper_logger_handler = logging.FileHandler(r"./faster_whisper.log", mode="w")
faster_whisper_logger_handler.setLevel(logging.DEBUG)
formatter1 = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",datefmt='%Y-%m-%d_%H:%M:%S')
faster_whisper_logger_handler.setFormatter(formatter1)
logger_faster_whisper.addHandler(faster_whisper_logger_handler)

pb.setValue(10)

from faster_whisper_GUI.mainWindows import MainWindows

pb.setValue(60)

from resource import rc_Translater
from faster_whisper_GUI.translator import TRANSLATOR, language

# 主程序入口
if __name__ == "__main__":
    
    # 修复程序路径依赖
    sys.path.append(os.path.join(BASE_DIR, 'resource'))
    sys.path.append(os.path.join(BASE_DIR, 'faster_whisper_GUI'))
    sys.path.append(os.path.join(BASE_DIR, 'whisperX'))
    sys.path.append(os.path.join(BASE_DIR, 'ffmpeg'))
    sys.path.append(os.path.join(BASE_DIR, 'cache'))
    sys.path.append(os.path.join(BASE_DIR, 'python'))
    sys.path.append(os.path.join(BASE_DIR, 'bin'))
    
    # 修复环境变量 - ffmpeg
    ffmpeg_dir = ";" + os.path.join(BASE_DIR, 'ffmpeg')
    os.environ["path"] += ffmpeg_dir

    # os.environ["CUDA_LAUNCH_BLOCKING"] = "0"

    pb.setValue(65)

    # 获取当前计算机语言
    # language_localtion, _ = locale.getdefaultlocale()
    # language = language_localtion.split("_")[0]
    # print(f"language: {language_localtion}")
    
    # 非中文时加载语言翻译文件, 设置英文界面
    translator = TRANSLATOR
    splash.showMessage(
                        "Install translator...", 
                        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, 
                        Qt.white
                    )

    app.installTranslator(translator)
            
    pb.setValue(70)
    sys.stderr = sys.__stderr__
    log_f.close()

    # splash.showMessage("Load Windows...") #, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, Qt.white)
    
    splash.showMessage(
                        "Launching app...", 
                        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, 
                        Qt.white
                    )
    
    mainWindows = MainWindows()
    pb.setValue(100)
    
    # splash.requestInterruption()
    # splash.stop(mainWindows)

    splash.finish(mainWindows)
    splash.deleteLater()

    ly.deleteLater()
    pb.deleteLater()

    # 显示窗体
    mainWindows.show()

    # 退出程序，并使用app实例的退出代码
    sys.exit(app.exec())


