# coding:utf-8
import os
from PySide6.QtCore import (
                            Qt,
                            QUrl
                        )

from PySide6.QtGui import (
                            QDesktopServices
                            , QPainter
                            , QPen
                            , QColor
                        )
from PySide6.QtWidgets import (
                                QWidget
                                , QLabel
                                , QVBoxLayout
                                , QHBoxLayout
                                # , QApplication
                            )

from qfluentwidgets import (ScrollArea
                            , PushButton
                            , ToolButton
                            , FluentIcon
                            , isDarkTheme
                            , toggleTheme
                            , ToolTipFilter
                            , TitleLabel
                            , CaptionLabel
                            , MessageBox
                        )

from .style_sheet import StyleSheet
from .version import (__version__,
                    __FasterWhisper_version__,
                    __WhisperX_version__, 
                    __Demucs_version__
                )

class SeparatorWidget(QWidget):
    """ Seperator widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(6, 16)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(1)
        pen.setCosmetic(True)
        c = QColor(255, 255, 255, 21) if isDarkTheme() else QColor(0, 0, 0, 50)
        pen.setColor(c)
        painter.setPen(pen)

        x = self.width() // 2
        painter.drawLine(x, 0, x, self.height())


class ToolBar(QWidget):
    """ Tool bar """

    def __init__(self, title, subtitle,  parent=None):
        # if not translator:
        #     self.translator = translator
        # else:
        #     self.translator = TRANSLATOR

        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)

        # self.documentButton = PushButton(
        #     self.tr('Documentation'), self, FluentIcon.DOCUMENT)
        self.sourceButton = PushButton(self.tr('软件更新'), self, FluentIcon.GITHUB)
        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)
        # self.themeButton = PrimaryToolButton(FluentIcon.CONSTRACT, self)
        # self.languageButton = ToolButton(FluentIcon.LANGUAGE, self)

        # 分割线
        self.separator = SeparatorWidget(self)
        # self.supportButton = ToolButton(FluentIcon.HEART, self)
        self.questionButton = ToolButton(FluentIcon.QUESTION, self)

        self.modelStatusLabel = QLabel(self.tr("模型状态："))
        self.modelStatusLabel.setObjectName("modelStatusLabel")
        self.modelStatusLabel.setFixedWidth(150)

        self.openDirButton = PushButton(self.tr("软件目录"),self, FluentIcon.DICTIONARY)

        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(150)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.vBoxLayout.setAlignment(Qt.AlignTop)


        # self.buttonLayout.setSpacing(4)
        # self.buttonLayout.setContentsMargins(0, 0, 0, 0)

        self.buttonLayout.addWidget(self.modelStatusLabel, 0, Qt.AlignLeft)
        self.buttonLayout.addStretch(1)

        self.buttonLayout.addWidget(self.themeButton, 0, Qt.AlignRight)
        # self.buttonLayout.addWidget(self.languageButton,0,Qt.AlignmentFlag.AlignRight)
        self.buttonLayout.addWidget(self.openDirButton, 0, Qt.AlignRight)
        self.buttonLayout.addWidget(self.separator, 0, Qt.AlignRight)

        # self.buttonLayout.addWidget(self.documentButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.sourceButton, 0, Qt.AlignRight)
        
        # self.buttonLayout.addWidget(self.supportButton, 0, Qt.AlignRight)
        self.buttonLayout.addWidget(self.questionButton, 0, Qt.AlignRight)
        # self.buttonLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        # self.supportButton.installEventFilter(ToolTipFilter(self.supportButton))
        self.questionButton.installEventFilter(ToolTipFilter(self.questionButton))
        self.themeButton.setToolTip(self.tr('切换主题'))
        # self.supportButton.setToolTip(self.tr('Support me'))
        self.questionButton.setToolTip(self.tr('关于'))
        self.openDirButton.setToolTip(self.tr("打开主目录"))

        self.themeButton.clicked.connect(lambda: toggleTheme(True,True))
        # self.supportButton.clicked.connect(signalBus.supportSignal)
        # self.documentButton.clicked.connect(
        #     lambda: QDesktopServices.openUrl(QUrl(HELP_URL)))
        
        self.sourceButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/CheshireCC/fatser-whisper-GUI/releases")))
        self.questionButton.clicked.connect(lambda: MessageBox(self.tr("关于"),self.tr(f"version: {__version__}" + "\n" + f"faster-whisper: {__FasterWhisper_version__}" + "\n" + f"whisperX: {__WhisperX_version__}" + "\n" + f"Demucs: {__Demucs_version__}"),parent=self.parent()).show())
        self.openDirButton.clicked.connect(lambda: os.startfile(os.path.abspath(r"./").replace("\\","/")))#print(os.path.abspath(r"./").replace("\\","/")))#os.startfile(os.path.abspath(r"./")))
        # self.languageButton.clicked.connect(self.install_uninstall_translator)

        self.vBoxLayout.addSpacing(4)

            
class NavigationBaseInterface(ScrollArea):
    """ Gallery interface """

    def __init__(self, title: str, subtitle: str,  parent=None):
        """
        Parameters
        ----------
        title: str
            The title of gallery

        subtitle: str
            The subtitle of gallery

        parent: QWidget
            parent widget
        """

        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = ToolBar(title, subtitle, self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(36, 10, 36, 10)

        self.view.setObjectName('view')
        StyleSheet.NAVIGATION_INTERFACE.apply(self)

        self.setModelStatusLabelText(False)
        

    def addWidget(self, widget):
        self.vBoxLayout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignTop)
    
    def addLayout(self, layout):
        self.vBoxLayout.addLayout(layout)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        try:
            self.toolBar.resize(self.width(), self.toolBar.height())
        except Exception as e:
            pass

    def setModelStatusLabelText(self,status:bool=True):
        if status:
            self.toolBar.modelStatusLabel.setText(self.tr("模型已加载!"))
            self.toolBar.setStyleSheet("#modelStatusLabel{ background: rgba(0, 255, 0, 0.3); }")
        else:
            self.toolBar.modelStatusLabel.setText(self.tr("模型未加载!"))
            self.toolBar.setStyleSheet("#modelStatusLabel{ background: rgba(255, 0, 0, 0.3); }")
        
