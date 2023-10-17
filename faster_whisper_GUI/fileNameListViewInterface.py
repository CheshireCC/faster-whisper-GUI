
import os

from PySide6.QtCore import QStringListModel, Qt, QCoreApplication
import PySide6.QtGui

from PySide6.QtWidgets import (
                                QWidget
                                , QVBoxLayout
                                , QLabel
                                , QHBoxLayout
                                , QListView
                                , QFileDialog
                            )

from qfluentwidgets import (
                            ListView
                            , ToolButton
                            , FluentIcon
                            , InfoBar
                            , InfoBarPosition
                            )

from .style_sheet import StyleSheet
from .config import SUBTITLE_FORMAT

class FileNameListView(QWidget):
    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)
    
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

        self.widget_table = QWidget()
        self.hBoxLayout = QHBoxLayout(self.widget_table)
        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)
        self.setupUI()

        self.FileNameModle = QStringListModel()
        self.fileNameList.setModel(self.FileNameModle)

        self.avDataRootDir = r"./"
        self.avFileList = self.FileNameModle.stringList()
        self.result_faster_whisper = []

        StyleSheet.FILE_LIST.apply(self)
        self.SignalAndSlotConnect()

        # 设置接受文件拖放
        self.setAcceptDrops(True)


    def testFileExitedAndNotSubtitle(self, fileNameList):
        files_exist = [os.path.exists(file) for file in fileNameList]
        if not all(files_exist):
            ignore_file = [file for file in fileNameList if not os.path.exists(file)]
            print(self.__tr("存在无效文件："))
            new_line = "\n                    "
            print(f"  Error FilesName : {new_line.join(ignore_file)}")
            new_line = "\n                "
            print(f"  ignore files: {new_line.join(ignore_file)}")
            fileNameList = [file for file in fileNameList if os.path.exists(file)]

            # TODO: self.parent().parent().parent().parent().parent() is monkey code , 
            # it should be replaced by a signal-slot system
            InfoBar.info(
                title=self.__tr("剔除文件")
                , content=self.__tr("存在无效文件，已剔除\n") + "\n".join(ignore_file)
                , isClosable=False
                , duration=2000
                , position=InfoBarPosition.TOP_RIGHT
                , parent=self.parent().parent().parent().parent().parent() # TODO: monkey code 
            )
        
        # 忽略掉输入文件中可能存在的所有的字幕文件
        files = [file for file in fileNameList if file.split(".")[-1].upper() not in SUBTITLE_FORMAT]
        if ingnore_files := [file for file in fileNameList if file.split(".")[-1].upper() in SUBTITLE_FORMAT]:
            new_line = "\n              "
            print(f"ignore files: {new_line.join(ingnore_files)}")

            # TODO: self.parent().parent().parent().parent().parent() is monkey code , 
            # it should be replaced by a signal-slot system
            InfoBar.info(
                title=self.__tr("剔除文件")
                , content=self.__tr("已知的字幕格式文件已忽略\n") + "\n".join(ingnore_files)
                , isClosable=False
                , duration=2000
                , position=InfoBarPosition.TOP_RIGHT
                , parent=self.parent().parent().parent().parent().parent() # TODO: monkey code 
            )
            # print(self.parent().parent().parent().parent().parent())

        return files

    def addFileNamesToListWidget(self):
        fileNames, _ = QFileDialog.getOpenFileNames(self, self.__tr("选择音频文件"), self.avDataRootDir, "All file type(*.*);;Wave file(*.wav);;MPEG 4(*.mp4)")
        
        if fileNames is None or len(fileNames) == 0:
            return

        self.setFileNameListToDataModel(fileNames)
        
    def setFileNameListToDataModel(self,fileNames)->None:
        baseDir, _ = os.path.split(fileNames[0])
        self.avDataRootDir = baseDir

        fileNames = self.testFileExitedAndNotSubtitle(fileNames)

        file_ignored = []
        self.avFileList = self.FileNameModle.stringList()
        for file in fileNames:
            # 获取已存在于列表中的全部文件名
            
            if file in self.avFileList:
                file_ignored.append(file)
                print(f"Exited File: {file}")
                continue
            
            self.avFileList.append(file)

        self.FileNameModle.setStringList(self.avFileList)

        # TODO: monkey code
        if len(file_ignored) > 0:
            InfoBar.info(
                    title=self.__tr("忽略已存在的文件")
                    , content=self.__tr("重复添加的文件将被忽略：\n") + "\n".join(file_ignored)
                    , isClosable=False
                    , duration=2000
                    , parent=self.parent().parent().parent().parent().parent() 
                )    
        
    def removeFileNameFromListWidget(self):

        # 获取当前选中的项目
        fileNameListWidget = self.fileNameList
        selected_indexes = fileNameListWidget.selectedIndexes()

        # 从数据模型中移除项目
        for index in selected_indexes:
            self.FileNameModle.removeRow(index.row())
        
        # fileNameListWidget._setSelectedRows(0)

        # 重新设置当前的显示数据 由于之前已经进行过数据项目绑定 所以这里应该可以省略 
        fileNameListWidget.setModel(self.FileNameModle)
        # 同步数据到列表项
        self.avFileList = self.FileNameModle.stringList()

    def addWidget(self, widget:QWidget):
        self.vBoxLayout.addWidget(widget)
    def addLayout(self, layout):
        self.vBoxLayout.addLayout(layout)

    def setupUI(self):
        
        label_1 = QLabel()
        label_1.setText(self.tr("音视频文件列表"))
        label_1.setFixedHeight(20)
        self.addWidget(label_1)

        self.addWidget(self.widget_table)
        self.widget_table.setLayout(self.hBoxLayout)
        self.widget_table.setObjectName("widgetTable")

        self.fileNameListContain = QWidget()
        self.hBoxLayout.addWidget(self.fileNameListContain)
        self.fileNameListContain.setObjectName("fileNameListContain")
        
        self.fileNameListContainLayout = QHBoxLayout(self.fileNameListContain)
        self.fileNameListContain.setLayout(self.fileNameListContainLayout)

        self.fileNameList = ListView()
        self.fileNameList.setFixedHeight(275)
        self.fileNameList.setSelectionMode(QListView.ExtendedSelection)
        self.fileNameListContainLayout.addWidget(self.fileNameList)

        
        self.fileButtonLayout = QVBoxLayout()
        self.fileButtonLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.hBoxLayout.addLayout(self.fileButtonLayout)

        self.addFileButton = ToolButton()
        self.addFileButton.setIcon(FluentIcon.ADD)
        self.fileButtonLayout.addWidget(self.addFileButton)

        self.removeFileButton = ToolButton()
        self.removeFileButton.setIcon(FluentIcon.REMOVE)
        self.fileButtonLayout.addWidget(self.removeFileButton)
    
    def SignalAndSlotConnect(self):
        self.addFileButton.clicked.connect(self.addFileNamesToListWidget)
        self.removeFileButton.clicked.connect(self.removeFileNameFromListWidget)
    
    # ===========================================================================================================
    def dragEnterEvent(self, event: PySide6.QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()  # 接受拖放事件
        else:
            event.ignore()
        
    def dropEvent(self, a0: PySide6.QtGui.QDropEvent) -> None:
        """
        重写鼠标放开事件
        :param a0:事件
        :return:None
        """
        # 获取拖拽进来的所有文件的路径
        urls = a0.mimeData().urls()
        
        fileNames = [url.toLocalFile() for url in urls]
        self.setFileNameListToDataModel(fileNames)
        