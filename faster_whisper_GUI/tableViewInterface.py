# coding:utf-8

import time
from PySide6.QtCore import (QCoreApplication, 
                            QModelIndex, 
                            Qt, 
                            Signal
                        )

from PySide6.QtGui import (
                            QBrush,
                            QPalette, 
                            QAction
                        )

from PySide6.QtWidgets import (
                                QApplication,
                                QFrame,
                                QHBoxLayout,
                                QHeaderView,
                                QSizePolicy,
                                QStackedWidget,
                                QStyleOptionViewItem,
                                QTableView,
                                QWidget,
                                QVBoxLayout
                            )

from qfluentwidgets import (
                            LineEdit
                            , CheckBox
                            , BodyLabel
                            , StrongBodyLabel
                            , SpinBox
                            , TabBar
                            , TabCloseButtonDisplayMode
                            , ComboBox
                            , TableView
                            , isDarkTheme
                            , TableItemDelegate
                            , HorizontalSeparator
                            , Router
                            , RoundMenu ,
                            MessageBoxBase,
                            SubtitleLabel,
                        )

from .style_sheet import StyleSheet
from .util import outputWithDateTime


class CustomTableItemDelegate(TableItemDelegate):
    """ Custom table item delegate """
    def __init__(self, parent: QTableView=None):
        super().__init__(parent)
    
    # def sizeHint(self, option, index):
    #     row, column = index.row(), index.column()
    #     size = super().sizeHint(option, index)
    #     size.setHeight(35)
    #     if column == 0 or column == 1:
    #         size.setWidth(115)
    #     return size

    # def paint(self, painter, option, index):
    #     if index.column() in [0,1,2]:
    #         option.displayAlignment = Qt.AlignCenter
    #     super().paint(painter, option, index)
        
    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)

        # 设置单元格的对齐方式
        if index.column() in [0,1,2]:
            option.displayAlignment = Qt.AlignCenter

        if index.column() == 1:
            
            if isDarkTheme():
                option.palette.setColor(QPalette.Text, Qt.GlobalColor.cyan)
                option.palette.setColor(QPalette.HighlightedText, Qt.GlobalColor.cyan)
                
            else:
                option.palette.setColor(QPalette.Text, Qt.GlobalColor.blue)
                option.palette.setColor(QPalette.HighlightedText, Qt.GlobalColor.blue)
            
            # option.palette.setBackground(QBrush(Qt.GlobalColor.blue))
        
        elif index.column() == 0:
            if isDarkTheme():
                option.palette.setColor(QPalette.Text, Qt.GlobalColor.red)
                option.palette.setColor(QPalette.HighlightedText, Qt.GlobalColor.red)
            else:
                option.palette.setColor(QPalette.Text, Qt.GlobalColor.magenta)
                option.palette.setColor(QPalette.HighlightedText, Qt.GlobalColor.magenta)
            
        
    # 设置编辑框的提示内容为原本的内容
    def createEditor(self, parent, option, index):
        value = index.model().data(index, Qt.DisplayRole)
        option.text = str(value)
        editor:LineEdit = super().createEditor(parent, option, index)
        editor.setPlaceholderText(str(value))
        return editor

    
    # 使编辑框保留编辑之前的值
    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole) or ""
        editor.setText(str(text))
        

