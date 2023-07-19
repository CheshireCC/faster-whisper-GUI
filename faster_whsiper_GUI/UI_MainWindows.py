'''
Author: CheshireCC 36411617+CheshireCC@users.noreply.github.com
Date: 2023-07-19 05:07:50
LastEditors: CheshireCC 36411617+CheshireCC@users.noreply.github.com
LastEditTime: 2023-07-19 22:25:24
FilePath: \fatser_whsiper_GUI\test_GUI.py
Description: 
'''

# coding:utf-8
import sys
import os

from PySide6.QtCore import  Qt
from PySide6.QtWidgets import QApplication, QFileDialog, QFrame, QWidget, QStackedWidget, QVBoxLayout, QLabel, QStyle
from PySide6.QtWidgets import QHBoxLayout, QGridLayout, QCompleter, QTextBrowser
from PySide6.QtGui import QIcon

from qfluentwidgets import Pivot, setTheme, Theme, LineEdit, CheckBox, ComboBox, RadioButton, ToolButton, EditableComboBox, PushButton, TextEdit
from qframelesswindow import FramelessMainWindow , StandardTitleBar
from config import Language_dict, Preciese_list, Model_names, Device_list
from resource import Image_rc


class mainWin(FramelessMainWindow):

    def __init__(self):
        super().__init__()

        self.model_path = r"./model/whsiper-large-v2-ct2-f32"
        self.model_names = Model_names
        # 模型支持的计算设备
        self.device_list = Device_list
        # 模型支持的计算精度
        self.preciese_list = Preciese_list
        # 语言支持
        self.LANGUAGES_DICT = Language_dict
        userDir = os.path.expanduser("~")
        cache_dir = os.path.join(userDir,".cache","huggingface","hub").replace("\\", "/")
        self.download_cache_path = cache_dir

        self.initWin()

        # 创建窗体中心控件
        self.mainWindowsWidget = QWidget(self)
        self.mainWindowsWidget.setObjectName("mainWidget")

        # 创建窗体主布局
        self.mainLayout = QGridLayout()
        # 将主布局添加到窗体中心控件
        self.mainWindowsWidget.setLayout(self.mainLayout)

        # 创建窗体导航枢 和 stacke 控件 以及放置控件的垂直布局
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout()

        # 将导航布局添加到主布局
        self.mainLayout.addLayout(self.vBoxLayout,0,0)

        # 设置窗体中心控件
        self.setCentralWidget(self.mainWindowsWidget)
        # 设置中心控件上边距
        # self.mainWindowsWidget.setStyleSheet("#mainWidget{margin-top:30px}")

        # 设置层到最后避免遮挡窗体按钮
        self.mainWindowsWidget.lower()

        # 添加子界面
        self.page_model = QWidget()
        self.addSubInterface(self.page_model, "pageModelParameter", "模型参数")
        self.page_VAD = QWidget()
        self.addSubInterface(self.page_VAD, "pageVADParameter", "VAD 参数")
        self.page_transcribes = QWidget()
        self.addSubInterface(self.page_transcribes, "pageTranscribesParameter", "转写参数")
        self.page_process = QWidget()
        self.addSubInterface(self.page_process, "pageProcess", "执行转写")

        # 将导航枢 和 stacke 添加到窗体布局
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)

        # self.stackedWidget.setGeometry(50,50,500,500)
        # 设置当前的子界面
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.page_transcribes)
        self.pivot.setCurrentItem(self.page_transcribes.objectName())

        # UI设置
        self.setupUI()
        # 信号和槽处理
        self.singleAndSlotProcess()

    def initWin(self):
        # setTheme(Theme.LIGHT)
        self.setStyleSheet(
                            """
                            mainWin{
                                background: white; 
                                }
                            QLabel{
                                font: 15px 'Segoe UI';
                                background: rgb(242,242,242);
                                border-radius: 8px
                                    }
                            """
                            )

        # self.resize(800, 500)
        self.setGeometry(500,50,800,500)

        # 添加标题栏 但是不知道为甚么它不显示
        self.setTitleBar(StandardTitleBar(self))
        self.setWindowTitle("FasterWhisper")
        # self.setWindowIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_TrashIcon))
        # self.setWindowIcon(self.style().standardPixmap(":/resource/Image/microphone.png"))
        self.setWindowIcon(QIcon(":/resource/Image/microphone.png"))
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

    def setupUI(self):

        self.setupVADUI()
        self.setupModelUI()
        self.setupTranscribesUI()
        self.setupProcessUI()

    def setupProcessUI(self):
        VBoxLayout = QVBoxLayout()
        self.page_process.setLayout(VBoxLayout)

        self.processResultText = QTextBrowser()
        # self.processResultText.setText("Hello Whsiper")
        VBoxLayout.addWidget(self.processResultText)

        self.button_process = PushButton()
        self.button_process.setText("Transcribes")
        VBoxLayout.addWidget(self.button_process)

        VBoxLayout.setStretch(0,10)
        VBoxLayout.setStretch(1,2)

        self.page_process.setStyleSheet("#pageProcess{border: 1px solid cyan; padding: 5px;}")

        self.button_process.setObjectName("processButton")
        self.button_process.setStyleSheet("#processButton{background:242 242 242}")

        

    def setupTranscribesUI(self):

        VBoxLayout_Transcribes = QVBoxLayout()
        self.page_transcribes.setLayout(VBoxLayout_Transcribes)

        hBoxLayout_Audio_File = QHBoxLayout()
        hBoxLayout_Audio_File.setSpacing(10)
        hBoxLayout_Audio_File.setContentsMargins(10,10,10,10)

        label_1 = QLabel()
        label_1.setText("目标音频文件")
        hBoxLayout_Audio_File.addWidget(label_1)

        self.fileNameLineEdit = LineEdit()
        self.fileNameLineEdit.setToolTip("要转写的音频文件路径")
        hBoxLayout_Audio_File.addWidget(self.fileNameLineEdit)

        fileChosePushButton = ToolButton()
        self.fileOpenPushButton = fileChosePushButton
        fileChosePushButton.setToolTip("选择要转写的音频文件")
        fileChosePushButton.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_FileIcon))
        fileChosePushButton.resize(385,420)
        hBoxLayout_Audio_File.addWidget(fileChosePushButton)
        VBoxLayout_Transcribes.addLayout(hBoxLayout_Audio_File)

        GridBoxLayout_other_paramters = QGridLayout()
        VBoxLayout_Transcribes.addLayout(GridBoxLayout_other_paramters)

        Label_language = QLabel("Language")
        self.combox_language = EditableComboBox()
        self.combox_language.addItem("Auto")
        for key, value in self.LANGUAGES_DICT.items():
            self.combox_language.addItem(value + "    " + key)
        
        self.combox_language.setCurrentIndex(0)
        completer_language = QCompleter([item.text for item in self.combox_language.items])
        completer_language.setFilterMode(Qt.MatchFlag.MatchContains)
        self.combox_language.setCompleter(completer_language)
        self.combox_language.setToolTip("音频中的语言。如果选择 Auto，则自动在音频的前30秒内检测语言。")
        GridBoxLayout_other_paramters.addWidget(Label_language, 0, 0)
        GridBoxLayout_other_paramters.addWidget(self.combox_language, 0, 1)
        
        label_Translate_to_English = QLabel("翻译为英语")
        self.combox_Translate_to_English = ComboBox()
        self.combox_Translate_to_English.addItems(["False", "True"])
        self.combox_Translate_to_English.setCurrentIndex(0)
        self.combox_Translate_to_English.setToolTip("输出转写结果翻译为英语的翻译结果")
        GridBoxLayout_other_paramters.addWidget(label_Translate_to_English,1,0)
        GridBoxLayout_other_paramters.addWidget(self.combox_Translate_to_English, 1, 1)

        label_beam_size = QLabel("分块大小")
        self.LineEdit_beam_size = LineEdit()
        self.LineEdit_beam_size.setText("5")
        self.LineEdit_beam_size.setToolTip("用于解码的音频块的大小。")
        GridBoxLayout_other_paramters.addWidget(label_beam_size ,2,0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_beam_size, 2, 1)

        label_best_of = QLabel("最佳热度")
        self.LineEdit_best_of = LineEdit()
        self.LineEdit_best_of.setText("5")
        self.LineEdit_best_of.setToolTip("采样时使用非零热度的候选数")
        GridBoxLayout_other_paramters.addWidget(label_best_of ,3,0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_best_of, 3, 1)

        label_patience = QLabel("搜索耐心")
        self.LineEdit_patience = LineEdit()
        self.LineEdit_patience.setToolTip("搜索音频块时的耐心因子")
        self.LineEdit_patience.setText("1.0")
        GridBoxLayout_other_paramters.addWidget(label_patience, 4,0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_patience, 4, 1)

        label_length_penalty = QLabel("惩罚常数")
        self.LineEdit_length_penalty = LineEdit()
        self.LineEdit_length_penalty.setText("1.0")
        self.LineEdit_length_penalty.setToolTip("指数形式的长度惩罚常数")
        GridBoxLayout_other_paramters.addWidget(label_length_penalty, 5,0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_length_penalty, 5,1)

        label_temperature = QLabel("采样热度候选")
        self.LineEdit_temperature = LineEdit()
        self.LineEdit_temperature.setText("0.0,0.2,0.4,0.6,0.8,1.0")
        self.LineEdit_temperature.setToolTip("采样的温度。\n当程序因为压缩比参数或者采样标记概率参数失败时会依次使用")
        GridBoxLayout_other_paramters.addWidget(label_temperature, 6, 0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_temperature, 6, 1)
        

        label_compression_ratio_threshold = QLabel("gzip 压缩比阈值")
        self.LineEdit_compression_ratio_threshold = LineEdit()
        self.LineEdit_compression_ratio_threshold.setText("2.4")
        self.LineEdit_compression_ratio_threshold.setToolTip("如果音频的gzip压缩比高于此值，则视为失败。")
        GridBoxLayout_other_paramters.addWidget(label_compression_ratio_threshold, 7, 0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_compression_ratio_threshold, 7, 1)

        label_log_prob_threshold = QLabel("采样概率阈值")
        self.LineEdit_log_prob_threshold = LineEdit()
        self.LineEdit_log_prob_threshold.setText("-1.0")
        self.LineEdit_log_prob_threshold.setToolTip("如果采样标记的平均对数概率阈值低于此值，则视为失败")
        GridBoxLayout_other_paramters.addWidget(label_log_prob_threshold, 8, 0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_log_prob_threshold, 8 ,1)

        label_no_speech_threshold  = QLabel("静音阈值")
        self.LineEdit_no_speech_threshold = LineEdit()
        self.LineEdit_no_speech_threshold.setText("0.6")
        self.LineEdit_no_speech_threshold.setToolTip("音频段的如果非语音概率高于此值，\n并且对采样标记的平均对数概率低于阈值，\n则将该段视为静音。")
        GridBoxLayout_other_paramters.addWidget(label_no_speech_threshold, 9, 0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_no_speech_threshold, 9,1)

        label_condition_on_previous_text = QLabel("循环提示")
        self.combox_condition_on_previous_text = ComboBox()
        self.combox_condition_on_previous_text.addItems(["True", "False"])
        self.combox_condition_on_previous_text.setCurrentIndex(0)
        self.combox_condition_on_previous_text.setToolTip("如果启用，则将模型的前一个输出作为下一个音频段的提示;\n禁用可能会导致文本在段与段之间不一致，\n但模型不太容易陷入失败循环，\n比如重复循环或时间戳失去同步。")
        GridBoxLayout_other_paramters.addWidget(label_condition_on_previous_text, 10,0)
        GridBoxLayout_other_paramters.addWidget(self.combox_condition_on_previous_text, 10, 1)

        label_initial_prompt = QLabel("初始提示词")
        self.LineEdit_initial_prompt = LineEdit()
        self.LineEdit_initial_prompt.setToolTip("为第一个音频段提供的可选文本字符串或词元 id 提示词，可迭代项。")
        GridBoxLayout_other_paramters.addWidget(label_initial_prompt, 11, 0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_initial_prompt, 11 ,1)

        label_prefix = QLabel("初始文本前缀")
        self.LineEdit_prefix = LineEdit()
        self.LineEdit_prefix.setToolTip("为第初始音频段提供的可选文本前缀。")
        GridBoxLayout_other_paramters.addWidget(label_prefix, 12, 0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_prefix, 12, 1)

        label_suppress_blank = QLabel("空白抑制")
        self.combox_suppress_blank = ComboBox()
        self.combox_suppress_blank.addItems(["True", "False"])
        self.combox_suppress_blank.setCurrentIndex(0)
        self.combox_suppress_blank.setToolTip("在采样开始时抑制空白输出。")
        GridBoxLayout_other_paramters.addWidget(label_suppress_blank, 13, 0)
        GridBoxLayout_other_paramters.addWidget(self.combox_suppress_blank, 13 ,1)

        label_suppress_tokens = QLabel("特定标记抑制")
        self.LineEdit_suppress_tokens = LineEdit()
        self.LineEdit_suppress_tokens.setText("-1")
        self.LineEdit_suppress_tokens.setToolTip("要抑制的标记ID列表。 \n-1 将抑制模型配置文件 config.json 中定义的默认符号集。")
        GridBoxLayout_other_paramters.addWidget(label_suppress_tokens, 14, 0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_suppress_tokens, 14, 1)

        label_without_timestamps  = QLabel("关闭时间戳")
        self.combox_without_timestamps = ComboBox()
        self.combox_without_timestamps.addItems(["False", "True"])
        self.combox_without_timestamps.setCurrentIndex(0)
        self.combox_without_timestamps.setToolTip("开启时将会仅输出文本不输出时间戳")
        GridBoxLayout_other_paramters.addWidget(label_without_timestamps, 15, 0)
        GridBoxLayout_other_paramters.addWidget(self.combox_without_timestamps, 15, 1)

        label_max_initial_timestamp = QLabel("最晚初始时间戳")
        self.LineEdit_max_initial_timestamp = LineEdit()
        self.LineEdit_max_initial_timestamp.setText("1.0")
        self.LineEdit_max_initial_timestamp.setToolTip("首个时间戳不能晚于此时间。")
        GridBoxLayout_other_paramters.addWidget(label_max_initial_timestamp, 16, 0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_max_initial_timestamp, 16, 1)


        label_word_timestamps = QLabel("单词级时间戳")
        self.combox_word_timestamps = ComboBox()
        self.combox_word_timestamps.addItems(["False", "True"])
        self.combox_word_timestamps.setCurrentIndex(0)
        self.combox_word_timestamps.setToolTip("用交叉注意力模式和动态时间规整提取单词级时间戳，\n并在每个段的每个单词中包含时间戳。")
        GridBoxLayout_other_paramters.addWidget(label_word_timestamps, 17, 0)
        GridBoxLayout_other_paramters.addWidget(self.combox_word_timestamps, 17,1)
        
        label_prepend_punctuations = QLabel("标点向后合并")
        self.LineEdit_prepend_punctuations = LineEdit()
        self.LineEdit_prepend_punctuations.setText("\"'“¿([{-")
        self.LineEdit_prepend_punctuations.setToolTip("如果开启单词级时间戳，\n则将这些标点符号与下一个单词合并。")
        GridBoxLayout_other_paramters.addWidget(label_prepend_punctuations, 18, 0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_prepend_punctuations, 18, 1)

        label_append_punctuations = QLabel("标点向前合并")
        self.LineEdit_append_punctuations = LineEdit()
        self.LineEdit_append_punctuations.setText("\"'.。,，!！?？:：”)]}、")
        self.LineEdit_append_punctuations.setToolTip("如果开启单词级时间戳，\n则将这些标点符号与前一个单词合并。")
        GridBoxLayout_other_paramters.addWidget(label_append_punctuations, 19,0)
        GridBoxLayout_other_paramters.addWidget(self.LineEdit_append_punctuations, 19, 1)
        
        self.page_transcribes.setStyleSheet("#pageTranscribesParameter{border: 1px solid blue; padding: 5px}")
        VBoxLayout_Transcribes.setAlignment(Qt.AlignmentFlag.AlignTop)


    def setupModelUI(self):
        # 总布局
        self.vBoxLayout_model_param = QVBoxLayout()
        self.page_model.setLayout(self.vBoxLayout_model_param)
        vBoxLayout_onlien_local_model = QVBoxLayout()
        self.vBoxLayout_model_param.addLayout(vBoxLayout_onlien_local_model)

        model_local_RadioButton = RadioButton()
        self.model_local_RadioButton = model_local_RadioButton
        model_local_RadioButton.setChecked(True)
        model_local_RadioButton.setText("使用本地模型")
        model_local_RadioButton.setToolTip("本地模型需使用经过 CTranslate2 转换工具，从 OpenAI 模型格式转换而来的模型")
        vBoxLayout_onlien_local_model.addWidget(model_local_RadioButton)

        self.hBoxLayout_local_model = QHBoxLayout()
        vBoxLayout_onlien_local_model.addLayout(self.hBoxLayout_local_model)

        # 使用本地模型时添加相关控件到布局
        self.label_model_path = QLabel()
        self.label_model_path.setText("模型文件路径")
        self.lineEdit_model_path = LineEdit()
        self.lineEdit_model_path.setText(self.model_path)
        self.toolPushButton_get_model_path = ToolButton()
        self.toolPushButton_get_model_path.setIcon(self.style().standardPixmap(QStyle.StandardPixmap.SP_DirOpenIcon))

        self.toolPushButton_get_model_path.clicked.connect(self.getLocalModelPath)

        self.hBoxLayout_local_model.addWidget(self.label_model_path)
        self.hBoxLayout_local_model.addWidget(self.lineEdit_model_path)
        self.hBoxLayout_local_model.addWidget(self.toolPushButton_get_model_path)
        
        model_online_RadioButton = RadioButton()
        self.model_online_RadioButton = model_online_RadioButton
        model_online_RadioButton.setChecked(False)
        model_online_RadioButton.setText("在线下载模型")
        model_online_RadioButton.setToolTip("下载可能会花费很长时间，具体取决于网络状态，\n作为参考 large-v2 模型下载量最大约 6GB")
        vBoxLayout_onlien_local_model.addWidget(model_online_RadioButton)

        self.hBoxLayout_online_model = QHBoxLayout()
        vBoxLayout_onlien_local_model.addLayout(self.hBoxLayout_online_model)
        # 添加一些控件到布局中
        self.label_online_model_name = QLabel()    
        self.label_online_model_name.setText("模型名称")
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
        self.vBoxLayout_model_param.addLayout(GridLayout_model_param)

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
        button_download_root.clicked.connect(self.getDownloadCacheDir)
        LineEdit_download_root = LineEdit()
        LineEdit_download_root.setToolTip("模型下载保存的目录。如果未修改,\n则模型将保存在标准Hugging Face缓存目录中。")
        LineEdit_download_root.setText(self.download_cache_path)
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

        # GridLayout_model_param.setContentsMargins(10,10,10,10)
        self.page_model.setStyleSheet("#pageModelParameter{border:1px solid red; padding: 5px;}")
        self.vBoxLayout_model_param.setAlignment(Qt.AlignmentFlag.AlignTop)

    
    def setupVADUI(self):

        # VAD 模型引入以及 VAD 参数
        self.VLayout_VAD = QVBoxLayout(self.page_VAD)
        self.VLayout_VAD.setStretch(0,2)
        self.VLayout_VAD.setStretch(1,7)

        self.HLayout_VAD_check = QHBoxLayout()

        VAD_check= CheckBox()
        VAD_check.setText("是否启用 VAD 及 VAD 参数")
        VAD_check.setChecked(False)
        VAD_check.setToolTip("VAD 模型常用来对语音文件的空白段进行筛除, 可以有效减小 Whsiper 模型幻听")
        self.VAD_check = VAD_check
        self.VAD_check.setChecked(True)

        self.HLayout_VAD_check.setContentsMargins(10,10,10,10)
        self.HLayout_VAD_check.addWidget(VAD_check)

        GridLayout_VAD_param = QGridLayout()
        self.GridLayout_VAD_param = GridLayout_VAD_param
        GridLayout_VAD_param.setContentsMargins(10,10,10,10)

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

        self.VLayout_VAD.addLayout(self.HLayout_VAD_check)
        self.VLayout_VAD.addLayout(GridLayout_VAD_param)
        self.VLayout_VAD.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.page_VAD.setLayout(self.VLayout_VAD)

        # self.page_VAD.setObjectName("pageVADParameter")
        self.page_VAD.setStyleSheet("#pageVADParameter{border:1px solid green; padding: 5px;}")
        
    
    def addSubInterface(self, layout: QWidget, objectName, text: str ):
        layout.setObjectName(objectName)
