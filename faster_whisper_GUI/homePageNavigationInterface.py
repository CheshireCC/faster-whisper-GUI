# coding:utf-8

from PySide6.QtCore import QEasingCurve, Qt
from .navigationInterface import NavigationBaseInterface

from .homePageItemLabel import ItemLabel
from qfluentwidgets import FlowLayout

from resource import rc_Image


class HomePageNavigationinterface(NavigationBaseInterface):
    def __init__(self, parent=None):
        super().__init__(title=self.tr("Home"), subtitle=self.tr("faster-whisper 为主要后端的 ASR 及 AVE 软件"), parent=parent)
        self.steupUI()

    def steupUI(self):
        # self.toolBar.deleteLater()
        # self.vBoxLayout.removeWidget(self.toolBar)
        # self.toolBar = None

        self.toolBar.modelStatusLabel.setVisible(False)
        # self.toolBar.buttonLayout.removeWidget( self.toolBar.modelStatusLabel)

        self.hBoxLayout = FlowLayout(needAni=True)
        self.hBoxLayout.setContentsMargins(30,30,30,30)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.setAnimation(250, QEasingCurve.OutQuad)
        self.addLayout(self.hBoxLayout)
        
        self.itemLabel_demucs = ItemLabel(  self,     
                                            self.tr("Demucs"), 
                                            self.tr("自动人声提取")
                                        )
        
        self.hBoxLayout.addWidget(self.itemLabel_demucs)#, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        self.itemLabel_demucs.setMainButton(self.tr("进入"))
        
        # image = QImage(FasterWhisperGUIIcon.DEMUCS.png())
        # self.itemLabel_demucs.imageLabel.setImage(image)
        # self.itemLabel_demucs.setFixedHeight(440)

        self.itemLabel_faster_whisper = ItemLabel(
                                                    self,
                                                    self.tr("faster-whisper"),
                                                    self.tr("自动人声识别")
                                                )
        
        self.itemLabel_faster_whisper.setSubButton(self.tr("设置参数"))
        self.itemLabel_faster_whisper.setMainButton(self.tr("进入"))
        
        
        self.hBoxLayout.addWidget(self.itemLabel_faster_whisper)#, 3, alignment=Qt.AlignmentFlag.AlignLeft)

        self.itemLabel_whisperx = ItemLabel(
                                            self,
                                            self.tr("whisperX"),
                                            self.tr("字幕后处理")
                                        )
        self.itemLabel_whisperx.setMainButton(self.tr("进入"))
        
        self.hBoxLayout.addWidget(self.itemLabel_whisperx)#, 3, alignment=Qt.AlignmentFlag.AlignLeft)