class TabInterface(QWidget):
    """ Tab interface """

    signal_delete_table = Signal(str)
    signal_addTable_request = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.outputWithDateTime = outputWithDateTime
        
        self.tabCount = 1

        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)
        self.controlPanel = QFrame(self)

        self.movableCheckBox = CheckBox(self.tr('标签移动'), self)
        self.scrollableCheckBox = CheckBox(self.tr('标签滚动'), self)
        self.shadowEnabledCheckBox = CheckBox(self.tr('标签阴影'), self)
        self.tabMaxWidthLabel = BodyLabel(self.tr('最大宽度'), self)
        self.tabMaxWidthSpinBox = SpinBox(self)
        self.closeDisplayModeLabel = BodyLabel(self.tr('关闭按钮显示模式'), self)
        self.closeDisplayModeComboBox = ComboBox(self)

        self.controlLabel_table = StrongBodyLabel(self.tr("表格样式控制"))

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        self.router = Router()


        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.initLayout()

        self.shadowEnabledCheckBox.setChecked(True)

        self.tabMaxWidthSpinBox.setRange(60, 600)
        self.tabMaxWidthSpinBox.setValue(self.tabBar.tabMaximumWidth())

        self.closeDisplayModeComboBox.addItem(self.tr('始终显示'), userData=TabCloseButtonDisplayMode.ALWAYS)
        self.closeDisplayModeComboBox.addItem(self.tr('进入时显示'), userData=TabCloseButtonDisplayMode.ON_HOVER)
        self.closeDisplayModeComboBox.addItem(self.tr('从不显示'), userData=TabCloseButtonDisplayMode.NEVER)
        self.closeDisplayModeComboBox.currentIndexChanged.connect(self.onDisplayModeChanged)
        self.closeDisplayModeComboBox.setCurrentIndex(2)
        self.onDisplayModeChanged(2)

        self.controlPanel.setObjectName('controlPanel')
        self.tabView.setObjectName("tabView")
        StyleSheet.TAB_INTERFSCE.apply(self)

        self.connectSignalToSlot()

    def connectSignalToSlot(self):
        self.movableCheckBox.stateChanged.connect(lambda: self.tabBar.setMovable(self.movableCheckBox.isChecked()))
        self.scrollableCheckBox.stateChanged.connect(lambda: self.tabBar.setScrollable(self.scrollableCheckBox.isChecked()))
        self.shadowEnabledCheckBox.stateChanged.connect(lambda: self.tabBar.setTabShadowEnabled(self.shadowEnabledCheckBox.isChecked()))
        self.tabMaxWidthSpinBox.valueChanged.connect(self.tabBar.setTabMaximumWidth)
        self.tabBar.tabCloseRequested.connect(self.removeTab)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        # self.tabBar.currentChanged()
        # self.tabBar.tabAddRequested.connect(self.addTab)
        

    def initLayout(self):
        self.tabBar.setTabMaximumWidth(200)

        self.setFixedHeight(280)
        self.controlPanel.setFixedWidth(220)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.panelLayout.setSpacing(8)
        self.panelLayout.setContentsMargins(14, 16, 14, 14)
        self.panelLayout.setAlignment(Qt.AlignTop)

        self.panelLayout.addWidget(self.controlLabel_table)
        self.panelLayout.addWidget(HorizontalSeparator())

        self.panelLayout.addWidget(self.movableCheckBox)
        self.panelLayout.addWidget(self.scrollableCheckBox)
        self.panelLayout.addWidget(self.shadowEnabledCheckBox)

        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.tabMaxWidthLabel)
        self.panelLayout.addWidget(self.tabMaxWidthSpinBox)

        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.closeDisplayModeLabel)
        self.panelLayout.addWidget(self.closeDisplayModeComboBox)
        
    def addSubInterface(self
                        , widget: QWidget = None
                        , objectName:str=""
                        , text:str=""
                        , icon=None
                    ):

        if widget is None:
            widget = CustomTableView()
            # widget.setObjectName(objectName)
            
        widget.setObjectName(objectName)
        
        # 设置填充可用空间
        widget.horizontalHeader().setStretchLastSection(True)

        # 设置单元格代理 重新设置编辑方式、单元格格式等等
        widget.setItemDelegate(CustomTableItemDelegate(widget))

        # 设置缩放策略
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # print(f"len_stack_items:{self.stackedWidget.count()}")
        
        # 移除旧的结果
        # for i in range(self.stackedWidget.count()):
        #     widget_i = self.stackedWidget.widget(i)
        #     if widget_i is None:
        #         self.stackedWidget.removeWidget(widget_i)
        #         break
        #     if widget_i.objectName() == objectName:
        #         print(f"excited objectName:{objectName}")
        #         self.stackedWidget.removeWidget(widget_i)
        #         break

        # 添加子分页
        print(f"addSubInterface:{objectName}")
        self.stackedWidget.addWidget(widget)

        # 已经存在的旧结果将会被清除
        items_rou = [item.routeKey() for item in self.tabBar.items]

        if objectName in items_rou:
            self.tabBar.removeTab(items_rou.index(objectName))

        # 添加子页标签
        self.tabBar.addTab(
                            routeKey=objectName,
                            text=text,
                            icon=icon,
                            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
                        )
        
        # 设置列宽
        widget.setColumnWidth(0,115)
        widget.setColumnWidth(1,115)
        widget.setColumnWidth(3,400)
        widget.setColumnWidth(2,110)
        widget.setColumnWidth(4,50)

        # 设置列宽适应内容
        widget.resizeColumnToContents(0)
        widget.resizeColumnToContents(1)
        widget.resizeColumnToContents(3)
        widget.resizeColumnToContents(2)
        
        # 设置行高度固定
        # widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

    def onDisplayModeChanged(self, index):
        mode = self.closeDisplayModeComboBox.itemData(index)
        self.tabBar.setCloseButtonDisplayMode(mode)

    def onCurrentIndexChanged(self, index):
        # print(f"currentTabIndexChangedTo:{index}")
        widget = self.stackedWidget.widget(index)
        if not widget:
            return
        
        self.tabBar.setCurrentTab(widget.objectName())
        # self.router.push(self.stackedWidget, widget.objectName())

    def removeTab(self, index):

        self.outputWithDateTime("deleteTable")
        
        item = self.tabBar.tabItem(index)
        print(f"removeTab: {item.routeKey()}")

        widget = self.stackedWidget.widget(index)
        
        print(f"removeTable:{widget.objectName()}")
        self.stackedWidget.removeWidget(widget)
        self.signal_delete_table.emit(item.routeKey())

        self.tabBar.removeTab(index)
        widget.deleteLater()

        if self.stackedWidget.count() == 0:
            print("all clear")


