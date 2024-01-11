# coding:utf-8

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
                                QHBoxLayout, 
                                QPushButton, 
                                QVBoxLayout, 
                                QWidget, 
                            )
from qfluentwidgets import (ImageLabel, CaptionLabel, TitleLabel)
from .style_sheet import StyleSheet

class ItemLabel(QWidget):
    def __init__(self, parent, title:str, subTitle:str) -> None:
        super().__init__(parent=parent)

        self.parent = parent

        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)
        self.mainWidget = QWidget(self)
        self.vBoxLayout.addWidget(self.mainWidget)
        self.mainWidget.setObjectName("mainWidget")

        self.mainWidget.setFixedHeight(450)

        self.titleLabel_page_1 = TitleLabel()
        self.titleLabel_page_1.setText(title)
        self.subTitleLabel_page_1 = CaptionLabel()
        self.subTitleLabel_page_1.setText(subTitle)
        self.subTitleLabel_page_1.setScaledContents(True)

        self.imageLabel = ImageLabel()
        self.imageLabel.setFixedSize(150,150)
        self.imageLabel.setScaledContents(True)

        self.vBoxLayout_label = QVBoxLayout()
        self.vBoxLayout_label.setSpacing(10)
        self.vBoxLayout_label.setContentsMargins(30,30,30,30)
        self.vBoxLayout_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainWidget.setLayout(self.vBoxLayout_label)

        self.mainButton = QPushButton()
        self.mainButton.setObjectName("mainPushButton")

        self.subButton = QPushButton()
        self.subButton.setObjectName("subPushButton")

        self.setupUI()
        StyleSheet.HOME_ITEM.apply(self)

    def setMainButton(self, text):
        self.vBoxLayout_label.addWidget(self.mainButton, Qt.AlignmentFlag.AlignBottom)
        self.mainButton.setText(text)

    def setSubButton(self, text):
        self.vBoxLayout_label.addWidget(self.subButton, Qt.AlignmentFlag.AlignBottom)
        self.subButton.setText(text)

    def setupUI(self):
        
        # print("setupUI")

        self.vBoxLayout_label.addWidget(self.titleLabel_page_1, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout_label.addWidget(self.subTitleLabel_page_1, 0 , Qt.AlignmentFlag.AlignTop)

        # self.vBoxLayout_label.addSpacing(300)
        # self.vBoxLayout_label.addItem(QSpacerItem(0,150))

        self.hBoxLayou_imageLabel = QHBoxLayout()
        self.vBoxLayout_label.addLayout(self.hBoxLayou_imageLabel)
        self.hBoxLayou_imageLabel.addWidget(self.imageLabel,alignment=Qt.AlignmentFlag.AlignCenter)

        self.vBoxLayout_label.addSpacing(50)

    def addWidget(self, widget, alignment):
        self.vBoxLayout_label.addWidget(widget,alignment=alignment)

    def addLayout(self, layout):
        self.vBoxLayout_label.addLayout(layout)

