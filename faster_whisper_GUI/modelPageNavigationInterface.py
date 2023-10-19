from PySide6.QtCore import (QCoreApplication, Qt)

from PySide6.QtWidgets import (
                                QCompleter, 
                                QGridLayout, 
                                QHBoxLayout, 
                                QLabel, 
                                QStyle
                            )

from qfluentwidgets import (
                            ComboBox, 
                            RadioButton, 
                            PushButton, 
                            ToolButton, 
                            EditableComboBox, 
                            LineEdit 
                        )

from .navigationInterface import NavigationBaseInterface

from .config import (
                    Preciese_list
                    , Model_names
                    , Device_list
                )

class ModelNavigationInterface(NavigationBaseInterface):
    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)
    
    def __init__(self, parent=None):
        
        super().__init__(
                        title=self.__tr("Model")
                        , subtitle=self.__tr('加载本地模型或下载模型')
                        , parent=parent
                    )
        
        self.model_names = Model_names
        self.device_list = Device_list
        self.preciese_list = Preciese_list
        
        self.setObjectName('modelNavigationInterface')
        self.setupUI()

        self.SignalAndSlotConnect()
    
    def SignalAndSlotConnect(self):
        self.model_local_RadioButton.clicked.connect(self.setModelLocationLayout)
        self.model_online_RadioButton.clicked.connect(self.setModelLocationLayout)
        
    def setModelLocationLayout(self):
        num_widgets_layout = self.hBoxLayout_local_model.count()
            
        for i in range(num_widgets_layout):
            widget = self.hBoxLayout_local_model.itemAt(i).widget()
            widget.setEnabled(self.model_local_RadioButton.isChecked())
        
        num_widgets_layout = self.hBoxLayout_online_model.count()
            
        for i in range(num_widgets_layout):
            widget = self.hBoxLayout_online_model.itemAt(i).widget()
            widget.setEnabled(self.model_online_RadioButton.isChecked())

    def setupUI(self):

        model_local_RadioButton = RadioButton()
        model_local_RadioButton.setChecked(True)
        model_local_RadioButton.setText(self.__tr("使用本地模型"))
        model_local_RadioButton.setToolTip(self.__tr("本地模型需使用经过 CTranslate2 转换工具，从 OpenAI 模型格式转换而来的模型"))
        self.model_local_RadioButton = model_local_RadioButton
        self.addWidget(self.model_local_RadioButton)

        self.hBoxLayout_local_model = QHBoxLayout()
        self.addLayout(self.hBoxLayout_local_model)

        # 使用本地模型时添加相关控件到布局
        self.label_model_path = QLabel()
        self.label_model_path.setText(self.__tr("模型目录"))
        self.label_model_path.setObjectName("LabelModelPath")
        self.label_model_path.setStyleSheet("#LabelModelPath{ background : rgba(0, 128, 0, 120); }")
        self.lineEdit_model_path = LineEdit()
        # self.lineEdit_model_path.setText()
        self.toolPushButton_get_model_path = ToolButton()
        self.toolPushButton_get_model_path.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_DirOpenIcon))

        self.hBoxLayout_local_model.addWidget(self.label_model_path)
        self.hBoxLayout_local_model.addWidget(self.lineEdit_model_path)
        self.hBoxLayout_local_model.addWidget(self.toolPushButton_get_model_path)
        
        model_online_RadioButton = RadioButton()
        model_online_RadioButton.setChecked(False)
        model_online_RadioButton.setText(self.__tr("在线下载模型"))
        model_online_RadioButton.setToolTip(self.__tr("下载可能会花费很长时间，具体取决于网络状态，\n作为参考 large-v2 模型下载量最大约 6GB"))
        self.model_online_RadioButton = model_online_RadioButton
        self.addWidget(model_online_RadioButton)

        self.hBoxLayout_online_model = QHBoxLayout()
        self.addLayout(self.hBoxLayout_online_model)

        # 添加一些控件到布局中
        self.label_online_model_name = QLabel()    
        self.label_online_model_name.setText(self.__tr("模型名称"))
        self.label_online_model_name.setObjectName("LabelOnlineModelName")
        self.label_online_model_name.setStyleSheet("#LabelOnlineModelName{ background : rgba(0, 128, 0, 120); }")
        self.combox_online_model = EditableComboBox()

        # 下拉框设置项目
        self.combox_online_model.addItems(self.model_names)

        # 下拉框设置自动完成
        completer = QCompleter(self.model_names, self)
        self.combox_online_model.setCompleter(completer)
        self.combox_online_model.setCurrentIndex(0)
        self.hBoxLayout_online_model.addWidget(self.label_online_model_name)
        self.hBoxLayout_online_model.addWidget(self.combox_online_model)

        self.setModelLocationLayout()

        GridLayout_model_param = QGridLayout()
        GridLayout_model_param.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.addLayout(GridLayout_model_param)

        # 设备
        label_device = QLabel()
        label_device.setText(self.__tr("处理设备："))
        label_device.setObjectName("LabelDevice")
        label_device.setStyleSheet("#LabelDevice{background : rgba(240, 113, 0, 128);}")
        device_combox  = ComboBox()
        device_combox.addItems(self.device_list)
        device_combox.setCurrentIndex(1)
        self.device_combox = device_combox
        GridLayout_model_param.addWidget(label_device,0,0)
        GridLayout_model_param.addWidget(device_combox,0,1)

        label_device_index = QLabel()
        label_device_index.setText(self.__tr("设备号："))
        LineEdit_device_index = LineEdit()
        LineEdit_device_index.setText("0")
        LineEdit_device_index.setToolTip(self.__tr("要使用的设备ID。也可以通过传递ID列表(例如0,1,2,3)在多GPU上加载模型。"))
        self.LineEdit_device_index = LineEdit_device_index
        GridLayout_model_param.addWidget(label_device_index,1,0)
        GridLayout_model_param.addWidget(LineEdit_device_index,1,1)

        # 计算精度
        VLayout_preciese = QHBoxLayout()
        label_preciese = QLabel()
        label_preciese.setText(self.__tr("计算精度："))
        label_preciese.setObjectName("LabelPreciese")
        label_preciese.setStyleSheet("#LabelPreciese{background: rgba(240, 113, 0, 128);}")
        preciese_combox  = EditableComboBox()
        preciese_combox.addItems(self.preciese_list)
        preciese_combox.setCurrentIndex(5)
        preciese_combox.setCompleter(QCompleter(self.preciese_list))
        preciese_combox.setToolTip(self.__tr("要使用的计算精度，尽管某些设备不支持半精度，\n但事实上不论选择什么精度类型都可以隐式转换。\n请参阅 https://opennmt.net/CTranslate2/quantization.html。"))
        self.preciese_combox = preciese_combox
        GridLayout_model_param.addWidget(label_preciese,2,0)
        GridLayout_model_param.addWidget(preciese_combox,2,1)

        label_cpu_threads = QLabel()
        label_cpu_threads.setText(self.__tr("线程数（CPU）"))
        LineEdit_cpu_threads = LineEdit()
        LineEdit_cpu_threads.setText("4")
        LineEdit_cpu_threads.setToolTip(self.__tr("在CPU上运行时使用的线程数(默认为4)。非零值会覆盖"))
        self.LineEdit_cpu_threads = LineEdit_cpu_threads
        GridLayout_model_param.addWidget(label_cpu_threads,3,0)
        GridLayout_model_param.addWidget(LineEdit_cpu_threads,3,1)

        label_num_workers = QLabel()
        label_num_workers.setText(self.__tr("并发数"))
        LineEdit_num_workers = LineEdit()
        LineEdit_num_workers.setText("1")
        LineEdit_num_workers.setToolTip(self.__tr("具有多个工作线程可以在运行模型时实现真正的并行性。\n这可以以增加内存使用为代价提高整体吞吐量。"))
        self.LineEdit_num_workers = LineEdit_num_workers
        GridLayout_model_param.addWidget(label_num_workers,4,0)
        GridLayout_model_param.addWidget(LineEdit_num_workers,4,1)

        button_download_root = PushButton()
        button_download_root.setText(self.__tr("下载缓存目录"))
        # button_download_root.clicked.connect(self.getDownloadCacheDir)
        self.LineEdit_download_root = LineEdit()
        self.LineEdit_download_root.setToolTip(self.__tr("模型下载保存的目录。如果未修改,\n则模型将保存在标准Hugging Face缓存目录中。"))
        # self.LineEdit_download_root.setText(self.download_cache_path)
        self.LineEdit_download_root = self.LineEdit_download_root
        self.button_download_root = button_download_root
        GridLayout_model_param.addWidget(button_download_root,5,0)
        GridLayout_model_param.addWidget(self.LineEdit_download_root,5,1)

        label_local_files_only =QLabel()
        label_local_files_only.setText(self.__tr("是否使用本地缓存"))
        combox_local_files_only = ComboBox()
        combox_local_files_only.addItems(["False", "True"])
        combox_local_files_only.setCurrentIndex(1)
        combox_local_files_only.setToolTip(self.__tr("如果为True，在本地缓存的文件存在时返回其路径，不再重新下载文件。"))
        self.combox_local_files_only = combox_local_files_only
        GridLayout_model_param.addWidget(label_local_files_only,6,0)
        GridLayout_model_param.addWidget(combox_local_files_only,6,1)

        hBoxLayout_model_convert = QHBoxLayout()
        self.addLayout(hBoxLayout_model_convert)

        self.button_set_model_out_dir =  PushButton()
        self.button_set_model_out_dir.setText(self.__tr("模型输出目录"))
        hBoxLayout_model_convert.addWidget(self.button_set_model_out_dir)

        self.LineEdit_model_out_dir = LineEdit()
        self.LineEdit_model_out_dir.setToolTip(self.__tr("转换模型的保存目录，不会自动创建子目录"))
        hBoxLayout_model_convert.addWidget(self.LineEdit_model_out_dir)

        self.button_convert_model = PushButton()
        self.button_convert_model.setText(self.__tr("下载并转换模型"))
        self.button_convert_model.setToolTip(self.__tr("转换 OpenAi 模型到本地格式，\n必须选择在线模型"))
        hBoxLayout_model_convert.addWidget(self.button_convert_model)

        self.button_model_lodar = PushButton()
        self.button_model_lodar.setText(self.__tr("加载模型"))
        self.addWidget(self.button_model_lodar)

        self.LineEdit_download_root.setText(self.parent().download_cache_path)

        # self.page_model.setStyleSheet("#pageModelParameter{border:1px solid red; padding: 5px;}")
        
    
