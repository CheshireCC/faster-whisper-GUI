
import os
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (QFileDialog, 
                                QHBoxLayout, 
                                QLabel, 
                                QStyle, 
                                QVBoxLayout, 
                                QWidget
                            )

from qfluentwidgets import LineEdit, ToolButton
from .style_sheet import StyleSheet

class OutputGroupWidget(QWidget):

    def __init__(self, parant):
        super().__init__(parent=parant)

        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)

        self.mainWidget = QWidget()
        self.vBoxLayout.addWidget(self.mainWidget)
        self.mainWidget.setObjectName("mainObject")

        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)

        self.setupUI()

        StyleSheet.OUTPUT_GROUP_WIDGET.apply(self)

        # 设置接受文件拖放
        self.setAcceptDrops(True)

    
    def addWidget(self, widget, alignment):
        self.mainLayout.addWidget(widget, alignment=alignment)
    
    def addLayout(self, layout):
        self.mainLayout.addLayout(layout)
    
    def setupUI(self):
        
        self.outputHBoxLayout = QHBoxLayout()
        self.addLayout(self.outputHBoxLayout)

        label_output_file = QLabel()
        label_output_file.setText(self.tr("输出文件目录"))
        self.outputHBoxLayout.addWidget(label_output_file)

        self.LineEdit_output_dir = LineEdit()
        self.LineEdit_output_dir.setToolTip(self.tr("输出文件保存的目录"))
        self.LineEdit_output_dir.setPlaceholderText(self.tr("当目录为空的时候将会自动输出到每一个音频文件所在目录"))
        self.LineEdit_output_dir.setClearButtonEnabled(True)
        self.outputHBoxLayout.addWidget(self.LineEdit_output_dir)

        outputDirChoseButton = ToolButton()
        self.outputDirChoseButton = outputDirChoseButton
        outputDirChoseButton.setToolTip(self.tr("选择输出目录"))
        outputDirChoseButton.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_DirIcon))
        outputDirChoseButton.resize(385,420)
        self.outputHBoxLayout.addWidget(outputDirChoseButton)

        set_output_file = lambda path: path if path != "" else self.LineEdit_output_dir.text()
        self.outputDirChoseButton.clicked.connect(lambda:self.LineEdit_output_dir.setText(set_output_file(QFileDialog.getExistingDirectory(self,"选择输出文件存放目录", self.LineEdit_output_dir.text()))))
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()  # 接受拖放事件
        else:
            event.ignore()
        
    def dropEvent(self, a0: QDropEvent) -> None:
        """
        重写鼠标放开事件
        :param a0:事件
        :return:None
        """
        # 获取拖拽进来的所有文件的路径
        urls = a0.mimeData().urls()
        
        fileNames = [url.toLocalFile() for url in urls]
        
        fileName = fileNames[0]

        
        if os.path.isfile(fileName):
            dir_, _ = os.path.split(fileName)

        elif os.path.isdir(fileName):
            dir_ = fileName

        self.LineEdit_output_dir.setText(dir_)




        