# coding:utf-8

import datetime
import sys
# 将默认的递归深度修改为3000
sys.setrecursionlimit(7000)  
# print输出重定向到文件
log_f = open('fasterwhispergui.log', 'w')
sys.stdout = log_f
sys.stderr = log_f

RunDateTime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
print(f"=========={RunDateTime}==========")

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

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
# splash.setPixmap(QPixmap(r":/resource/Image/FasterWhisper.png")) 
splash.setPixmap(QPixmap(r":/resource/Image/SplashScreen_0.25.jpg")) 
#初始文本
splash.showMessage("Lodding...", Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom, Qt.white)
# splash.showMessage("Lodding...", Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, Qt.white)
# 设置字体
splash.setFont(QFont('MicrosoftYaHei', 10))
# 显示启动界面
splash.show()
app.processEvents()  # 处理主进程事件

import os
from PySide6.QtCore import QTranslator
import locale
from faster_whisper_GUI.UI_MainWindows import mainWin
from resource import rc_Translater


# 主程序入口
if __name__ == "__main__":

    # 修复程序路径依赖
    BASE_DIR = os.path.dirname(os.path.abspath( __file__))
    sys.path.append(os.path.join(BASE_DIR, 'resource'))
    sys.path.append(os.path.join(BASE_DIR, 'faster_whisper_GUI'))

    # 修复环境变量 - cudnn
    cudnn_dir = ";" + os.path.join(BASE_DIR, 'cuDNN')
    os.environ["path"] += cudnn_dir

    # 修复环境变量 - cuBLAS
    cuBLAS_dir = ";" + os.path.join(BASE_DIR, 'cuBLAS')
    os.environ["path"] += cuBLAS_dir

    # 修复环境变量 - ffmpeg
    ffmpeg_dir = ";" + os.path.join(BASE_DIR, 'ffmpeg')
    os.environ["path"] += ffmpeg_dir

    # 获取当前计算机语言
    language_localtion, _ = locale.getdefaultlocale()
    language = language_localtion.split("_")[0]
    # print(language_localtion)
    # 非中文时加载语言翻译文件，进行国际化
    if language != "zh" :
        translator = QTranslator(app)
        if translator.load(":/resource/Translater/en.qm"):
            app.installTranslator(translator)
            
    sys.stderr = sys.__stderr__
    log_f.close()

    # 实例化窗体
    mainWindows = mainWin()
    # 显示窗体
    mainWindows.show()

    # 隐藏启动界面
    splash.finish(mainWindows)  
    # 将启动界面标记为稍后删除
    splash.deleteLater()

    # 退出程序，并使用app实例的退出代码
    sys.exit(app.exec())


