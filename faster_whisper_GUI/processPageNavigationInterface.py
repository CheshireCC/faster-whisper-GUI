from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
                                QGridLayout
                                , QHBoxLayout
                                , QLabel
                                , QSpacerItem
                                , QStyle
                                , QTextBrowser
                                # , QVBoxLayout
                            )
from qfluentwidgets import (
                            PushButton
                            , RadioButton
                            , ToolButton
                            , ComboBox
                            , LineEdit
                            , TextEdit
                        )

from .navigationInterface import NavigationBaseInterface

from .config import CAPTURE_PARA

class ProcessPageNavigationInterface(NavigationBaseInterface):
    
    def __init__(self, parent=None):
        super().__init__(
                        title = self.tr("Transcription")
                        , subtitle = self.tr("选择文件、字幕文件保存目录、转写文件")
                        , parent=parent)
        
        self.setupUI()

        self.SignalAndSlotConnect()

        
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
        self.combox_capture = ComboBox()
        self.combox_capture.addItems([f"{x['channel']} channel, {x['dType']} bit, {x['rate']} Hz ({x['quality']})" for x in CAPTURE_PARA])
        self.combox_capture.setCurrentIndex(1)
        spacer = QSpacerItem(10, 0) 
        
        self.hBoxLayout_Audio_capture_para.addWidget(self.label_capture)
        self.hBoxLayout_Audio_capture_para.addItem(spacer)
        self.hBoxLayout_Audio_capture_para.addWidget(self.combox_capture)

        self.gridBoxLayout_transcribe_capture.addItem(self.hBoxLayout_Audio_capture_para, 0, 2)
        
        self.addLayout(self.gridBoxLayout_transcribe_capture)
        
        self.GridBoxLayout_targetFiles = QGridLayout()
        self.addLayout(self.GridBoxLayout_targetFiles)

        label_1 = QLabel()
        label_1.setText(self.tr("目标音频文件"))
        self.GridBoxLayout_targetFiles.addWidget(label_1, 0, 0)
        # hBoxLayout_Audio_File.addWidget(label_1)

        self.LineEdit_audio_fileName = LineEdit()
        self.LineEdit_audio_fileName.setToolTip(self.tr("要转写的音频文件路径"))
        self.LineEdit_audio_fileName.setClearButtonEnabled(True)
        self.GridBoxLayout_targetFiles.addWidget(self.LineEdit_audio_fileName, 0, 1)

        fileChosePushButton = ToolButton()
        self.fileOpenPushButton = fileChosePushButton
        fileChosePushButton.setToolTip(self.tr("选择要转写的音频文件"))
        fileChosePushButton.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_FileIcon))
        fileChosePushButton.resize(385,420)
        self.GridBoxLayout_targetFiles.addWidget(fileChosePushButton, 0, 2)

        # -----------------------------------------------------------------------------------------
        label_output_file = QLabel()
        label_output_file.setText(self.tr("输出文件目录"))
        self.GridBoxLayout_targetFiles.addWidget(label_output_file, 1, 0 )

        self.LineEdit_output_dir = LineEdit()
        self.LineEdit_output_dir.setToolTip(self.tr("输出文件保存的目录"))
        self.LineEdit_output_dir.setClearButtonEnabled(True)
        self.GridBoxLayout_targetFiles.addWidget(self.LineEdit_output_dir, 1, 1)

        outputDirChoseButton = ToolButton()
        self.outputDirChoseButton = outputDirChoseButton
        outputDirChoseButton.setToolTip(self.tr("选择输出目录"))
        outputDirChoseButton.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_DirIcon))
        outputDirChoseButton.resize(385,420)
        self.GridBoxLayout_targetFiles.addWidget(outputDirChoseButton, 1 , 2)

        # ------------------------------------------------------------------------------------------
        self.button_process = PushButton()
        self.button_process.setObjectName("processButton")
        self.button_process.setText(self.tr("      开始"))
        self.button_process.setIcon(QIcon(self.parent().processPageSVG))

        # self.button_process.setStyleSheet("#processButton{background-color : rgba(0, 255, 0, 100);}")
        # self.button_process.setStyleSheet("#processButton{background:242 242 242}")
        
        self.addWidget(self.button_process)
        
        # ------------------------------------------------------------------------------------------
        self.processResultText = TextEdit()
        self.processResultText.setFixedHeight(400)
        self.addWidget(self.processResultText)

        # self.page_process.setStyleSheet("#pageProcess{border: 1px solid cyan; padding: 5px;}")
        # 根据选择设置相关控件的状态
        self.setTranscribeOrCapture()

    def setTranscribeOrCapture(self):
        num_widgets_layout = self.GridBoxLayout_targetFiles.columnCount()
        for i in range(num_widgets_layout):
            widget = self.GridBoxLayout_targetFiles.itemAtPosition(0, i).widget() # itemAt(i).widget()
            widget.setEnabled(self.transceibe_Files_RadioButton.isChecked())
        
        num_widgets_layout = self.hBoxLayout_Audio_capture_para.count()
        # print(f"num_widgets_layout:{num_widgets_layout}")

        for i in range(num_widgets_layout):
            widget = self.hBoxLayout_Audio_capture_para.itemAt(i).widget()
            # print(widget)
            try:
                widget.setEnabled(self.audio_capture_RadioButton.isChecked())
            except Exception as e:
                print(str(e))
        
    def SignalAndSlotConnect(self):
        self.transceibe_Files_RadioButton.clicked.connect(self.setTranscribeOrCapture)
        self.audio_capture_RadioButton.clicked.connect(self.setTranscribeOrCapture)