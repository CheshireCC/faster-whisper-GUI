
from PySide6.QtCore import QAbstractTableModel, Qt
# from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit
from typing import List
from faster_whisper import  Word

from .seg_ment import segment_Transcribe
from .transcribe import secondsToHMS
from .util import HMSToSeconds

# 自定义数据模型，用于在表格中显示数据
class TableModel(QAbstractTableModel):
    def __init__(self, data:List[tuple]):
        super(TableModel, self).__init__()
        self._data = data
        

    def resetData(self, data):
        self._data = data
        # self.dataChanged.emit()

    # 获取数据的方法
    def data(self, index, role):
        if role == Qt.DisplayRole:
            row, column = index.row(), index.column()
            data:segment_Transcribe = self._data[row]
            if column == 0:
                value = secondsToHMS(data.start)
            elif column == 1:
                value = secondsToHMS(data.end)
            elif column == 2:
                try:
                    value = f"{data.speaker}:{data.text}" if data.speaker is not None else data.text
                except AttributeError:
                    value = data.text

            elif column == 3:
                value = ";".join([f"<{word.start}>{word.word}<{word.end}>" for word in data.words]) if len(data.words) > 0 else ""
            # print(type(value))
            value.encode('utf-8').decode('utf-8')
            return value
    
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
                        retxt = value.split(":")
                        if len(retxt) > 1:
                            if self._data[row].speaker != retxt[0]:
                                temp_data_speaker = self._data[row].speaker 
                                for data in self._data:
                                    if data.speaker is not None and data.speaker != "" and data.speaker == temp_data_speaker:
                                        data.speaker = retxt[0]
                            self._data[row].speaker = retxt[0]
                            self._data[row].text = ":".join(retxt[1:])
                        else:
                            self._data[row].text = value
                    else:
                        return False
                    
                elif column == 3:
                    if value != "":
                        words_list = []
                        text = ""
                        try:
                            words = value.split(";")
                            print(words)
                            for word in words:
                                temp = word.split("<")
                                print(temp)
                                end_time = float(temp[-1].split(">")[0])
                                start_time = float(temp[1].split(">")[0])
                                word_text = temp[1].split(">")[-1]
                                text += word_text
                                word_ = Word(start=start_time, end=end_time, word=word_text, probability=1.0)
                                words_list.append(word_)
                            
                            print(text)
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
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        return 4

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return ["start(s)", "end(s)", "text", "words"][section]
            elif orientation == Qt.Orientation.Vertical:
                try:
                    index = range(1, self.rowCount()+1)[section]
                except:
                    index = None
                    
                return index
                
            