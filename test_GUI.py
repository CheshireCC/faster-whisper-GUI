'''
Author: CheshireCC 36411617+CheshireCC@users.noreply.github.com
Date: 2023-07-19 05:07:50
LastEditors: CheshireCC 36411617+CheshireCC@users.noreply.github.com
LastEditTime: 2023-07-19 13:50:49
FilePath: \fatser_whsiper_GUI\test_GUI.py
Description: 
'''

# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel
from PySide6.QtWidgets import QHBoxLayout, QGridLayout

from qfluentwidgets import Pivot, setTheme, Theme, LineEdit, CheckBox, ComboBox


class mainWin(QWidget):

    def __init__(self):
        super().__init__()
        setTheme(Theme.LIGHT)

        # self.setStyleSheet("""
        #     Demo{background: white}
        #     QLabel{
        #         font: 20px 'Segoe UI';
        #         background: rgb(242,242,242);
        #         border-radius: 8px;
        #     }
        # """)

        self.resize(800, 800)

        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        # self.modelInterface = QLabel('Model Interface', self)
        # self.VADInterface = QLabel('VAD Interface', self)
        # self.transcribesInterface = QLabel('Transcribes Interface', self)

        # add items to pivot
        # self.addSubInterface(self.modelInterface, 'modelInterface', '模型参数')
        # self.addSubInterface(self.VADInterface, 'VADInterface', 'VAD 设置')
        # self.addSubInterface(self.transcribesInterface, 'transcribesInterface', '转写设置')

        self.page_model = QWidget()
        self.addSubInterface(self.page_model, "pageModelParameter", "模型参数")
        self.page_VAD = QWidget()
        self.addSubInterface(self.page_VAD, "pageVADParameter", "VAD 参数")
        self.page_transcribes = QWidget()
        self.addSubInterface(self.page_transcribes, "pageTranscribesParameter", "转写")
        

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignmentFlag.AlignJustify)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.page_model)
        self.pivot.setCurrentItem(self.page_model.objectName())

        self.setupUI()
    

    def setupUI(self):

        self.setupVADUI()

    def setuoModelUI(self):
        pass
    
    def setupVADUI(self):

        # VAD 模型引入以及 VAD 参数
        VLayout_VAD = QVBoxLayout()
        HLayout_VAD_check = QHBoxLayout()

        VAD_check= CheckBox()
        VAD_check.setText("是否启用 VAD 及 VAD 参数")
        VAD_check.setChecked(False)
        VAD_check.setToolTip("VAD 模型常用来对语音文件的空白段进行筛除, 可以有效减小 Whsiper 模型幻听")
        self.VAD_check = VAD_check

        HLayout_VAD_check.setContentsMargins(10,10,10,10)
        HLayout_VAD_check.addWidget(VAD_check)

        GridLayout_VAD_param = QGridLayout()
        self.GridLayout_VAD_param = GridLayout_VAD_param
        GridLayout_VAD_param.setContentsMargins(10,10,10,10)

        label_VAD_param_threshold = QLabel()
        label_VAD_param_threshold.setText("阈值")
        LineEdit_VAD_param_threshold = LineEdit()
        LineEdit_VAD_param_threshold.setText("0.5")
        LineEdit_VAD_param_threshold.setToolTip("语音阈值。\n Silero VAD为每个音频块输出语音概率,概率高于此值的认为是语音。\n最好对每个数据集单独调整此参数,\n但“懒散”的0.5对大多数数据集来说都非常好。")
        self.GridLayout_VAD_param.addWidget(label_VAD_param_threshold,0,0)
        self.GridLayout_VAD_param.addWidget(LineEdit_VAD_param_threshold,0,1)
        self.LineEdit_VAD_param_threshold = LineEdit_VAD_param_threshold

        label_VAD_patam_min_speech_duration_ms = QLabel()
        label_VAD_patam_min_speech_duration_ms.setText("最小语音持续时间(ms)")            
        LineEdit_VAD_patam_min_speech_duration_ms = LineEdit()
        LineEdit_VAD_patam_min_speech_duration_ms.setText("250")
        LineEdit_VAD_patam_min_speech_duration_ms.setToolTip("短于该参数值的最终语音块会被抛弃。")
        self.GridLayout_VAD_param.addWidget(label_VAD_patam_min_speech_duration_ms,1,0)
        self.GridLayout_VAD_param.addWidget(LineEdit_VAD_patam_min_speech_duration_ms,1,1)
        self.LineEdit_VAD_patam_min_speech_duration_ms  = LineEdit_VAD_patam_min_speech_duration_ms

        label_VAD_patam_max_speech_duration_s = QLabel()
        label_VAD_patam_max_speech_duration_s.setText("最大语音块时长(s)")            
        LineEdit_VAD_patam_max_speech_duration_s = LineEdit()
        LineEdit_VAD_patam_max_speech_duration_s.setText("inf")
        LineEdit_VAD_patam_max_speech_duration_s.setToolTip("语音块的最大持续时间(秒)。\n比该参数值指定时长更长的块将在最后一个持续时间超过100ms的静音时间戳拆分(如果有的话),\n以防止过度切割。\n否则,它们将在参数指定值的时长之前强制拆分。")
        self.GridLayout_VAD_param.addWidget(label_VAD_patam_max_speech_duration_s, 2,0)
        self.GridLayout_VAD_param.addWidget(LineEdit_VAD_patam_max_speech_duration_s, 2,1)
        self.LineEdit_VAD_patam_max_speech_duration_s = LineEdit_VAD_patam_max_speech_duration_s
        

        label_VAD_patam_min_silence_duration_ms = QLabel()
        label_VAD_patam_min_silence_duration_ms.setText("最小静息时长(ms)")            
        LineEdit_VAD_patam_min_silence_duration_ms = LineEdit()
        LineEdit_VAD_patam_min_silence_duration_ms.setText("2000")
        LineEdit_VAD_patam_min_silence_duration_ms.setToolTip("在每个语音块结束时等待该参数值指定的时长再拆分它。")
        self.GridLayout_VAD_param.addWidget(label_VAD_patam_min_silence_duration_ms, 3,0)
        self.GridLayout_VAD_param.addWidget(LineEdit_VAD_patam_min_silence_duration_ms, 3,1)
        self.LineEdit_VAD_patam_min_silence_duration_ms = LineEdit_VAD_patam_min_silence_duration_ms


        label_VAD_patam_window_size_samples = QLabel()
        label_VAD_patam_window_size_samples.setText("采样窗口大小")
        combox_VAD_patam_window_size_samples = ComboBox()
        combox_VAD_patam_window_size_samples.addItems(["512", "1024", "1536"])
        combox_VAD_patam_window_size_samples.setCurrentIndex(1)
        combox_VAD_patam_window_size_samples.setToolTip("指定大小的音频块被馈送到silero VAD模型。\n警告!\nSilero VAD模型使用16000采样率训练得到512,1024,1536样本。\n其他值可能会影响模型性能!")
        self.GridLayout_VAD_param.addWidget(label_VAD_patam_window_size_samples, 4,0)
        self.GridLayout_VAD_param.addWidget(combox_VAD_patam_window_size_samples, 4,1)
        self.combox_VAD_patam_window_size_samples = combox_VAD_patam_window_size_samples

        label_VAD_patam_speech_pad_ms = QLabel()
        label_VAD_patam_speech_pad_ms.setText("语音块前后填充")
        LineEdit_VAD_patam_speech_pad_ms = LineEdit()
        LineEdit_VAD_patam_speech_pad_ms.setText("400")
        LineEdit_VAD_patam_speech_pad_ms.setToolTip("最终的语音块前后都由指定时长的空白填充。")
        self.GridLayout_VAD_param.addWidget(label_VAD_patam_speech_pad_ms, 5,0)
        self.GridLayout_VAD_param.addWidget(LineEdit_VAD_patam_speech_pad_ms, 5,1)
        self.LineEdit_VAD_patam_speech_pad_ms = LineEdit_VAD_patam_speech_pad_ms

        VLayout_VAD.addLayout(HLayout_VAD_check)
        VLayout_VAD.addLayout(GridLayout_VAD_param)
        VLayout_VAD.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.page_VAD.setLayout(VLayout_VAD)

        self.page_VAD.setStyleSheet("border:1px solid gray; padding: 5px;")
        
        

    # def addSubInterface(self, widget: QLabel, objectName, text):
    #     widget.setObjectName(objectName)
    #     # widget.setAlignment(Qt.AlignCenter)
    #     self.stackedWidget.addWidget(widget)
    #     self.pivot.addItem(
    #         routeKey=objectName,
    #         text=text,
    #         onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
    #     )
    
    def addSubInterface(self, layout: QWidget, objectName, text: str ):
        layout.setObjectName(objectName)
#         layout.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(layout)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(layout)
        )
        

    def onCurrentIndexChanged(self, index):
        if not index :
            index = self.stackedWidget.currentIndex()
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = mainWin()
    w.show()
    app.exec()