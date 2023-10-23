# coding:utf-8


import datetime
import sys

# # 将默认的递归深度修改为3000
# sys.setrecursionlimit(7000)  

# print输出重定向到文件
log_f = open('fasterwhispergui.log', 'w', buffering=1)
sys.stdout = log_f
sys.stderr = log_f

RunDateTime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
print(f"=========={RunDateTime}==========")

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen, QVBoxLayout

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
splash.showMessage("Loadding...", Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom, Qt.white)

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



# app.processEvents()  # 处理主进程事件

import os
import locale
# from threading import Thread
pb.setValue(10)

# splash.showMessage("import translator...") # , Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, Qt.white)
from PySide6.QtCore import QTranslator

# splash.showMessage("import windows...") #, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, Qt.white)


# MainWindows_moudle = LazyImport("faster_whisper_GUI.mainWindows")
from faster_whisper_GUI.mainWindows import MainWindows
pb.setValue(60)

from resource import rc_Translater


# 主程序入口
if __name__ == "__main__":

    
    # 修复程序路径依赖
    BASE_DIR = os.path.dirname(os.path.abspath( __file__))
    sys.path.append(os.path.join(BASE_DIR, 'resource'))
    sys.path.append(os.path.join(BASE_DIR, 'faster_whisper_GUI'))
    sys.path.append(os.path.join(BASE_DIR, 'whisperX'))
    sys.path.append(os.path.join(BASE_DIR, 'ffmpeg'))
    sys.path.append(os.path.join(BASE_DIR, 'cache'))

    # cudn 环境现随 PyTorch 提供
    # 修复环境变量 - cudnn
    # cudnn_dir = ";" + os.path.join(BASE_DIR, 'cuDNN')
    # os.environ["path"] += cudnn_dir

    # # 修复环境变量 - cuBLAS
    # cuBLAS_dir = ";" + os.path.join(BASE_DIR, 'cuBLAS')
    # os.environ["path"] += cuBLAS_dir

    # 修复环境变量 - ffmpeg
    ffmpeg_dir = ";" + os.path.join(BASE_DIR, 'ffmpeg')
    os.environ["path"] += ffmpeg_dir

    pb.setValue(65)

    # 获取当前计算机语言
    language_localtion, _ = locale.getdefaultlocale()
    language = language_localtion.split("_")[0]
    print(f"language: {language_localtion}")
    
    # splash.showMessage("set Language...")# , Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, Qt.white)
    # 非中文时加载语言翻译文件, 设置英文界面
    if language != "zh" :
        splash.showMessage(
                            "Install translator...", 
                            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, 
                            Qt.white
                        )
        
        translator = QTranslator(app)
        if translator.load(":/resource/Translater/en.qm"):
            # splash.showMessage("set Language: English") #, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, Qt.white)
            app.installTranslator(translator)
            
    pb.setValue(70)
    sys.stderr = sys.__stderr__
    log_f.close()

    # splash.showMessage("Load Windows...") #, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, Qt.white)
    
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


