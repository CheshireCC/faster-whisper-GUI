
import os
from PySide6.QtCore import (QCoreApplication, Qt)

from PySide6.QtWidgets import (
                                QGridLayout, 
                                QVBoxLayout, 
                                QWidget
                            )

from qfluentwidgets import (
                            SwitchButton, 
                            ComboBox, 
                            LineEdit,
                            MessageBox,
                            PushButton
                        )

from .paramItemWidget import ParamWidget
from .style_sheet import StyleSheet
from .config import default_Huggingface_user_token

from .util import outputWithDateTime

class SettingPageNavigationInterface(QWidget):
    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)
    """
    This class is used to navigate to the settings page
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.mainWidget = QWidget(self)
        self.mainWidget.setObjectName("mainObject")
        self.layout.addWidget(self.mainWidget, 0,0)

        self.mainLayout = QVBoxLayout(self.mainWidget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setupUI()
        self.signalAndSlotProcess()
        StyleSheet.SETTINGPAGEINTERFACE.apply(self)
        
    def addWidget(self, widget):
        self.mainLayout.addWidget(widget)
    def addLayout(self, layout):
        self.mainLayout.addLayout(layout)

    def setupUI(self):
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.switchButton_saveConfig = SwitchButton()
        self.switchButton_saveConfig.setChecked(True)
        self.paramItemWidget_saveConfig = ParamWidget(self.__tr("自动保存配置"), self.__tr("程序退出时自动保存配置"),self.switchButton_saveConfig, self)
        self.addWidget(self.paramItemWidget_saveConfig)

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.switchButton_autoLoadModel = SwitchButton()
        self.switchButton_autoLoadModel.setChecked(True)
        self.paramItemWidget_autoLoadModel = ParamWidget(self.__tr("自动加载模型"), self.__tr("程序启动时自动加载模型"),self.switchButton_autoLoadModel, self)
        self.addWidget(self.paramItemWidget_autoLoadModel)

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.combox_language = ComboBox()
        self.combox_language.addItems(["中文","English",self.__tr("自动")])
        self.combox_language.setCurrentIndex(2)
        self.paramItemWidget_language = ParamWidget(self.__tr("语言"), self.__tr("程序界面语言，修改后重启生效"),self.combox_language, self)
        self.addWidget(self.paramItemWidget_language)
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        self.LineEdit_use_auth_token = LineEdit()
        self.LineEdit_use_auth_token.setFixedWidth(330)
        self.use_auth_token_param_widget = ParamWidget(self.__tr("HuggingFace用户令牌"),
                                                        self.__tr("访问声源分析、分离模型需要提供经过许可的 HuggingFace 用户令牌。\n如果默认令牌失效可以尝试自行注册账号并生成、刷新令牌"),
                                                        self.LineEdit_use_auth_token 
                                                    )
        
        self.addWidget(self.use_auth_token_param_widget)
        self.use_auth_token_param_widget.mainHLayout.setStretch(0,4)
        self.use_auth_token_param_widget.mainHLayout.setStretch(1,1)

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.combox_autoGoToOutputPage = ComboBox()
        self.combox_autoGoToOutputPage.addItems([self.__tr("总是"), self.__tr("从不"),self.__tr("询问")])
        self.combox_autoGoToOutputPage.setCurrentIndex(2)

        self.paramItemWidget_autoGoToOutputPage = ParamWidget(self.__tr("转写结束后自动跳转"), self.__tr("转写结束后是否自动跳转到输出页, 目前怀疑自动跳转功能和窗体崩溃有关"), self.combox_autoGoToOutputPage)
        self.addWidget(self.paramItemWidget_autoGoToOutputPage)
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.switchButton_autoClearTempFiles = SwitchButton()
        self.switchButton_autoClearTempFiles.setOnText(self.__tr("清除"))
        self.switchButton_autoClearTempFiles.setOffText(self.__tr("不清除"))

        self.paramItemWidget_autoClearTempFiles = ParamWidget(self.__tr("自动清除临时文件"), self.__tr("程序退出时是否自动清除临时文件"), self.switchButton_autoClearTempFiles)
        self.addWidget(self.paramItemWidget_autoClearTempFiles)

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.pushButton_clearTempFiles = PushButton()
        self.pushButton_clearTempFiles.setText(self.__tr("清除"))
        self.pushButton_openTempDir = PushButton()
        self.pushButton_openTempDir.setText(self.__tr("打开目录"))

        self.paramItemWidget_TempDir = ParamWidget(self.__tr("临时文件"), self.__tr("转写完成后, 临时文件将保存在该目录下, 仅保存 srt 格式文件"), self.pushButton_openTempDir)
        self.paramItemWidget_TempDir.widgetVLayout.addWidget(self.pushButton_clearTempFiles)
        self.addWidget(self.paramItemWidget_TempDir)

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.pushButton_openLogFile = PushButton()
        self.pushButton_openLogFile.setText(self.__tr("打开"))
        self.paramItemWidget_logFile = ParamWidget(self.__tr("日志文件"), self.__tr("程序运行的日志将保存到该文件中"), self.pushButton_openLogFile)
        self.addWidget(self.paramItemWidget_logFile)

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.pushButton_openFWLogFile = PushButton()
        self.pushButton_openFWLogFile.setText(self.__tr("打开"))
        self.paramItemWidget_FWlogFile = ParamWidget(self.__tr("faster-whisper 日志文件"), self.__tr("faster-whisper 转写的日志将保存到该文件中，\n转写过程中如果发生崩溃请参看"), self.pushButton_openFWLogFile)
        self.addWidget(self.paramItemWidget_FWlogFile)

    def setSwitchStatus(self):
        self.switchButton_autoLoadModel.setChecked(False)
        self.paramItemWidget_autoLoadModel.setEnabled(self.switchButton_saveConfig.isChecked())

    def signalAndSlotProcess(self):
        self.switchButton_saveConfig.checkedChanged.connect(self.setSwitchStatus)
        self.pushButton_openTempDir.clicked.connect(lambda: os.startfile(os.path.abspath(r"./temp/").replace("\\","/")))
        self.pushButton_openLogFile.clicked.connect(lambda: os.startfile(os.path.abspath(r"./fasterwhispergui.log").replace("\\","/")))
        self.pushButton_openFWLogFile.clicked.connect(lambda: os.startfile(os.path.abspath(r"./faster_whisper.log").replace("\\","/")))  
        
        self.pushButton_clearTempFiles.clicked.connect(self.deletTempFiles)
        

    def deletTempFiles(self):
        outputWithDateTime("clearTempFiles")
        mess_ = MessageBox(self.__tr("注意"), self.__tr("将会清除全部临时文件，是否确定？"), self)
        if mess_.exec():
            try:
                os.system(r"del .\temp\*.srt")
                mess_ = MessageBox(self.__tr("提示"), self.__tr("清除成功"), self)
                mess_.show()
                print("clear over")
            except Exception as e:
                mess_ = MessageBox(self.__tr("错误"), self.__tr("清除失败"), self)
                print(f"clear temp files error: \n    {str(e)}")
        else:
            print("clear temp files cancel")
        
    def setParam(self,param:dict) -> None:
        try:
            self.switchButton_saveConfig.setChecked(param["saveConfig"])
            self.switchButton_autoLoadModel.setChecked(param["autoLoadModel"])
            self.combox_language.setCurrentIndex(param["language"])
            self.LineEdit_use_auth_token.setText(param["huggingface_user_token"])
            self.combox_autoGoToOutputPage.setCurrentIndex(param["autoGoToOutputPage"])
            self.switchButton_autoClearTempFiles.setChecked(param["autoClearTempFiles"])
        except:
            pass
    
    def getParam(self):
        param = {}
        param["saveConfig"] = self.switchButton_saveConfig.isChecked()
        param["autoLoadModel"] = self.switchButton_autoLoadModel.isChecked() if param["saveConfig"] else False
        param["language"] = self.combox_language.currentIndex()
        param["huggingface_user_token"] = self.LineEdit_use_auth_token.text().strip() or default_Huggingface_user_token 
        param["autoGoToOutputPage"] =  self.combox_autoGoToOutputPage.currentIndex()
        param["autoClearTempFiles"] = self.switchButton_autoClearTempFiles.isChecked()
        return param