class CustomTableView(TableView):
    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)
    
    def __init__(self, parent=None):
        super(CustomTableView, self).__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.temp_speaker = ""
        self.temp_timestamp = ""

    def show_context_menu(self, position):
        index = self.indexAt(position)
        if index.isValid():

            indexs = self.selectedIndexes()
            rows = list(set([index.row() for index in indexs]))

            # rect = self.visualRect(index)
            
            # 显示单行内容菜单
            menu = RoundMenu(self)

            copy_action = QAction(self.__tr("复制字幕"), self)
            # copy_action.setShortcut("Ctrl+C")
            menu.addAction(copy_action)
            copy_action.triggered.connect(self.copy_all_content)

            copy_subtitle_action = QAction(self.__tr("复制字幕内容"), self)
            menu.addAction(copy_subtitle_action)
            copy_subtitle_action.triggered.connect(self.copy_subtitle_content)

            # 提前开始时间戳
            advance_start_time_action = QAction(self.__tr("提前开始时间戳"), self)
            menu.addAction(advance_start_time_action)
            advance_start_time_action.triggered.connect(self.advance_start_time_action)

            # 延后开始时间戳
            delay_start_time_action = QAction(self.__tr("延后开始时间戳"), self)
            menu.addAction(delay_start_time_action)
            delay_start_time_action.triggered.connect(self.delay_start_time_action)

            # 提前结束时间戳
            advance_end_time_action = QAction(self.__tr("提前结束时间戳"), self)
            menu.addAction(advance_end_time_action)
            advance_end_time_action.triggered.connect(self.advance_end_time_action)

            # 延后结束时间戳
            delay_end_time_action = QAction(self.__tr("延后结束时间戳"), self)
            menu.addAction(delay_end_time_action)
            delay_end_time_action.triggered.connect(self.delay_end_time_action)

            delete_subtitles_line = QAction(self.__tr("删除字幕行"), self)
            menu.addAction(delete_subtitles_line)
            delete_subtitles_line.triggered.connect(self.delete_subtitles_line)
            
            if len(rows) > 1:
                # 显示多行内容菜单

                # 修改说话人
                set_speaker_action = QAction(self.__tr("设置说话人"), self)
                menu.addAction(set_speaker_action)
                set_speaker_action.triggered.connect(self.open_set_speaker_dialog)

                # 合并字幕行
                merge_subtitel_line_action = QAction(self.__tr("合并字幕行"), self)
                menu.addAction(merge_subtitel_line_action)
                merge_subtitel_line_action.triggered.connect(self.merge_subtitles)

            menu.exec(self.mapToGlobal(position))
    
    def delete_subtitles_line(self):
        indexs = self.selectedIndexes()

        rows = list(set([index.row() for index in indexs]))
        
        items = []
        for i in rows:
            items.append(self.model()._data[i])
        for item in items:
            self.model()._data.remove(item)
        
    
    def advance_start_time_action(self):
        self.adjust_time_stamp("advance", "start")
    
    def delay_start_time_action(self):
        self.adjust_time_stamp("delay", "start")

    def advance_end_time_action(self):
        self.adjust_time_stamp("advance", "end")

    def delay_end_time_action(self):
        self.adjust_time_stamp("delay", "end")

    def adjust_time_stamp(self, flag:str, position:str):

        esmb = CustomMessageBox(
                                    self.tr('调整时间戳'),
                                    self.tr('输入调整时长(ms)'),
                                    QApplication.activeWindow()
                                )
        
        esmb.accept_value_signal.connect(self.set_temp_timestamp)

        if not esmb.exec():
            return

        if not self.temp_timestamp.isdigit():
            return

        time_stamp_adjust = float(self.temp_timestamp)/1000.0

        indexs = self.selectedIndexes()
        rows = list(set([index.row() for index in indexs]))

        for row in rows:
            # 获取当前行数据
            subtitle_obj = self.model()._data[row]

            if position == "start":
                
                # 获取当前行开始时间戳
                start_time = subtitle_obj.start
                if flag == "advance":
                    start_time -= time_stamp_adjust
                elif flag == "delay":
                    start_time += time_stamp_adjust

                # 设置当前行开始时间戳
                subtitle_obj.start = start_time

            elif position == "end":
                # 获取当前行结束时间戳
                end_time = subtitle_obj.end
                if flag == "advance":
                    end_time -= time_stamp_adjust
                elif flag == "delay":
                    end_time += time_stamp_adjust
                
                # 设置当前行结束时间戳
                subtitle_obj.end = end_time

            # self.model().setData(self.model().index(row, 0), subtitle_obj)
        
    def set_temp_timestamp(self, value):
        self.temp_timestamp = value
        
    # 批量合并字幕行
    def merge_subtitles(self):
        indexs = self.selectedIndexes()
        if len(indexs) < 2:
            return

        rows = list(set([index.row() for index in indexs]))
        rows.sort()

        merge_line = []

        for i in range(len(rows)-1):
            
            row1 = rows[i]
            row2 = rows[i+1]

            if row2 == row1+1:
                self.merge_subtitle_lines(row1, row2)
            else:
                merge_line.append(row1)
            
            if i+1 == len(rows)-1:
                merge_line.append(row2)

        subtitle_obj = []
        for row in rows:
            if row not in merge_line:
                subtitle_obj.append(self.model()._data[row])

        for obj in subtitle_obj:
            self.model()._data.remove(obj)
        
        # self.setCurrentRow(-1)

    def merge_subtitle_lines(self, row1, row2):
        # 合并字幕行
        subtitle_line1 = self.model()._data[row1]
        subtitle_line2 = self.model()._data[row2]

        subtitle_line2.start = subtitle_line1.start
        subtitle_line2.text = subtitle_line1.text + f",{subtitle_line2.text}"

        subtitle_line2.words = subtitle_line1.words + subtitle_line2.words

        subtitle_line2.speaker = None

        # self.model().setData(self.model.index(row2, 0), subtitle_line2)
        # self.model.removeRows(row2, 1)

    def set_temp_speaker(self, speaker):
        self.temp_speaker = speaker
        # print(f"input speaker:{self.temp_speaker}")

    def open_set_speaker_dialog(self):

        indexs = self.selectedIndexes()
        print(len(indexs))

        esmb = CustomMessageBox(
                                self.tr('说话人'),
                                self.tr('输入说话人'),
                                parent= QApplication.activeWindow()
                            )
        
        esmb.accept_value_signal.connect(self.set_temp_speaker)
        # time.sleep(1000)
        if esmb.exec():
            # print(f"temp speaker:{self.temp_speaker}")
            self.set_speaker(indexs)
            # self.model().refresh()

    def set_speaker(self, indexs):

        # 获取唯一行号为列表
        rows = list(set(index.row() for index in indexs))
        for row in rows:
            self.model()._data[row].speaker = self.temp_speaker

    def copy_all_content(self):
        indexs = self.selectedIndexes()
        content = ""

        rows = []
        for index in indexs:
            if index.row() not in rows:
                rows.append(index.row())

        for row in rows:
            if self.model().index(row,2).data():
                content += f"{row+1}\n{self.model().index(row, 0).data()} --> {self.model().index(row, 1).data()}\n{self.model().index(row,2).data()}: {self.model().index(row, 3).data()}\n\n"
            else:
                content += f"{row+1}\n{self.model().index(row, 0).data()} --> {self.model().index(row, 1).data()}\n{self.model().index(row, 3).data()}\n\n"

        # for column in range(self.model().columnCount()-1):
        #     row_data.append(self.model().index(index.row(), column).data())
            
        QApplication.clipboard().setText(content)

    def copy_subtitle_content(self):
        
        indexs = self.selectedIndexes()
        # index = self.currentIndex()
        content = ""

        rows = []
        for index in indexs:
            if index.row() not in rows:
                rows.append(index.row())

        for row in rows:
            content += f"{self.model().index(row, 3).data()}\n"
        # content = index.data()
        # content = self.model().index(index.row(), 2).data()
        QApplication.clipboard().setText(content)