#         layout.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(layout)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(layout)
        )
        

    def onCurrentIndexChanged(self, index):
        if not index :
            index = self.stackedWidget.currentIndex()
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())

    def getLocalModelPath(self):
        """
        get path of local model dir
        """
        path = QFileDialog.getExistingDirectory(self,"选择模型文件所在的文件夹",r"./")
        if path:
            self.lineEdit_model_path.setText(path)
            self.model_path = path

    def setModelLocationLayout(self):
        num_widgets_layout = self.hBoxLayout_local_model.count()
            # print(num_widgets_layout)
            # 遍历并移除存在于布局上的控件
        for i in range(num_widgets_layout):
            widget = self.hBoxLayout_local_model.itemAt(i).widget()
            widget.setEnabled(self.model_local_RadioButton.isChecked())
        
        num_widgets_layout = self.hBoxLayout_online_model.count()
            # print(num_widgets_layout)
            # 遍历并移除存在于布局上的控件
        for i in range(num_widgets_layout):
            widget = self.hBoxLayout_online_model.itemAt(i).widget()
            widget.setEnabled(self.model_online_RadioButton.isChecked())
    
    def setVADUILayout(self):
        num_widgets_layout = self.GridLayout_VAD_param.count()
            # print(num_widgets_layout)
            # 遍历并移除存在于布局上的控件
        for i in range(num_widgets_layout):
            widget = self.GridLayout_VAD_param.itemAt(i).widget()
            widget.setEnabled(not (widget.isEnabled()))

    def getDownloadCacheDir(self):
        """
        get path of local model dir
        """
        path = QFileDialog.getExistingDirectory(self,"选择缓存文件夹", self.LineEdit_download_root.text())
        if path:
            self.lineEdit_model_path.setText(path)
            self.download_cache_path = path
    
    def getFileName(self):
        """
        get a file name from a dialog
        """
        fileName, _ = QFileDialog.getOpenFileName(self, "选择音频文件", r"./", "Wave file(*.wav)")
        if fileName:
            self.fileNameLineEdit.setText(fileName)


    def singleAndSlotProcess(self):
        """
        process single connect and others
        """

        self.fileOpenPushButton.clicked.connect(self.getFileName)
        self.model_local_RadioButton.clicked.connect(self.setModelLocationLayout)
        self.model_online_RadioButton.clicked.connect(self.setModelLocationLayout)
        self.VAD_check.clicked.connect(self.setVADUILayout)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = mainWin()
    w.show()
    app.exec()