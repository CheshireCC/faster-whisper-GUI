from PySide6.QtCore import QDataStream, QFile, Slot
from PySide6.QtWidgets import  QFileDialog, QMessageBox, QMainWindow, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QLabel, QStyle, QFrame, QCompleter, QGridLayout

import sys

from PySide6.QtGui import QPixmap

from qframelesswindow import FramelessWindow as FW
from qframelesswindow import TitleBar

from qfluentwidgets import ComboBox, ToolButton, LineEdit, RadioButton, EditableComboBox, CheckBox, PushButton

class mainWin(FW):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.model_path = r"./model/whsiper-large-v2-ct2-f32"
        self.model_names = ["tiny", "tiny.en", "base", "base.en", "small", 
                                            "small.en", "medium", "medium.en", "large-v1", "large-v2"]
        self.completer = QCompleter(self.model_names, self)

        # 模型支持的计算设备
        self.device_list = ["cpu", "cuda", "auto"]

        # 模型支持的计算精度
        self.preciese_list = ['int8',
                            'int8_float16',
                            'int8_bfloat16',
                            'int16',
                            'float16',
                            'float32',
                            'bfloat16']
        # 语言支持
        self.LANGUAGES_list = {
                            "en": "english",
                            "zh": "chinese",
                            "de": "german",
                            "es": "spanish",
                            "ru": "russian",
                            "ko": "korean",
                            "fr": "french",
                            "ja": "japanese",
                            "pt": "portuguese",
                            "tr": "turkish",
                            "pl": "polish",
                            "ca": "catalan",
                            "nl": "dutch",
                            "ar": "arabic",
                            "sv": "swedish",
                            "it": "italian",
                            "id": "indonesian",
                            "hi": "hindi",
                            "fi": "finnish",
                            "vi": "vietnamese",
                            "he": "hebrew",
                            "uk": "ukrainian",
                            "el": "greek",
                            "ms": "malay",
                            "cs": "czech",
                            "ro": "romanian",
                            "da": "danish",
                            "hu": "hungarian",
                            "ta": "tamil",
                            "no": "norwegian",
                            "th": "thai",
                            "ur": "urdu",
                            "hr": "croatian",
                            "bg": "bulgarian",
                            "lt": "lithuanian",
                            "la": "latin",
                            "mi": "maori",
                            "ml": "malayalam",
                            "cy": "welsh",
                            "sk": "slovak",
                            "te": "telugu",
                            "fa": "persian",
                            "lv": "latvian",
                            "bn": "bengali",
                            "sr": "serbian",
                            "az": "azerbaijani",
                            "sl": "slovenian",
                            "kn": "kannada",
                            "et": "estonian",
                            "mk": "macedonian",
                            "br": "breton",
                            "eu": "basque",
                            "is": "icelandic",
                            "hy": "armenian",
                            "ne": "nepali",
                            "mn": "mongolian",
                            "bs": "bosnian",
                            "kk": "kazakh",
                            "sq": "albanian",
                            "sw": "swahili",
                            "gl": "galician",
                            "mr": "marathi",
                            "pa": "punjabi",
                            "si": "sinhala",
                            "km": "khmer",
                            "sn": "shona",
                            "yo": "yoruba",
                            "so": "somali",
                            "af": "afrikaans",
                            "oc": "occitan",
                            "ka": "georgian",
                            "be": "belarusian",
                            "tg": "tajik",
                            "sd": "sindhi",
                            "gu": "gujarati",
                            "am": "amharic",
                            "yi": "yiddish",
                            "lo": "lao",
                            "uz": "uzbek",
                            "fo": "faroese",
                            "ht": "haitian creole",
                            "ps": "pashto",
                            "tk": "turkmen",
                            "nn": "nynorsk",
                            "mt": "maltese",
                            "sa": "sanskrit",
                            "lb": "luxembourgish",
                            "my": "myanmar",
                            "bo": "tibetan",
                            "tl": "tagalog",
                            "mg": "malagasy",
                            "as": "assamese",
                            "tt": "tatar",
                            "haw": "hawaiian",
                            "ln": "lingala",
                            "ha": "hausa",
                            "ba": "bashkir",
                            "jw": "javanese",
                            "su": "sundanese",
                            }

        # UI
        self.setupUI()
        # single process
        self.singleAndSlotProcess()

        self.setContentsMargins(10,10,10,10)
        self.setTitleBar(TitleBar(self))


    def setVADUILayout(self):
        
        if self.VAD_check.isChecked():

            label_VAD_param_threshold = QLabel()
            label_VAD_param_threshold.setText("阈值")
            LineEdit_VAD_param_threshold = LineEdit()
            LineEdit_VAD_param_threshold.setText("0.5")
            LineEdit_VAD_param_threshold.setToolTip("语音阈值。\n Silero VAD为每个音频块输出语音概率,概率高于此值的认为是语音。\n最好对每个数据集单独调整此参数,\n但“懒散”的0.5对大多数数据集来说都非常好。")
            self.GridLayout_VAD_param.addWidget(label_VAD_param_threshold,0,0)
            self.GridLayout_VAD_param.addWidget(LineEdit_VAD_param_threshold,0,1)
            self.LineEdit_VAD_param_threshold = LineEdit_VAD_param_threshold



            label_VAD_patam_min_speech_duration_ms = QLabel()
            label_VAD_patam_min_speech_duration_ms.setText("最小语音持续时间(ms)")            
            LineEdit_VAD_patam_min_speech_duration_ms = LineEdit()
            LineEdit_VAD_patam_min_speech_duration_ms.setText("250")
            LineEdit_VAD_patam_min_speech_duration_ms.setToolTip("短于该参数值的最终语音块会被抛弃。")
            self.GridLayout_VAD_param.addWidget(label_VAD_patam_min_speech_duration_ms,1,0)
            self.GridLayout_VAD_param.addWidget(LineEdit_VAD_patam_min_speech_duration_ms,1,1)
            self.LineEdit_VAD_patam_min_speech_duration_ms  = LineEdit_VAD_patam_min_speech_duration_ms

            label_VAD_patam_max_speech_duration_s = QLabel()
            label_VAD_patam_max_speech_duration_s.setText("最大语音块时长(s)")            
            LineEdit_VAD_patam_max_speech_duration_s = LineEdit()
            LineEdit_VAD_patam_max_speech_duration_s.setText("inf")
            LineEdit_VAD_patam_max_speech_duration_s.setToolTip("语音块的最大持续时间(秒)。\n比该参数值指定时长更长的块将在最后一个持续时间超过100ms的静音时间戳拆分(如果有的话),\n以防止过度切割。\n否则,它们将在参数指定值的时长之前强制拆分。")
            self.GridLayout_VAD_param.addWidget(label_VAD_patam_max_speech_duration_s, 2,0)
            self.GridLayout_VAD_param.addWidget(LineEdit_VAD_patam_max_speech_duration_s, 2,1)
            self.LineEdit_VAD_patam_max_speech_duration_s = LineEdit_VAD_patam_max_speech_duration_s
            

            label_VAD_patam_min_silence_duration_ms = QLabel()
            label_VAD_patam_min_silence_duration_ms.setText("最小静息时长(ms)")            
            LineEdit_VAD_patam_min_silence_duration_ms = LineEdit()
            LineEdit_VAD_patam_min_silence_duration_ms.setText("2000")
            LineEdit_VAD_patam_min_silence_duration_ms.setToolTip("在每个语音块结束时等待该参数值指定的时长再拆分它。")
            self.GridLayout_VAD_param.addWidget(label_VAD_patam_min_silence_duration_ms, 3,0)
            self.GridLayout_VAD_param.addWidget(LineEdit_VAD_patam_min_silence_duration_ms, 3,1)
            self.LineEdit_VAD_patam_min_silence_duration_ms = LineEdit_VAD_patam_min_silence_duration_ms


            label_VAD_patam_window_size_samples = QLabel()
            label_VAD_patam_window_size_samples.setText("采样窗口大小")
            combox_VAD_patam_window_size_samples = ComboBox()
            combox_VAD_patam_window_size_samples.addItems(["512", "1024", "1536"])
            combox_VAD_patam_window_size_samples.setCurrentIndex(1)
            combox_VAD_patam_window_size_samples.setToolTip("指定大小的音频块被馈送到silero VAD模型。\n警告!\nSilero VAD模型使用16000采样率训练得到512,1024,1536样本。\n其他值可能会影响模型性能!")
            self.GridLayout_VAD_param.addWidget(label_VAD_patam_window_size_samples, 4,0)
            self.GridLayout_VAD_param.addWidget(combox_VAD_patam_window_size_samples, 4,1)
            self.combox_VAD_patam_window_size_samples = combox_VAD_patam_window_size_samples

            label_VAD_patam_speech_pad_ms = QLabel()
            label_VAD_patam_speech_pad_ms.setText("语音块前后填充")
            LineEdit_VAD_patam_speech_pad_ms = LineEdit()
            LineEdit_VAD_patam_speech_pad_ms.setText("400")
            LineEdit_VAD_patam_speech_pad_ms.setToolTip("最终的语音块前后都由指定时长的空白填充。")
            self.GridLayout_VAD_param.addWidget(label_VAD_patam_speech_pad_ms, 5,0)
            self.GridLayout_VAD_param.addWidget(LineEdit_VAD_patam_speech_pad_ms, 5,1)
            self.LineEdit_VAD_patam_speech_pad_ms = LineEdit_VAD_patam_speech_pad_ms


        else:
            num_widgets_layout = self.GridLayout_VAD_param.count()
            # print(num_widgets_layout)
            # 遍历并移除存在于布局上的控件
            for i in range(num_widgets_layout):
            
                self.GridLayout_VAD_param.itemAt(i).widget().deleteLater()
        


    def setModelLocationLayout(self):
        """
        change widgets that could be used accord to status of RadioButton widgets
        """
        # get number of items of layout
        num_widgets_layout = self.model_path_HLayout.count()
        # print(num_widgets_layout)
        # 遍历并移除存在于布局上的控件
        for i in range(num_widgets_layout):
            
            self.model_path_HLayout.itemAt(i).widget().deleteLater()


        if self.model_online_RadioButton.isChecked():

            # 添加一些控件到布局中
            self.label_online_model_name = QLabel()    
            self.label_online_model_name.setText("模型名称")
            self.combox_online_model = EditableComboBox()

            # 下拉框设置项目
            self.combox_online_model.addItems(self.model_names)

            # 下拉框设置自动完成
            self.combox_online_model.setCompleter(self.completer)

            self.model_path_HLayout.addWidget(self.label_online_model_name)
            self.model_path_HLayout.addWidget(self.combox_online_model)
            
        elif self.model_local_RadioButton.isChecked():
            
            # 使用本地模型时添加相关控件到布局
            self.label_model_path = QLabel()
            self.label_model_path.setText("模型文件路径")
            self.lineEdit_model_path = LineEdit()
            self.lineEdit_model_path.setText(self.model_path)
            self.toolPushButton_get_model_path = ToolButton()
            self.toolPushButton_get_model_path.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_DirOpenIcon))

            self.toolPushButton_get_model_path.clicked.connect(self.getLocalModelPath)

            self.model_path_HLayout.addWidget(self.label_model_path)
            self.model_path_HLayout.addWidget(self.lineEdit_model_path)
            self.model_path_HLayout.addWidget(self.toolPushButton_get_model_path)


    def singleAndSlotProcess(self):
        """
        process single connect and others
        """

        self.fileOpenPushButton.clicked.connect(self.getFileName)
        self.model_local_RadioButton.clicked.connect(self.setModelLocationLayout)
        self.model_online_RadioButton.clicked.connect(self.setModelLocationLayout)
        self.VAD_check.clicked.connect(self.setVADUILayout)

    def getFileName(self):
        """
        get a file name from a dialog
        """
        fileName, _ = QFileDialog.getOpenFileName(self, "选择音频文件", r"./", "Wave file(*.wav)")
        if fileName:
            self.fileNameLineEdit.setText(fileName)

    def getLocalModelPath(self):
        """
        get path of local model dir
        """
        path = QFileDialog.getExistingDirectory(self,"选择模型文件所在的文件夹",r"./")
        if path:
            self.lineEdit_model_path.setText(path)
            self.model_path = path

    def setupUI(self):
        """
        create UI
        """

        # 添加主布局
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # 为窗口新增布局
        Hlayout_1 = QHBoxLayout()
        Hlayout_1.setSpacing(10)
        Hlayout_1.setContentsMargins(10,10,10,10)

        label_1 = QLabel()
        label_1.setText("目标音频文件")
        Hlayout_1.addWidget(label_1)

        self.fileNameLineEdit = LineEdit()
        self.fileNameLineEdit.setToolTip("要转写的音频文件路径")
        Hlayout_1.addWidget(self.fileNameLineEdit)

        fileChosePushButton = ToolButton()
        self.fileOpenPushButton = fileChosePushButton
        fileChosePushButton.setToolTip("选择要转写的音频文件")
        fileChosePushButton.setToolTip("选择要转写的音频文件")
        fileChosePushButton.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_FileIcon))
        fileChosePushButton.resize(385,420)
        Hlayout_1.addWidget(fileChosePushButton)
        
        # Hlayout_1.setStretch(0,2)
        # Hlayout_1.setStretch(1,10)
        # Hlayout_1.setStretch(2,5)

        mainLayout.addLayout(Hlayout_1)

        # ----------------------------------------------------------------------------------------------
        # 添加分割线
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        mainLayout.addWidget(hline)


        # 新布局用于存放处理模型路径等
        model_VLayout = QVBoxLayout()
        mainLayout.addLayout(model_VLayout)

            # 添加新选择按钮，用于选择模型在线或者本地
        model_location_Hlayout = QHBoxLayout()
        model_online_RadioButton = RadioButton()
        self.model_online_RadioButton = model_online_RadioButton
        model_online_RadioButton.setChecked(False)
        model_online_RadioButton.setText("在线下载模型")
        model_online_RadioButton.setToolTip("下载可能会花费很长时间，具体取决于网络状态，\n作为参考 large-v2 模型下载量最大约 6GB")
        model_location_Hlayout.addWidget(model_online_RadioButton)
        

        model_local_RadioButton = RadioButton()
        self.model_local_RadioButton = model_local_RadioButton
        model_local_RadioButton.setChecked(True)
        model_local_RadioButton.setText("使用本地模型")
        model_local_RadioButton.setToolTip("本地模型需使用经过 CTranslate2 转换工具，从 OpenAI 模型格式转换而来的模型")
        model_location_Hlayout.addWidget(model_local_RadioButton)

        # 新布局 用于存放模型路径或名称的相关控件
        self.model_path_HLayout = QHBoxLayout()
        self.model_path_HLayout.setContentsMargins(10,10,10,10)
        self.model_path_HLayout.setSpacing(10)
        
        # 根据当前选择按钮的选中情况设置控件到布局上
        self.setModelLocationLayout()
        

        # 布局中添加布局
        model_VLayout.addLayout(model_location_Hlayout)
        model_VLayout.addLayout(self.model_path_HLayout)
        

        # ----------------------------------------------------------------------------------------------
        hline_2 = QFrame()
        hline_2.setFrameShape(QFrame.HLine)
        hline_2.setFrameShadow(QFrame.Sunken)
        mainLayout.addWidget(hline_2)


        GridLayout_model_param = QGridLayout()

        # 设备
        label_device = QLabel()
        label_device.setText("处理设备：")
        device_combox  = ComboBox()
        device_combox.addItems(self.device_list)
        device_combox.setCurrentIndex(1)
        self.device_combox = device_combox
        GridLayout_model_param.addWidget(label_device,0,0)
        GridLayout_model_param.addWidget(device_combox,0,1)


        label_device_index = QLabel()
        label_device_index.setText("设备号：")
        LineEdit_device_index = LineEdit()
        LineEdit_device_index.setText("0")
        LineEdit_device_index.setToolTip("要使用的设备ID。也可以通过传递ID列表(例如0,1,2,3)在多GPU上加载模型。")
        self.LineEdit_device_index = LineEdit_device_index
        GridLayout_model_param.addWidget(label_device_index,1,0)
        GridLayout_model_param.addWidget(LineEdit_device_index,1,1)


        # 计算精度
        VLayout_preciese = QHBoxLayout()
        label_preciese = QLabel()
        label_preciese.setText("计算精度：")
        preciese_combox  = EditableComboBox()
        preciese_combox.addItems(self.preciese_list)
        preciese_combox.setCurrentIndex(5)
        preciese_combox.setCompleter(QCompleter(self.preciese_list))
        preciese_combox.setToolTip("要使用的计算精度，尽管某些设备不支持半精度，\n但事实上不论选择什么精度类型都可以隐式转换。\n请参阅 https://opennmt.net/CTranslate2/quantization.html。")
        self.preciese_combox = preciese_combox
        GridLayout_model_param.addWidget(label_preciese,2,0)
        GridLayout_model_param.addWidget(preciese_combox,2,1)


        label_cpu_threads = QLabel()
        label_cpu_threads.setText("线程数（CPU）")
        LineEdit_cpu_threads = LineEdit()
        LineEdit_cpu_threads.setText("4")
        LineEdit_cpu_threads.setToolTip("在CPU上运行时使用的线程数(默认为4)。非零值会覆盖")
        self.LineEdit_cpu_threads = LineEdit_cpu_threads
        GridLayout_model_param.addWidget(label_cpu_threads,3,0)
        GridLayout_model_param.addWidget(LineEdit_cpu_threads,3,1)


        label_num_workers = QLabel()
        label_num_workers.setText("并发数")
        LineEdit_num_workers = LineEdit()
        LineEdit_num_workers.setText("1")
        LineEdit_num_workers.setToolTip("具有多个工作线程可以在运行模型时实现真正的并行性。\n这可以以增加内存使用为代价提高整体吞吐量。")
        self.LineEdit_num_workers = LineEdit_num_workers
        GridLayout_model_param.addWidget(label_num_workers,4,0)
        GridLayout_model_param.addWidget(LineEdit_num_workers,4,1)

        button_download_root = PushButton()
        button_download_root.setText("下载缓存目录")
        LineEdit_download_root = LineEdit()
        LineEdit_download_root.setText("")
        LineEdit_download_root.setToolTip("模型下载保存的目录。如果未设置,\n则模型将保存在标准Hugging Face缓存目录中。")
        self.LineEdit_download_root = LineEdit_download_root
        self.button_download_root = button_download_root
        GridLayout_model_param.addWidget(button_download_root,5,0)
        GridLayout_model_param.addWidget(LineEdit_download_root,5,1)


        label_local_files_only =QLabel()
        label_local_files_only.setText("是否使用本地缓存")
        combox_local_files_only = ComboBox()
        combox_local_files_only.addItems(["False", "True"])
        combox_local_files_only.setCurrentIndex(1)
        combox_local_files_only.setToolTip("如果为True，在本地缓存的文件存在时返回其路径，不再重新下载文件。")
        self.combox_local_files_only = combox_local_files_only
        GridLayout_model_param.addWidget(label_local_files_only,6,0)
        GridLayout_model_param.addWidget(combox_local_files_only,6,1)


        GridLayout_model_param.setContentsMargins(10,10,10,10)

        mainLayout.addLayout(GridLayout_model_param)


        # ----------------------------------------------------------------------------------------------
        hline_3 = QFrame()
        hline_3.setFrameShape(QFrame.HLine)
        hline_3.setFrameShadow(QFrame.Sunken)
        mainLayout.addWidget(hline_3)

        # VAD 模型引入以及 VAD 参数
        VLayout_VAD = QVBoxLayout()
        HLayout_VAD_check = QHBoxLayout()

        VAD_check= CheckBox()
        VAD_check.setText("是否启用 VAD 及 VAD 参数")
        VAD_check.setChecked(False)
        VAD_check.setToolTip("VAD 模型常用来对语音文件的空白段进行筛除, 可以有效减小 Whsiper 模型幻听")
        self.VAD_check = VAD_check

        HLayout_VAD_check.setContentsMargins(10,10,10,10)
        HLayout_VAD_check.addWidget(VAD_check)

        GridLayout_VAD_param = QGridLayout()
        self.GridLayout_VAD_param = GridLayout_VAD_param
        GridLayout_VAD_param.setContentsMargins(10,10,10,10)

        self.setVADUILayout()

        VLayout_VAD.addLayout(HLayout_VAD_check)
        VLayout_VAD.addLayout(GridLayout_VAD_param)
        mainLayout.addLayout(VLayout_VAD)

