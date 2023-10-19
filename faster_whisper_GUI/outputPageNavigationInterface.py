from PySide6.QtCore import  Qt
from PySide6.QtWidgets import (
                                QHBoxLayout
                                , QSizePolicy
                            )

from qfluentwidgets import PushButton
                        
from .navigationInterface import NavigationBaseInterface
from .tableViewInterface import TabInterface

from .outputLabelLineEditButtonWidget import OutputGroupWidget


class OutputPageNavigationInterface(NavigationBaseInterface):
    def __init__(self, parent=None):
        super().__init__(title=self.tr("WhisperX And Output"),subtitle=self.tr("whisperX后处理及字幕文件输出"),parent=parent)

        self.setupUI()
    
    def setupUI(self):
        # -----------------------------------------------------------------------------------------

        # self.outputHBoxLayout = QHBoxLayout()
        # label_output_file = QLabel()
        # label_output_file.setText(self.tr("输出文件目录"))
        # self.outputHBoxLayout.addWidget(label_output_file)

        # self.LineEdit_output_dir = LineEdit()
        # self.LineEdit_output_dir.setToolTip(self.tr("输出文件保存的目录"))
        # self.LineEdit_output_dir.setPlaceholderText(self.tr("当目录为空的时候将会自动输出到每一个音频文件所在目录"))
        # self.LineEdit_output_dir.setClearButtonEnabled(True)
        # self.outputHBoxLayout.addWidget(self.LineEdit_output_dir)

        # outputDirChoseButton = ToolButton()
        # self.outputDirChoseButton = outputDirChoseButton
        # outputDirChoseButton.setToolTip(self.tr("选择输出目录"))
        # outputDirChoseButton.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_DirIcon))
        # outputDirChoseButton.resize(385,420)
        # self.outputHBoxLayout.addWidget(outputDirChoseButton)
        # self.addLayout(self.outputHBoxLayout)

        self.outputGroupWidget = OutputGroupWidget(self)
        self.addWidget(self.outputGroupWidget)
        

        self.WhisperXAligmentTimeStampleButton = PushButton()
        self.WhisperXAligmentTimeStampleButton.setText(self.tr("WhisperX 时间戳对齐"))
        self.WhisperXAligmentTimeStampleButton.setToolTip(self.tr("wav2vec2 模型进行音素分析，并进行字幕时间戳对齐，该功能需要有对应的语言的模型支持。"))

        self.WhisperXSpeakerDiarizeButton = PushButton()
        self.WhisperXSpeakerDiarizeButton.setText(self.tr("WhisperX 说话人分离"))
        self.WhisperXSpeakerDiarizeButton.setToolTip(self.tr("speachBrain 模型声纹聚类分析，将不同语音段的不同说话人进行分离"))

        self.WhisperXHBoxLayout = QHBoxLayout()
        self.WhisperXHBoxLayout.addWidget(self.WhisperXAligmentTimeStampleButton)
        self.WhisperXHBoxLayout.addWidget(self.WhisperXSpeakerDiarizeButton)
        self.WhisperXHBoxLayout.addSpacing(10)

        self.outputSubtitleFileButton = PushButton()
        self.outputSubtitleFileButton.setText(self.tr("保存字幕文件"))
        self.outputSubtitleFileButton.setToolTip(self.tr("保存结果到字幕文件"))
        self.WhisperXHBoxLayout.addWidget(self.outputSubtitleFileButton)

        self.WhisperXHBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.addLayout(self.WhisperXHBoxLayout)
        
        # 添加放置表格的标签导航页
        self.tableTab = TabInterface()
        self.tableTab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(self.tableTab)
        self.tableTab.setFixedHeight(735)
    

