
# coding:utf-8

import os
# from pathlib import Path

from PySide6.QtCore import  ( 
                                Qt
                                , QCoreApplication
                            )

from PySide6.QtWidgets import  (
                                # QFileDialog ,
                                QSpacerItem
                                , QWidget
                                , QStackedWidget
                                , QVBoxLayout
                                # , QStyle
                                , QHBoxLayout
                                , QGridLayout
                                # , QCompleter
                                # , QTextBrowser
                                # , QLabel
                            )

from PySide6.QtGui import QIcon


from qfluentwidgets import (
                            NavigationInterface
                            # , Pivot
                            # , LineEdit
                            # , CheckBox
                            # , ComboBox
                            # , RadioButton
                            # , ToolButton
                            # , EditableComboBox
                            # , PushButton
                            # , SpinBox
                            # , DisplayLabel
                            # , SegmentedWidget
                            # , StateToolTip
                            # , InfoBar
                            # , InfoBarPosition
                            # , InfoBarIcon
                            , setTheme
                            , Theme
                            , FluentIcon
                        )

from qframelesswindow import (
                                FramelessMainWindow 
                                , StandardTitleBar
                            )

from .config import (Language_dict
                    , Preciese_list
                    , Model_names
                    , Device_list
                    # , Task_list
                    # , STR_BOOL
                    # , SUBTITLE_FORMAT
                    # , CAPTURE_PARA
                )

from resource import rc_Image, rc_qss
import json

from .version import (
                        __version__
                        , __FasterWhisper_version__
                        , __WhisperX_version__
                    )

from .style_sheet import StyleSheet

from .modelPageNavigationInterface import ModelNavigationInterface
from .tranccribePageNavigationInterface import TranscribeNavigationInterface
from .vadPageNavigationInterface import VADNavigationInterface
from .processPageNavigationInterface import ProcessPageNavigationInterface
from .outputPageNavigationInterface import OutputPageNavigationInterface

from .fasterWhisperGuiIcon import FasterWhisperGUIIcon

# =======================================================================================
# UI
# =======================================================================================
class UIMainWin(FramelessMainWindow):
    """V"""

    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)

    def __init__(self):
        super().__init__()

        self.model_path = ""
        self.model_names = Model_names

        # 模型支持的计算设备
        self.device_list = Device_list
        # 模型支持的计算精度
        self.preciese_list = Preciese_list
        # 语言支持
        self.LANGUAGES_DICT = Language_dict

        self.use_auth_token_speaker_diarition= ""
        with open(r"./fasterWhisperGUIConfig.json","r") as fp:
            json_data = json.load(fp)
            self.use_auth_token_speaker_diarition = json_data["use_auth_token"]

        userDir = os.path.expanduser("~")
        cache_dir = os.path.join(userDir,".cache","huggingface","hub").replace("\\", "/")
        self.download_cache_path = cache_dir

        self.FasterWhisperModel = None

        # UI设置
        self.setupUI()

        self.initWin()
        

    def initWin(self):

        self.setObjectName("FramlessMainWin")
        setTheme(Theme.LIGHT)
        StyleSheet.MAIN_WINDOWS.apply(self)
        
        self.resize(800, 500)
        self.setGeometry(500, 200, 1147, 775)

        # 添加标题栏 
        self.setTitleBar(StandardTitleBar(self))

        self.setWindowTitle(f"FasterWhisperGUI-{__version__}--fw-{__FasterWhisper_version__}--WhisperX-{__WhisperX_version__}")
        
        self.setWindowIcon(QIcon(":/resource/Image/microphone.png"))
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

    def setupUI(self):
        
        # =====================================================================================
        # 创建窗体中心控件
        self.mainWindowsWidget = QWidget(self)
        self.mainWindowsWidget.setObjectName("mainWidget")

        # 创建窗体主布局
        self.mainLayout = QGridLayout()
        # 将主布局添加到窗体中心控件
        self.mainWindowsWidget.setLayout(self.mainLayout)

        self.vBoxLayout = QVBoxLayout()

        # 将导航布局添加到主布局
        self.mainLayout.addLayout(self.vBoxLayout,0,0)

        # 设置窗体中心控件
        self.setCentralWidget(self.mainWindowsWidget)

        # 创建一个空对象 用于改善布局顶部
        self.spacer_main = QSpacerItem(0,25)
        self.vBoxLayout.addItem(self.spacer_main)

        # 设置层到最后避免遮挡窗体按钮
        self.mainWindowsWidget.lower()
        self.lower()

        # 创建布局用于放置导航枢和分页
        self.mainHBoxLayout = QHBoxLayout()
        self.vBoxLayout.addLayout(self.mainHBoxLayout)

        # 创建窗体导航枢 和 stacke 控件 以及放置控件的垂直布局
        self.pivot = NavigationInterface(self, showMenuButton=True, showReturnButton=False)
        self.pivot.setObjectName("pivot")
        self.pivot.setExpandWidth(300)

        self.stackedWidget = QStackedWidget(self)

        self.mainHBoxLayout.addWidget(self.pivot)
        self.mainHBoxLayout.addWidget(self.stackedWidget)
        
        self.pages = []
        # 添加子界面
        self.page_model = ModelNavigationInterface(self)
        self.addSubInterface(self.page_model, "pageModelParameter", self.__tr("模型参数"), icon=FluentIcon.BOOK_SHELF)
        self.pages.append(self.page_model)

        self.page_VAD = VADNavigationInterface(self)
        self.addSubInterface(self.page_VAD, "pageVADParameter", self.__tr("VAD及WhisperX"), icon=FasterWhisperGUIIcon.VAD_PAGE)
        self.pages.append(self.page_VAD)

        self.page_transcribes = TranscribeNavigationInterface(self)
        self.addSubInterface(self.page_transcribes, "pageTranscribesParameter", self.__tr("转写参数"), icon=FasterWhisperGUIIcon.TRANSCRIPTION_PAGE)
        self.pages.append(self.page_transcribes)

        self.page_process = ProcessPageNavigationInterface(self)
        self.addSubInterface(self.page_process, "pageProcess", self.__tr("执行转写"), icon=FasterWhisperGUIIcon.HEAD_PHONE)
        self.pages.append(self.page_process)

        self.page_output = OutputPageNavigationInterface(self)
        self.addSubInterface(self.page_output, "pageOutput", self.__tr("后处理及输出"), icon=FluentIcon.SAVE_AS)
        self.pages.append(self.page_output)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.page_model)
        self.pivot.setCurrentItem(self.page_model.objectName())
    
    def addSubInterface(self, layout: QWidget, objectName, text: str, icon:QIcon=None ):
        layout.setObjectName(objectName)
#         layout.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(layout)
        item = self.pivot.addItem(
            routeKey=objectName
            ,text=text
            # 由于修复下面的 bug ，此处需要手动重新设置 setCurrentWidget 来保证换页功能正常
            ,onClick=lambda: self.stackedWidget.setCurrentWidget(layout)
            ,icon=icon
        )

    def onCurrentIndexChanged(self, index):
        if not index :
            index = self.stackedWidget.currentIndex()
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        

    

