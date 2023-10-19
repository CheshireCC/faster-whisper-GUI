from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
                                QGridLayout
                                , QHBoxLayout
                                , QLabel
                                , QSpacerItem
                            )

from qfluentwidgets import (
                            PushButton
                            , RadioButton
                            , ComboBox
                            , TextEdit
                        )

from .navigationInterface import NavigationBaseInterface
from .fasterWhisperGuiIcon import FasterWhisperGUIIcon
from .config import CAPTURE_PARA

# from .style_sheet import StyleSheet
from .fileNameListViewInterface import FileNameListView

class ProcessPageNavigationInterface(NavigationBaseInterface):
    
    def __init__(self, parent=None):
        super().__init__(
                        title = self.tr("Transcription")
                        , subtitle = self.tr("选择文件、字幕文件保存目录、转写文件")
                        , parent=parent
                    )
        
        self.setupUI()
        # self.SignalAndSlotConnect()

        
    def setupUI(self):

        self.gridBoxLayout_transcribe_capture = QGridLayout()
        self.transceibe_Files_RadioButton = RadioButton()
        self.transceibe_Files_RadioButton.setText(self.tr("转写文件"))
        self.transceibe_Files_RadioButton.setChecked(True)
        self.gridBoxLayout_transcribe_capture.addWidget(self.transceibe_Files_RadioButton, 0 ,0)

        self.audio_capture_RadioButton = RadioButton()
        self.audio_capture_RadioButton.setText(self.tr("音频采集"))
        self.gridBoxLayout_transcribe_capture.addWidget(self.audio_capture_RadioButton, 0, 1)
        self.audio_capture_RadioButton.setEnabled(False)
        self.gridBoxLayout_transcribe_capture.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.hBoxLayout_Audio_capture_para = QHBoxLayout()
        self.label_capture = QLabel(self.tr("音频采集参数"))
        self.label_capture.setEnabled(False)
        self.combox_capture = ComboBox()
        self.combox_capture.addItems([f"{x['channel']} channel, {x['dType']} bit, {x['rate']} Hz ({x['quality']})" for x in CAPTURE_PARA])
        self.combox_capture.setCurrentIndex(1)
        spacer = QSpacerItem(10, 0) 
        self.combox_capture.setEnabled(False)
        
        self.hBoxLayout_Audio_capture_para.addWidget(self.label_capture)
        self.hBoxLayout_Audio_capture_para.addItem(spacer)
        self.hBoxLayout_Audio_capture_para.addWidget(self.combox_capture)

        self.gridBoxLayout_transcribe_capture.addItem(self.hBoxLayout_Audio_capture_para, 0, 2)
        
        self.addLayout(self.gridBoxLayout_transcribe_capture)
        
        self.fileNameListView = FileNameListView(self)
        self.addWidget(self.fileNameListView)

        # ------------------------------------------------------------------------------------------
        self.button_process = PushButton()
        self.button_process.setObjectName("processButton")
        self.button_process.setText(self.tr("开始"))
        self.button_process.setIcon(FasterWhisperGUIIcon.PROCESS)
        
        self.addWidget(self.button_process)
        
        # ------------------------------------------------------------------------------------------
        self.processResultText = TextEdit()
        self.processResultText.setFixedHeight(400)
        self.addWidget(self.processResultText)
