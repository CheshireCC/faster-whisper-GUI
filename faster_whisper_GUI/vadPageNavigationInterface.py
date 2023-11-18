from PySide6.QtCore import QCoreApplication

from PySide6.QtWidgets import (
                                QGridLayout
                                , QHBoxLayout
                            )

from qfluentwidgets import (
                                SwitchButton
                                , LineEdit
                                , ComboBox
                                , TitleLabel
                                , DoubleSpinBox
                            )

from .navigationInterface import NavigationBaseInterface
from .paramItemWidget import ParamWidget
from .style_sheet import StyleSheet

class VADNavigationInterface(NavigationBaseInterface):
    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)
    
    def __init__(self, parent=None):
        super().__init__(
                            title = self.__tr("Silero VAD")
                            , subtitle = self.__tr("VAD（人声活动检测）及 VAD 模型参数")
                            , parent = parent
                        )

        self.setupUI()
        self.SignalAndSlotConnect()
        StyleSheet.TRANSCRIBEPAGEINTERFACE.apply(self.view)

    def setupUI(self):

        self.HLayout_VAD_check = QHBoxLayout()

        self.VAD_check_switchButton= SwitchButton()
        self.VAD_check_switchButton.setChecked(True)

        # ================================================================================================================================
        self.titleLabel_VAD= TitleLabel(self.__tr("VAD 参数"))
        self.addWidget(self.titleLabel_VAD)
        
        # --------------------------------------------------------------------------------------------------------------------------------------
        self.VAD_check_param_widget = ParamWidget(self.__tr("启用 VAD"),
                                                    self.__tr("VAD 模型常用来对音频文件的非语音段进行筛除, 可以有效减小 Whisper 模型幻听"),
                                                    self.VAD_check_switchButton
                                                )

        self.HLayout_VAD_check.setContentsMargins(10,0,10,0)
        self.HLayout_VAD_check.addWidget(self.VAD_check_param_widget)

        # ------------------------------------------------------------------------------------------------------------------------------------

        GridLayout_VAD_param = QGridLayout()
        self.GridLayout_VAD_param = GridLayout_VAD_param
        GridLayout_VAD_param.setContentsMargins(10,0,10,0)
        GridLayout_VAD_param.setSpacing(0)

        # ------------------------------------------------------------------------------------------------------------------------------------
        
        self.doubleSpin_VAD_param_threshold = DoubleSpinBox()
        self.doubleSpin_VAD_param_threshold.setRange(0.0, 1.0)
        self.doubleSpin_VAD_param_threshold.setSingleStep(0.05)
        self.doubleSpin_VAD_param_threshold.setValue(0.50)
        # self.doubleSpin_VAD_param_threshold.setSuffix("%")
        
        self.VAD_param_threshold_param_widget = ParamWidget(self.__tr("概率阈值"), 
                                                            self.__tr("语音概率阈值。 Silero VAD为每个音频块输出语音概率, 概率高于此值的认为是语音。\n最好对每个数据集单独调整此参数, 但“懒散”的 0.5 对大多数数据集来说都非常好。"),
                                                            self.doubleSpin_VAD_param_threshold
                                                        )

        self.GridLayout_VAD_param.addWidget(self.VAD_param_threshold_param_widget, 0, 0)

        # -------------------------------------------------------------------------------------------------------------------------------------------
        self.LineEdit_VAD_param_min_speech_duration_ms = LineEdit()
        self.LineEdit_VAD_param_min_speech_duration_ms.setText("250")
        
        self.VAD_param_min_speech_duration_ms_param_widget = ParamWidget(self.__tr("最小语音持续时间(ms)"),
                                                                        self.__tr("最小语音块时长，毫秒为单位，时长短于该参数值的最终语音块会被抛弃"),
                                                                        self.LineEdit_VAD_param_min_speech_duration_ms
                                                                    )
        
        self.GridLayout_VAD_param.addWidget(self.VAD_param_min_speech_duration_ms_param_widget, 1, 0)
        # -------------------------------------------------------------------------------------------------------------------------------------------
        
        self.LineEdit_VAD_param_max_speech_duration_s = LineEdit()
        self.LineEdit_VAD_param_max_speech_duration_s.setText("inf")

        self.VAD_param_max_speech_duration_s_param_widget = ParamWidget(self.__tr("最大语音块时长(s)"),
                                                                        self.__tr("语音块的最大持续时间(秒)。比该参数值指定时长更长的块将在最后一个持续时间超过100ms的静音时间戳拆分(如果有的话),\n以防止过度切割。否则,它们将在参数指定值的时长之前强制拆分。"),
                                                                        self.LineEdit_VAD_param_max_speech_duration_s
                                                                    )
        self.GridLayout_VAD_param.addWidget(self.VAD_param_max_speech_duration_s_param_widget, 2, 0)

        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        self.LineEdit_VAD_param_min_silence_duration_ms = LineEdit() 
        self.LineEdit_VAD_param_min_silence_duration_ms.setText("2000")

        self.VAD_param_min_silence_duration_ms_param_widget = ParamWidget(self.__tr("最小静息时长(ms)"),    
                                                                            self.__tr("在每个语音块结束时等待该参数值指定的时长再拆分它。"),
                                                                            self.LineEdit_VAD_param_min_silence_duration_ms 
                                                                        )

        self.GridLayout_VAD_param.addWidget(self.VAD_param_min_silence_duration_ms_param_widget, 3, 0)

        # ------------------------------------------------------------------------------------------------------------------------------------------------
        
        combox_VAD_param_window_size_samples = ComboBox()
        combox_VAD_param_window_size_samples.addItems(["512", "1024", "1536"])
        combox_VAD_param_window_size_samples.setCurrentIndex(1)
        combox_VAD_param_window_size_samples.setToolTip(self.__tr("警告!\nSilero VAD模型使用16000采样率训练得到512,1024,1536样本。其他值可能会影响模型性能!"))
        self.combox_VAD_param_window_size_samples = combox_VAD_param_window_size_samples

        self.VAD_param_window_size_samples_param_widget = ParamWidget(self.__tr("采样窗口大小"),
                                                                    self.__tr("指定大小的音频块被馈送到silero VAD模型。"),
                                                                    self.combox_VAD_param_window_size_samples
                                                                )
        
        self.GridLayout_VAD_param.addWidget(self.VAD_param_window_size_samples_param_widget, 4,0)
        

        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        self.LineEdit_VAD_param_speech_pad_ms = LineEdit()
        self.LineEdit_VAD_param_speech_pad_ms.setText("400")
        
        self.VAD_param_speech_pad_ms_param_widget = ParamWidget(self.__tr("语音块前后填充"),
                                                                self.__tr("最终的语音块前后都由指定时长的空白填充"),
                                                                self.LineEdit_VAD_param_speech_pad_ms
                                                            )
        self.GridLayout_VAD_param.addWidget(self.VAD_param_speech_pad_ms_param_widget , 5, 0)

        # ----------------------------------------------------------------------------------------------------------------------        
        self.addLayout(self.HLayout_VAD_check)
        self.addLayout(GridLayout_VAD_param)


        # ================================================================================================================================================================
        # self.titleLabel_HuggingFace = TitleLabel(self.__tr("huggingface 参数"))
        # self.addWidget(self.titleLabel_HuggingFace )
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # GridLayout_speakerDiarize_param = QGridLayout()
        # self.GridLayout_speakerDiarize_param = GridLayout_speakerDiarize_param
        # GridLayout_speakerDiarize_param.setContentsMargins(10,10,10,10)
        # self.addLayout(self.GridLayout_speakerDiarize_param)


    def SignalAndSlotConnect(self):
        self.VAD_check_switchButton.checkedChanged.connect(self.setVADUILayout)
        

    def setVADUILayout(self):
        num_widgets_layout = self.GridLayout_VAD_param.count()
            
        for i in range(num_widgets_layout):
            widget = self.GridLayout_VAD_param.itemAt(i).widget()
            widget.setEnabled(self.VAD_check_switchButton.isChecked())
        
    def getParam(self):
        param = {}
        param["use_VAD"] = self.VAD_check_switchButton.isChecked()
        param["threshold"] = self.doubleSpin_VAD_param_threshold.value()
        param["minSpeechDuration"] = self.LineEdit_VAD_param_min_speech_duration_ms.text().strip()
        param["minSilenceDuration"] = self.LineEdit_VAD_param_min_silence_duration_ms.text().strip()
        param["maxSpeechDuration"] = self.LineEdit_VAD_param_max_speech_duration_s.text().strip()
        param["windowSize"] = self.combox_VAD_param_window_size_samples.currentIndex()
        param["speechPad"] = self.LineEdit_VAD_param_speech_pad_ms.text().strip()
        
        return param

    def setParam(self, param:dict):
        
        self.VAD_check_switchButton.setChecked(param["use_VAD"])
        self.doubleSpin_VAD_param_threshold.setValue(param["threshold"] )
        self.LineEdit_VAD_param_min_speech_duration_ms.setText(param["minSpeechDuration"])
        self.LineEdit_VAD_param_min_silence_duration_ms.setText(param["minSilenceDuration"])
        self.LineEdit_VAD_param_max_speech_duration_s.setText(param["maxSpeechDuration"])
        self.combox_VAD_param_window_size_samples.setCurrentIndex(param["windowSize"])
        self.LineEdit_VAD_param_speech_pad_ms.setText(param["speechPad"])
        