
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
                                QGridLayout,
                                QHBoxLayout,
                                QVBoxLayout,
                                QWidget
                            )


from qfluentwidgets import (
                            CaptionLabel
                            , StrongBodyLabel
                        )

from .style_sheet import StyleSheet

class ParamWidget(QWidget):
    def __init__(self, title:str, caption:str, widget:QWidget ,parent=None):
        super().__init__(parent=parent)

        self.mainWidget = QWidget(self)
        self.mainWidget.setObjectName("mainObject")

        self.mainLayout = QGridLayout()
        
        self.mainHLayout = QHBoxLayout()
        self.titleVLayout = QVBoxLayout()
        self.widgetVLayout = QVBoxLayout()

        self.titleLabel = StrongBodyLabel(title, self)
        self.captionLable = CaptionLabel(caption, self)

        self.widget = widget
        
        self.setupUI()
        StyleSheet.TRANSCRIBEPARAMITEMWIDGET.apply(self)
    
    def setupUI(self):
        
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.mainWidget)
        
        self.mainWidget.setLayout(self.mainHLayout)

        self.titleVLayout.addWidget(self.titleLabel)
        self.titleVLayout.addWidget(self.captionLable)

        self.mainHLayout.addLayout(self.titleVLayout)
        self.mainHLayout.addSpacing(10)
        self.mainHLayout.addLayout(self.widgetVLayout)

        self.widgetVLayout.addWidget(self.widget)

        self.mainHLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.titleVLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.widgetVLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        self.mainHLayout.setStretch(0,8)
        self.mainHLayout.setStretch(1,1)
