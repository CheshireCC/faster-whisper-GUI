# coding:utf-8

from PySide6.QtCore import QModelIndex, Qt, Signal
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
                                QFrame,
                                QHBoxLayout,
                                QSizePolicy,
                                QStackedWidget
                                ,QStyleOptionViewItem
                                , QWidget
                                , QVBoxLayout
                            )

from qfluentwidgets import (
                            LineEdit, 
                            qrouter
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
                        )

from .style_sheet import StyleSheet

class CustomTableItemDelegate(TableItemDelegate):
    """ Custom table item delegate """

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)
        if index.column() == 1:
            if isDarkTheme():
                option.palette.setColor(QPalette.Text, Qt.GlobalColor.cyan)
                option.palette.setColor(QPalette.HighlightedText, Qt.cyan)
            else:
                option.palette.setColor(QPalette.Text, Qt.blue)
                option.palette.setColor(QPalette.HighlightedText, Qt.blue)
        
        elif index.column() == 0:
            if isDarkTheme():
                option.palette.setColor(QPalette.Text, Qt.red)
                option.palette.setColor(QPalette.HighlightedText, Qt.red)
            else:
                option.palette.setColor(QPalette.Text, Qt.magenta)
                option.palette.setColor(QPalette.HighlightedText, Qt.magenta)

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
        self.movableCheckBox.stateChanged.connect(
            lambda: self.tabBar.setMovable(self.movableCheckBox.isChecked()))
        self.scrollableCheckBox.stateChanged.connect(
            lambda: self.tabBar.setScrollable(self.scrollableCheckBox.isChecked()))
        self.shadowEnabledCheckBox.stateChanged.connect(
            lambda: self.tabBar.setTabShadowEnabled(self.shadowEnabledCheckBox.isChecked()))

        self.tabMaxWidthSpinBox.valueChanged.connect(self.tabBar.setTabMaximumWidth)

        # self.tabBar.tabAddRequested.connect(self.addTab)
        self.tabBar.tabCloseRequested.connect(self.removeTab)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

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
            widget = TableView()
            
        widget.setObjectName(objectName)

        # 设置缩放策略
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # 设置列宽
        widget.setColumnWidth(0,115)
        widget.setColumnWidth(1,115)
        widget.setColumnWidth(2,400)
        # widget.setColumnWidth(4,50)

        # 设置列宽适应内容
        # widget.resizeColumnsToContents()
        # widget.resizeColumnToContents(0)
        # widget.resizeColumnToContents(1)
        widget.resizeColumnToContents(3)
        # widget.resizeColumnToContents(2)
        
        # 设置填充可用空间
        widget.horizontalHeader().setStretchLastSection(True)

        # 设置单元格代理 重新设置编辑方式、单元格格式等等
        widget.setItemDelegate(CustomTableItemDelegate(widget))
        
        # 添加子分页
        self.stackedWidget.addWidget(widget)

        # 已经存在的旧结果将会被清除
        items = self.tabBar.items
        items_rou = [item.routeKey() for item in items]

        if objectName in items_rou:
            self.tabBar.removeTab(items_rou.index(objectName))

        # 添加子页标签
        self.tabBar.addTab(
                            routeKey=objectName,
                            text=text,
                            icon=icon,
                            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
                        )

    def onDisplayModeChanged(self, index):
        mode = self.closeDisplayModeComboBox.itemData(index)
        self.tabBar.setCloseButtonDisplayMode(mode)

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        if not widget:
            return
        
        self.tabBar.setCurrentTab(widget.objectName())
        self.router.push(self.stackedWidget, widget.objectName())

    def removeTab(self, index):
        
        item = self.tabBar.tabItem(index)
        self.signal_delete_table.emit(item.routeKey())

        widget = self.findChild(TableView, item.routeKey())

        self.stackedWidget.removeWidget(widget)
        self.tabBar.removeTab(index)
        widget.deleteLater()

        

