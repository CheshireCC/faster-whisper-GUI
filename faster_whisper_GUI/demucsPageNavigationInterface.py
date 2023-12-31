# coding:utf-8
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import (
                                QHBoxLayout, 
                                QLabel, 
                                QVBoxLayout, 
                                QWidget
                            )

from qfluentwidgets import (DoubleSpinBox, PushButton, ComboBox, FluentIcon)


from .navigationInterface import NavigationBaseInterface
from .fileNameListViewInterface import FileNameListView
from .outputLabelLineEditButtonWidget import OutputGroupWidget

from .style_sheet import StyleSheet

from .config import STEMS

class DemucsParamGroupWidget(QWidget):
    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)
    
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)
        self.mainWidget = QWidget()
        self.mainWidget.setObjectName("mainObject")

        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)

        self.setupUI()
    
    def addWidget(self, widget, alignment):
        self.mainLayout.addWidget(widget, alignment=alignment)
    
    def addLayout(self, layout):
        self.mainLayout.addLayout(layout)

    
    def setupUI(self):

        self.label_ = QLabel(self.__tr("Demucs 参数"))
        self.vBoxLayout.addWidget(self.label_)

        # =====================================================================

        self.vBoxLayout.addWidget(self.mainWidget)

        # =====================================================================
        self.param_hBoxLayout = QHBoxLayout()
        self.addLayout(self.param_hBoxLayout)
        self.param_hBoxLayout.setContentsMargins(10,10,10,10)
        
        self.vBoxLayout_overlap = QVBoxLayout()
        self.param_hBoxLayout.addLayout(self.vBoxLayout_overlap)

        self.spinBox_overlap = DoubleSpinBox()
        self.spinBox_overlap.setMaximum(1.0)
        self.spinBox_overlap.setMinimum(0.1)
        self.spinBox_overlap.setSingleStep(0.1)
        self.spinBox_overlap.setValue(0.10)
        self.spinBox_overlap.setDecimals(2)
        self.spinBox_overlap.setToolTip(self.tr("分段采样的段间重叠度，该值不宜过小，以免影响分段之间的分离结果的融合度"))
        
        self.label_overlap_param = QLabel(self.tr("采样重叠度"))

        self.vBoxLayout_overlap.addWidget(self.label_overlap_param)
        self.vBoxLayout_overlap.addWidget(self.spinBox_overlap)

        # =============================================================================
        self.vBoxLayout_segment = QVBoxLayout()
        self.param_hBoxLayout.addLayout(self.vBoxLayout_segment)

        self.spinBox_segment = DoubleSpinBox()
        self.spinBox_segment.setMaximum(100.0)
        self.spinBox_segment.setMinimum(1)
        self.spinBox_segment.setSingleStep(5)
        self.spinBox_segment.setValue(10)
        self.spinBox_segment.setDecimals(1)
        self.spinBox_segment.setToolTip(self.tr("Demucs 是一个极其消耗计算机内存和显存的模型，\n世界上没有任何计算机能够直接使用该模型处理长时音频数据\n因此数据将按照该值所示的秒数，分段处理，值越大将越消耗计算机资源，但效果可能会有提升"))

        self.label_segment_param = QLabel(self.tr("分段长度(s)"))

        self.vBoxLayout_segment.addWidget(self.label_segment_param)
        self.vBoxLayout_segment.addWidget(self.spinBox_segment)

        # =============================================================================
        self.vBoxLayout_stems = QVBoxLayout()
        self.param_hBoxLayout.addLayout(self.vBoxLayout_stems)

        self.comboBox_stems = ComboBox()
        self.comboBox_stems.addItems(STEMS)
        self.comboBox_stems.setCurrentIndex(1)

        self.label_stems_param = QLabel(self.tr("输出音轨"))
        
        self.vBoxLayout_stems.addWidget(self.label_stems_param)
        self.vBoxLayout_stems.addWidget(self.comboBox_stems)


class DemucsPageNavigation(NavigationBaseInterface):
    def __init__(self, parent=None):
        super().__init__(title="Demucs", subtitle=self.tr("使用 Demucs4.0 模型的 AVE（自动人声提取）方案"), parent=parent)
        # self.parent = parent

        self.setupUI()

        StyleSheet.DENUCE_INTERFACE.apply(self.demucs_param_widget)

    
    def setupUI(self):

        self.toolBar.modelStatusLabel.setVisible(False)

        self.fileListView = FileNameListView(self)
        self.addWidget(self.fileListView)

        # =============================================================================
        self.demucs_param_widget = DemucsParamGroupWidget(self)
        self.addWidget(self.demucs_param_widget)

        # =============================================================================
        self.outputGroupWidget = OutputGroupWidget(self)
        self.addWidget(self.outputGroupWidget)

        
        # =============================================================================
        self.process_button = PushButton()
        self.addWidget(self.process_button)
        self.process_button.setText(self.tr("提取"))
        self.process_button.setIcon(FluentIcon.IOT)

    def getParam(self) -> dict:
        param = {}
        param["overlap"] = self.demucs_param_widget.spinBox_overlap.value()
        param["segment"]= self.demucs_param_widget.spinBox_segment.value()
        param["tracks"] = self.demucs_param_widget.comboBox_stems.currentIndex()

        return param

    def setParam(self, param: dict) -> None:

        self.demucs_param_widget.spinBox_overlap.setValue(param["overlap"] )
        self.demucs_param_widget.spinBox_segment.setValue(param["segment"])
        self.demucs_param_widget.comboBox_stems.setCurrentIndex(param["tracks"])

