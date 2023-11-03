from PySide6.QtCore import  Qt
from PySide6.QtWidgets import (
                                QHBoxLayout,
                                QSizePolicy,
                            )

from qfluentwidgets import PushButton,ComboBox
from qfluentwidgets.components.widgets.label import BodyLabel, StrongBodyLabel
from qfluentwidgets.components.widgets.separator import HorizontalSeparator
from qfluentwidgets.components.widgets.spin_box import SpinBox

from faster_whisper_GUI.config import SUBTITLE_FORMAT
                        
from .navigationInterface import NavigationBaseInterface
from .tableViewInterface import TabInterface

from .outputLabelLineEditButtonWidget import OutputGroupWidget
from .config import ENCODING_DICT

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
        self.WhisperXHBoxLayout.addWidget(self.WhisperXAligmentTimeStampleButton, 0, Qt.AlignmentFlag.AlignLeft)
        self.WhisperXHBoxLayout.addWidget(self.WhisperXSpeakerDiarizeButton, 0, Qt.AlignmentFlag.AlignLeft)
        self.WhisperXHBoxLayout.addSpacing(10)

        self.outputSubtitleFileButton = PushButton()
        self.outputSubtitleFileButton.setText(self.tr("保存字幕文件"))
        self.outputSubtitleFileButton.setToolTip(self.tr("保存结果到字幕文件"))
        self.WhisperXHBoxLayout.addWidget(self.outputSubtitleFileButton, 0, Qt.AlignmentFlag.AlignLeft)
        
        self.WhisperXHBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.unloadWhisperModelPushbutton = PushButton()
        self.unloadWhisperModelPushbutton.setText(self.tr("卸载模型"))
        self.unloadWhisperModelPushbutton.setToolTip(self.tr("卸载当前使用的模型"))
        self.WhisperXHBoxLayout.addSpacing(10)
        self.WhisperXHBoxLayout.addWidget(self.unloadWhisperModelPushbutton, 0, Qt.AlignmentFlag.AlignRight)

        self.addLayout(self.WhisperXHBoxLayout)
        
        # =============================================================================================
        # 添加放置表格的标签导航页
        self.tableTab = TabInterface()
        self.tableTab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(self.tableTab)
        self.tableTab.setFixedHeight(735)

        # =============================================================================================

        self.Label_min_speaker = BodyLabel(self.tr("最少声源数"))
        self.SpinBox_min_speaker = SpinBox()
        self.SpinBox_min_speaker.setToolTip(self.tr("音频中需分出来的最少的说话人的人数"))

        self.Label_max_speaker = BodyLabel(self.tr("最大声源数"))
        self.SpinBox_max_speaker = SpinBox()
        self.SpinBox_max_speaker.setToolTip(self.tr("音频中需分出来的最多的说话人的人数"))

        self.controlLabel_wshiperx = StrongBodyLabel(self.tr("whisperX 参数控制"))

        self.tableTab.panelLayout.addSpacing(15)
        self.tableTab.panelLayout.addWidget(self.controlLabel_wshiperx)
        self.tableTab.panelLayout.addWidget(HorizontalSeparator())
        
        self.tableTab.panelLayout.addSpacing(4)
        self.tableTab.panelLayout.addWidget(self.Label_min_speaker)
        self.tableTab.panelLayout.addWidget(self.SpinBox_min_speaker)

        self.tableTab.panelLayout.addSpacing(4)
        self.tableTab.panelLayout.addWidget(self.Label_max_speaker)
        self.tableTab.panelLayout.addWidget(self.SpinBox_max_speaker)
        
        # =====================================================================================
        
        self.controlLabel_output = StrongBodyLabel(self.tr("输出参数控制"))

        self.label_output_format = BodyLabel(self.tr("输出文件格式"))
        self.combox_output_format = ComboBox()
        self.combox_output_format.setToolTip(self.tr("输出字幕文件的格式"))
        self.combox_output_format.addItems(["ALL"] + SUBTITLE_FORMAT)
        self.combox_output_format.setCurrentIndex(0)

        self.label_output_code = BodyLabel(self.tr("输出文件编码"))
        self.combox_output_code = ComboBox()
        self.combox_output_code.setToolTip(self.tr("输出文件的编码"))
        self.combox_output_code.addItems([item[0] for item in ENCODING_DICT.items()])
        self.combox_output_code.setCurrentIndex(0)

        self.tableTab.panelLayout.addSpacing(15)
        self.tableTab.panelLayout.addWidget(self.controlLabel_output)
        self.tableTab.panelLayout.addWidget(HorizontalSeparator())
        
        self.tableTab.panelLayout.addSpacing(4)
        self.tableTab.panelLayout.addWidget(self.label_output_format)
        self.tableTab.panelLayout.addWidget(self.combox_output_format)

        self.tableTab.panelLayout.addSpacing(4)
        self.tableTab.panelLayout.addWidget(self.label_output_code)
        self.tableTab.panelLayout.addWidget(self.combox_output_code)
        