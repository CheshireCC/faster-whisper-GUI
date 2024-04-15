# coding:utf-8

from PySide6.QtCore import QAbstractTableModel, QCoreApplication, QSize, Qt
# from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit
from typing import List
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication
from faster_whisper import  Word
from qfluentwidgets import MessageBox, isDarkTheme

from .seg_ment import segment_Transcribe
from .util import HMSToSeconds, secondsToHMS
from .config import tableItem_dark_warning_BackGround_color, tableItem_light_warning_BackGround_color

# 自定义数据模型，用于在表格中显示数据
class TableModel(QAbstractTableModel):
    tdwbc = QColor.fromString(tableItem_dark_warning_BackGround_color)
    tlwbs = QColor.fromString(tableItem_light_warning_BackGround_color)

    def __init__(self, data:List[tuple]):
        super(TableModel, self).__init__()
        self._data = data
    
    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)
    

    def resetData(self, data):
        self._data = data
        # self.dataChanged.emit()

    # 获取数据的方法
    def data(self, index, role):
        row, column = index.row(), index.column()
        data:segment_Transcribe = self._data[row]

        # 设置数据内容
        if role == Qt.ItemDataRole.DisplayRole:
            
            if column == 0:
                value = secondsToHMS(data.start)
            elif column == 1:
                value = secondsToHMS(data.end)
            elif column == 2:
                value = data.speaker if data.speaker is not None else ""
            elif column == 3:
                try:
                    value =  data.text
                except AttributeError:
                    value = ""
            elif column == 4:
                value = ";".join([f"<{word.start}>{word.word}<{word.end}>" for word in data.words]) if len(data.words) > 0 else ""
            value.encode('utf-8').decode('utf-8')
            return value

        if role == Qt.ItemDataRole.BackgroundRole:
            if row != 0:
                # 间隔时间小于 0.4 s
                # if data.start - self._data[row-1].end < 0.4:
                #     return Qt.GlobalColor.red

                # 重叠字幕
                if data.start < self._data[row-1].end:
                    if isDarkTheme():
                        return self.tdwbc
                    else:
                        return self.tlwbs
                
                # 持续时间小于 1 s 的过短字幕
                elif data.end - data.start < 1.0:
                    if isDarkTheme():
                        return self.tdwbc
                    else:
                        return self.tlwbs
                    
                else:
                    # return QApplication.palette().color(Qt.Palette.Base)
                    pass

    # 使数据可编辑
    def setData(self, index, value, role):
        if role == Qt.EditRole:
            row, column = index.row(), index.column()
            _data = self._data[row]

            try:
                if column == 0:
                    self._data[row].start = HMSToSeconds(value)
                elif column == 1:
                    self._data[row].end = HMSToSeconds(value)
                elif column == 2:
                    if value != "":
                        if self._data[row].speaker != value:
                            temp_data_speaker = self._data[row].speaker
                            self._data[row].speaker = value
                            # 批量修改所有相同说话人
                            msgb = MessageBox(self.__tr("提示"), self.__tr("是否修改所有相同说话人？"),QApplication.activeWindow())
                            # msgb.show()
                            if msgb.exec():
                                for data in self._data:
                                    if data.speaker is not None and data.speaker != "" and data.speaker == temp_data_speaker:
                                        data.speaker = value

                            # self._data[row].speaker = value

                elif column == 3:
                    if value != "":
                            self._data[row].text = value
                    else:
                        return False
                    
                elif column == 4:
                    if value != "":
                        words_list = []
                        text = ""
                        try:
                            words = value.split(";")
                            # print(words)
                            for word in words:
                                temp = word.split("<")
                                # print(temp)
                                end_time = float(temp[-1].split(">")[0])
                                start_time = float(temp[1].split(">")[0])
                                word_text = temp[1].split(">")[-1]
                                text += word_text
                                word_ = Word(start=start_time, end=end_time, word=word_text, probability=1.0)
                                words_list.append(word_)
                            
                            # print(text)
                            self._data[row].words = words_list
                            self._data[row].text = text
                        except Exception as e:
                            print(f"edit words-level timestample error:{e}")
                            return False
                    else:
                        return False
                    
                self.dataChanged.emit(index, index)
                return True
            except ValueError:
                self._data[row] = _data
                return False
        return False

    def flags(self, index=None):
        return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        return 5

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return ["start(s)", "end(s)", "speaker", "text", "words"][section]
            elif orientation == Qt.Orientation.Vertical:
                try:
                    index = range(1, self.rowCount()+1)[section]
                except:
                    index = None
                    
                return index
                
            