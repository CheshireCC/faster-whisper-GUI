# coding:utf-8

import os
from threading import Thread

import av

from PySide6.QtCore import (QStringListModel, Qt, QCoreApplication, Signal)

from PySide6.QtGui import (QClipboard, QDropEvent, QDragEnterEvent)

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
                            # , InfoBar
                            # , InfoBarPosition
                        )

from .style_sheet import StyleSheet
from .config import SUBTITLE_FORMAT
from typing import TypedDict

class ignore_files_info(TypedDict):
    ignore_files: list[str]
    ignore_reason: str

class FileNameListView(QWidget):
    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)
    
    ignore_files_signal = Signal(ignore_files_info)

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

        self.widget_table = QWidget()
        self.hBoxLayout = QHBoxLayout(self.widget_table)
        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)
        self.setupUI()

        self.FileNameModle = QStringListModel()
        self.FileNameModle.setStringList([""])
        self.fileNameList.setModel(self.FileNameModle)

        self.avDataRootDir = r"./"
        self.avFileList = self.FileNameModle.stringList()
        self.result_faster_whisper = []

        StyleSheet.FILE_LIST.apply(self)
        self.SignalAndSlotConnect()

        # 设置接受文件拖放
        self.setAcceptDrops(True)

    def testFileExitedAndNotSubtitle(self, fileNameList) -> list[str]:
        files_exist = [os.path.exists(file) for file in fileNameList]

        if not all(files_exist):
            ignore_file = [file for file in fileNameList if not os.path.exists(file)]
            print(self.__tr("存在无效文件："))
            new_line = "\n                    "
            print(f"  Error FilesName : {new_line.join(ignore_file)}")
            new_line = "\n                "
            print(f"  ignore files: {new_line.join(ignore_file)}")
            fileNameList = [file for file in fileNameList if os.path.exists(file)]

            ifi = ignore_files_info(ignore_files=ignore_file, ignore_reason=self.__tr("存在无效文件，已剔除"))
            self.ignore_files_signal.emit(ifi)

            # TODO: self.parent().parent().parent().parent().parent() is monkey code , 
            # it should be replaced by a signal-slot system
            # InfoBar.info(
            #     title=self.__tr("剔除文件")
            #     , content=self.__tr("存在无效文件，已剔除\n") + "\n".join(ignore_file)
            #     , isClosable=False
            #     , duration=2000
            #     , position=InfoBarPosition.TOP_RIGHT
            #     , parent=self.parent().parent().parent().parent().parent() # TODO: monkey code 
            # )
        
        # 忽略掉输入文件中可能存在的所有的字幕文件
        files = [file for file in fileNameList if file.split(".")[-1].upper() not in SUBTITLE_FORMAT]
        ignore_files = [file for file in fileNameList if file.split(".")[-1].upper() in SUBTITLE_FORMAT]
        
        if len(ignore_files) > 0:
            new_line = "\n              "
            print(f"ignore files: {new_line.join(ignore_files)}")

            ifi = ignore_files_info(ignore_files=ignore_files,ignore_reason=self.__tr("已知的字幕格式文件已忽略："))
            self.ignore_files_signal.emit(ifi)
            # TODO: self.parent().parent().parent().parent().parent() is monkey code , 
            # it should be replaced by a signal-slot system
            # InfoBar.info(
            #     title=self.__tr("剔除文件")
            #     , content=self.__tr("已知的字幕格式文件已忽略\n") + "\n".join(ignore_files)
            #     , isClosable=False
            #     , duration=2000
            #     , position=InfoBarPosition.TOP_RIGHT
            #     , parent=self.parent().parent().parent().parent().parent() # TODO: monkey code 
            # )
            # print(self.parent().parent().parent().parent().parent())

        return files

    def addFileNamesToListWidget(self):

        fileNames, _ = QFileDialog.getOpenFileNames(self, self.__tr("选择音频文件"), self.avDataRootDir, "All file type(*.*);;Wave file(*.wav);;MPEG 4(*.mp4)")
        
        if fileNames is None or len(fileNames) == 0:
            return
        thread_: Thread = Thread(target=self.setFileNameListToDataModel, args=(fileNames,),daemon=True)
        thread_.start()
        # self.setFileNameListToDataModel(fileNames)
    
    def testFileWithAudioTrackOrNot(self, fileNames:list[str]) -> list[str]:
        
        fileNames_ = []
        ignoreFile = []
        for fileName in fileNames:
            cont = None
            try:
                cont = av.open(fileName, metadata_errors="ignore")
            except Exception as e:
                print(f"InvalidDataError : {fileName} \nerror:{str(e)}")
                ignoreFile.append(fileName)
            
            if cont is not None:
                for s in cont.streams:
                    if s.codec_context.type == 'audio':
                        stream_ = s
                        break
                    else:
                        stream_ = None
                
                if stream_ is None :
                    ignoreFile.append(fileName)
            
                else:
                    fileNames_.append(fileName)
                
                cont.close()
                
        if len(ignoreFile) > 0:
            ifi = ignore_files_info(ignore_files=ignoreFile, ignore_reason=self.__tr("不包含音频流的文件将被忽略："))
            self.ignore_files_signal.emit(ifi)

        # TODO: monkey code
        # if len(ignoreFile) > 0:
        #     InfoBar.info(
        #             title=self.__tr("忽略无效文件")
        #             , content=self.__tr("不包含音频流的文件将被忽略：\n") + "\n".join(ignoreFile)
        #             , isClosable=False
        #             , duration=2000
        #             , parent=self.parent().parent().parent().parent().parent() 
        #         )    

        return fileNames_


    def setFileNameListToDataModel(self, fileNames)->None:
        baseDir, _ = os.path.split(fileNames[0])
        self.avDataRootDir = baseDir

        fileNames = self.testFileExitedAndNotSubtitle(fileNames)
        fileNames = self.testFileWithAudioTrackOrNot(fileNames)

        file_ignored = []
        self.avFileList = self.FileNameModle.stringList()
        for file in fileNames:
            # 获取已存在于列表中的全部文件名
            
            if file in self.avFileList:
                file_ignored.append(file)
                print(f"Exited File: {file}")
                continue
            
            self.avFileList.append(file)
        self.avFileList = [file for file in self.avFileList if file != ""]
        self.FileNameModle.setStringList(self.avFileList)
        
        if len(file_ignored) > 0:
            ifi = ignore_files_info(ignore_files=file_ignored, ignore_reason=self.__tr("重复添加的文件将被忽略："))
            self.ignore_files_signal.emit(ifi)

        # TODO: monkey code
        # if len(file_ignored) > 0:
        #     InfoBar.info(
        #             title=self.__tr("忽略已存在的文件")
        #             , content=self.__tr("重复添加的文件将被忽略：\n") + "\n".join(file_ignored)
        #             , isClosable=False
        #             , duration=2000
        #             , parent=self.parent().parent().parent().parent().parent() 
        #         )    
        

    def removeFileNameFromListWidget(self):

        # 获取当前选中的项目
        fileNameListWidget = self.fileNameList
        selected_indexes = fileNameListWidget.selectedIndexes()

        while(len(selected_indexes) != 0):
            self.removeSingleFileNameFromListWidget(selected_indexes[0])
            selected_indexes = fileNameListWidget.selectedIndexes()

        # 同步数据到列表项
        self.avFileList = self.FileNameModle.stringList()
        if self.avFileList == []:
            self.avFileList.append("")
            
    def removeSingleFileNameFromListWidget(self, index):

        self.FileNameModle.removeRow(index.row())

        # 重新设置当前的显示数据 由于之前已经进行过数据项目绑定 所以这里应该可以省略 
        # self.fileNameList.setModel(self.FileNameModle)
        

    def clearFileNameListWidget(self):
        self.avFileList = [""]
        self.FileNameModle.setStringList(self.avFileList)
        # self.fileNameList.setModel(self.FileNameModle)
        

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

        self.clearFilesButton = ToolButton()
        self.clearFilesButton.setIcon(FluentIcon.DELETE)
        self.fileButtonLayout.addWidget(self.clearFilesButton)
    
    def SignalAndSlotConnect(self):
        self.addFileButton.clicked.connect(self.addFileNamesToListWidget)
        self.removeFileButton.clicked.connect(self.removeFileNameFromListWidget)
        self.clearFilesButton.clicked.connect( self.clearFileNameListWidget)
    
    # ===========================================================================================================
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            # acceptProposedAction 将导致 Nuitka 编译之后 拖放功能失效
            # event.acceptProposedAction()  # 接受拖放事件
            event.accept()
        else:
            event.ignore()

    def urlsToFileNames(self, urls):
        """
        从 QUrl 列表获取文件名 并递归获取子文件夹内的文件名的函数
        :param urls:QUrl 对象列表 List[QUrl]
        """
        fileNames_ = [url.toLocalFile() for url in urls]
        fileNames = [url for url in fileNames_ if os.path.isfile(url)]

        folderPaths = [url for url in fileNames_ if os.path.isdir(url)]
        if len(folderPaths):
            for folderPath in folderPaths:
                fileNames.extend(self.searchFilesFromFolder(folderPath))
        
        return fileNames
    
    def dropEvent(self, a0: QDropEvent) -> None:
        """
        重写鼠标放开事件
        :param a0:事件
        :return:None
        """
        # 获取拖拽进来的所有文件的路径
        urls = a0.mimeData().urls()

        fileNames = self.urlsToFileNames(urls)

        if len(fileNames):
            self.setFileNameListToDataModel(fileNames)
        else:
            pass

    def searchFilesFromFolder(self, folderPath: str):
        """
        从文件夹中获取文件名，并递归获取子文件夹内文件名的函数
        :param folderPath: 文件路径 str
        """
        fileNames = []
        if not os.path.isdir(folderPath):
            return fileNames
        fileList = os.listdir(folderPath)

        fileNames = [os.path.join(folderPath, file) for file in fileList if os.path.isfile(os.path.join(folderPath, file))]

        folderPaths = [os.path.join(folderPath, file) for file in fileList if os.path.isdir(os.path.join(folderPath, file))]

        for folderPath in folderPaths:
            fileNames.extend(self.searchFilesFromFolder(folderPath))

        return fileNames

    def keyPressEvent(self, event):
        # Ctrl+V键被按下 查找文件名 并尝试添加到文件名列表
        # print("Ctrl+V键被按下")
        if event.key() == Qt.Key.Key_V and event.modifiers() & Qt.KeyboardModifiers.ControlModifier:
            self.pasteFileNamesToFileNameList()
        else:
            super().keyPressEvent(event)
        
    def pasteFileNamesToFileNameList(self):
        
        # 获取剪贴板中的文本
        if QClipboard().mimeData().hasUrls():
            # 如果有文本，获取文本并显示文件选择器
            urls = QClipboard().mimeData().urls()
            fileNameList = self.urlsToFileNames(urls)
            
            self.setFileNameListToDataModel(fileNameList)
    