class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    accept_value_signal = Signal(str)

    def __init__(self, title:str, text:str, parent=None):
        super().__init__(parent)
        self.value = ""

        self.titleLabel = SubtitleLabel(title, self)
        self.speakerLineEdit:LineEdit = LineEdit(self)

        self.speakerLineEdit.setPlaceholderText(text)
        self.speakerLineEdit.setClearButtonEnabled(True)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.speakerLineEdit)

        # change the text of button
        self.yesButton.setText(self.tr('确定'))
        self.cancelButton.setText(self.tr('取消'))

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.speakerLineEdit.textChanged.connect(self._validateUrl)

        self.yesButton.setDefault(True)

        # self.hideYesButton()
        self.speakerLineEdit.setFocus()
        
        

    def _validateUrl(self, text:str):
        # print("text:",text)
        self.yesButton.setEnabled(text != "")
        self.value=text
        self.accept_value_signal.emit(self.value)

    def exec(self) -> int:
        # print("value:",self.value)
        self.value = self.speakerLineEdit.text()
        self.accept_value_signal.emit(self.value)
        return super().exec()

'''
class EditTimeStampMessageBox(MessageBoxBase):
    """ Custom message box """

    accept_time_stamp_signal = Signal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = ""

        self.titleLabel = SubtitleLabel(self.tr('调整时间戳'), self)
        self.speakerLineEdit = LineEdit(self)

        self.speakerLineEdit.setPlaceholderText(self.tr('输入调整时长(ms)'))
        self.speakerLineEdit.setClearButtonEnabled(True)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.speakerLineEdit)

        # change the text of button
        self.yesButton.setText(self.tr('确定'))
        self.cancelButton.setText(self.tr('取消'))

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.speakerLineEdit.textChanged.connect(self._validateUrl)

        self.yesButton.setDefault(True)

        # self.hideYesButton()

    def _validateUrl(self, text:str):
        # print("text:",text)
        self.yesButton.setEnabled(text != "" and text.isdigit())
        self.value=text
        self.accept_time_stamp_signal.emit(self.value)

    def exec(self) -> int:
        # print("value:",self.value)
        # self.value = self.speakerLineEdit.text()
        self.accept_time_stamp_signal.emit(self.value)
        return super().exec()
    


class EditSpeakerMessageBox(MessageBoxBase):
    """ Custom message box """

    accept_speaker_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = ""

        self.titleLabel = SubtitleLabel(self.tr('说话人'), self)
        self.speakerLineEdit = LineEdit(self)

        self.speakerLineEdit.setPlaceholderText(self.tr('输入说话人'))
        self.speakerLineEdit.setClearButtonEnabled(True)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.speakerLineEdit)

        # change the text of button
        self.yesButton.setText(self.tr('确定'))
        self.cancelButton.setText(self.tr('取消'))

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.speakerLineEdit.textChanged.connect(self._validateUrl)

        self.yesButton.setDefault(True)

        # self.hideYesButton()

    def _validateUrl(self, text):
        print("text:",text)
        self.yesButton.setEnabled(text != "")
        self.value=text
        self.accept_speaker_signal.emit(self.value)

    def exec(self) -> int:
        # print("value:",self.value)
        # self.value = self.speakerLineEdit.text()
        self.accept_speaker_signal.emit(self.value)
        return super().exec()
'''
    