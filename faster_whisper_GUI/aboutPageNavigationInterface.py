# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import (QBrush,  QPainter, QPixmap)
from PySide6.QtWidgets import  (
                                QFrame,  
                                QVBoxLayout, 
                                QWidget, 
                                QGraphicsView, 
                                QGraphicsScene
                            )

from qfluentwidgets import (
                            DisplayLabel, 
                            ScrollArea, 
                            TitleLabel, 
                            HorizontalSeparator
                        )

from .style_sheet import StyleSheet

class ImageViewer(QGraphicsView):
    def __init__(self, parent=None, image=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        # self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(Qt.GlobalColor.transparent))
        self.setFrameShape(QFrame.NoFrame)
        # self.setInteractive(True)
        # self.setFixedHeight(430)
        # self.setFixedWidth(1160)
        
        self.pixmap = QPixmap(image)
        self.pixmap_item = self.scene().addPixmap(self.pixmap)
        
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        # self.setFixedHeight(self.width() * self.scaler)
        # self.setSceneRect(0, 0, self.width(), self.height())
        
        self.scaler = self.height() / self.width()

        self.setMinimumHeight(362)
        self.setMinimumWidth(885)
        

    def resizeEvent(self, event):
        # self.setSceneRect(0, 0, self.width(), self.height())
        
        self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.setFixedHeight(self.width() * self.scaler)
        # self.setSceneRect(0, 0, self.width(), self.height())
        
        # print(self.pixmap.width(), self.pixmap.height())
        # print(self.width(), self.height())
        # print(self.sceneRect())
        
class AboutPageNavigationInterface(ScrollArea):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        # 主控件
        self.mainWidget= QWidget(self)
        self.mainWidget.setObjectName("mainObject")
        # self.mainLayout.addWidget(self.mainWidget, 0, 0, 1, 1)

        # 主控件布局
        self.mainVLayout = QVBoxLayout(self.mainWidget)
        self.mainWidget.setLayout(self.mainVLayout)
        self.mainVLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.mainVLayout.setSpacing(10)

        self.setViewportMargins(0, 0, 0, 0)
        self.setWidget(self.mainWidget)
        self.setWidgetResizable(True)

        self.lisence = self.tr("""
使用本软件即代表您已阅读并同意以下用户协议：  
    · 您同意在遵守您所在国家或地区的法律法规的前提下使用此软件。
    · 您不得实施包括但不限于以下行为，也不得为任何违反法律法规的行为提供便利：
        - 反对宪法所规定的基本原则的。
        - 危害国家安全、泄露国家秘密、颠覆国家政权，破坏国家统一的。
        - 损害国家荣誉和利益的。
        - 煽动民族仇恨、民族歧视，破坏民族团结的。
        - 破坏国家宗教政策，宣扬邪教和封建迷信的。
        - 散布谣言，扰乱社会秩序，破坏社会稳定的。
        - 散布淫秽色情、赌博、暴力、凶杀、恐怖主义或教唆犯罪的。
        - 侮辱或诽谤他人，侵害他人合法权益的。
        - 含有法律、行政法规禁止的其他内容的。
    · 因您的数据的产生、收集、处理、使用等任何相关事项存在违反法律法规等情况而造成的全部后果及责任均由您自行承担。
        """)

        self.setupUI()

        StyleSheet.ABOUTPAGEINTERFACE.apply(self)


    def setupUI(self):

        self.strongBodyLabel = TitleLabel(self)
        self.strongBodyLabel.setText(self.tr("生成式人工智能程序用户协议"))
        self.strongBodyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.strongBodyLabel)

        self.lisenceLabel = DisplayLabel()
        self.lisenceLabel.setText(self.lisence)
        self.lisenceLabel.setScaledContents(True)
        # self.lisenceLabel.setFont(QFont("Microsoft YaHei", 13))
        self.addWidget(self.lisenceLabel)

        self.mainVLayout.addSpacing(15)
        self.mainVLayout.addWidget(HorizontalSeparator(self))

        image = r":/resource/Image/donate.png"
        self.imagelabel= ImageViewer(self, image)
        self.addWidget(self.imagelabel)
        self.imagelabel.setObjectName("imageViewer")

        self.strongBodyLabel_donate = TitleLabel(self)
        self.strongBodyLabel_donate.setText(self.tr("请我喝杯咖啡吧"))
        self.strongBodyLabel_donate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.strongBodyLabel_donate)
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        

    def addWidget(self, widget):
        self.mainVLayout.addWidget(widget)
    
    def addLayout(self, layout):
        self.mainVLayout.addLayout(layout)

