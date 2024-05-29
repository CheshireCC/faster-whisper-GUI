# coding:utf-8

import os
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import (
                                QCompleter,
                                QFileDialog
                                , QGridLayout
                            )

from qfluentwidgets import (
                            EditableComboBox
                            , LineEdit
                            , PushButton
                            , InfoBar
                            , InfoBarPosition
                            , TitleLabel
                            , SwitchButton
                            , ComboBox
                        )

from .config import Language_dict
from .navigationInterface import NavigationBaseInterface

# import datetime
import json

from .util import outputWithDateTime, WhisperParameters
from .style_sheet import StyleSheet

from .paramItemWidget import ParamWidget


class TranscribeNavigationInterface(NavigationBaseInterface):
    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)
    
    def __init__(self, parent=None):
        
        super().__init__(
                        title=self.__tr("FasterWhisper")
                        , subtitle=self.__tr("faster-whisper 模型全部参数")
                        , parent=parent
                    )
        
        self.paramDir = r"./"
        
        self.LANGUAGES_DICT = Language_dict
        
        self.setObjectName('transcribeNavigationInterface')
        self.setupUI()

        self.SignalAndSlotConnect()
        StyleSheet.TRANSCRIBEPAGEINTERFACE.apply(self.view)


    def saveParams(self):
        outputWithDateTime("SaveParaments")

        params = self.getParam()
        for key, value in params.items():
            print(f"{key}:{value}")
        print("")
        file, _ = QFileDialog.getSaveFileName(
                                                self, 
                                                self.__tr("选择保存文件"),
                                                self.paramDir,
                                                "file(*.pa)"
                                        )
        
        paraDir, _ = os.path.split(file)

        self.paramDir = paraDir

        if file:
            print(f"save params to: {file}")

            try:
                with open(file, "w", encoding="utf8") as f:
                    json.dump(params, f, ensure_ascii=False, indent=4)
                
                InfoBar.success(self.__tr("保存参数"),
                                self.__tr("保存成功"),
                                duration=-1,
                                position=InfoBarPosition.TOP,
                                parent=self.toolBar
                            )
            except Exception as e:
                print(f"Error In Save Process:\n{str(e)}")
                InfoBar.error(self.__tr("保存参数"),
                                self.__tr("保存失败 查看 fasterWhisperGUI.log 可能会获取更多信息"),
                                duration=-1,
                                position=InfoBarPosition.TOP,
                                parent=self.toolBar
                            )

        else:
            return
    
    def setClipTimestampsStatus(self):
        if self.ComboBox_clip_mode.currentIndex() == 0:
            self.LineEdit_clip_timestamps.setPlaceholderText("")
            self.LineEdit_clip_timestamps.setEnabled(False)
        elif self.ComboBox_clip_mode.currentIndex() == 1:
            self.LineEdit_clip_timestamps.setPlaceholderText("0.0-10.0;25.0-36.0;......")
            self.LineEdit_clip_timestamps.setEnabled(True)
        elif self.ComboBox_clip_mode.currentIndex() == 2:
            self.LineEdit_clip_timestamps.setPlaceholderText("00:00:10.0-00:00:20.0;00:00:25.0-00:00:36.0;......")
            self.LineEdit_clip_timestamps.setEnabled(True)
            
    def SignalAndSlotConnect(self):
        self.saveParamButton.clicked.connect(self.saveParams)
        self.loadParamsButton.clicked.connect(self.loadParamsFromFile)
        self.ComboBox_clip_mode.currentIndexChanged.connect(self.setClipTimestampsStatus)
        # self.ComboBox_language.currentIndexChanged.connect(lambda:self.deta)

    def setupUI(self):
        # 使用网格布局存放参数列表
        GridBoxLayout_other_paramters = QGridLayout()
        GridBoxLayout_other_paramters.setAlignment(Qt.AlignmentFlag.AlignTop)
        GridBoxLayout_other_paramters.setContentsMargins(0,0,0,0)
        GridBoxLayout_other_paramters.setSpacing(0)
        self.addLayout(GridBoxLayout_other_paramters)
        widget_list = []

        # ============================================================================================
        self.titleLabel_normal = TitleLabel(self.__tr("常规"))
        widget_list.append(self.titleLabel_normal)
        # --------------------------------------------------------------------------------------------

        self.combox_language = EditableComboBox()
        self.combox_language.addItem("Auto")
        for key, value in self.LANGUAGES_DICT.items():
            self.combox_language.addItem(f"{key}-{value.title()}")
        
        self.combox_language.setCurrentIndex(0)
        completer_language = QCompleter([item.text for item in self.combox_language.items])
        completer_language.setFilterMode(Qt.MatchFlag.MatchContains)
        self.combox_language.setCompleter(completer_language)
        self.combox_language.setToolTip(self.__tr("音频中的语言。如果选择 Auto，则自动在音频的前30秒内检测语言。"))
        self.combox_language.setClearButtonEnabled(True)

        self.language_param_widget = ParamWidget(self.__tr("音频语言"),
                                                self.__tr("音频中使用的语言。如果选择 Auto，则自动在音频的前30秒内检测语言。也可使用此参数做强制翻译输出，但效果不佳"),
                                                self.combox_language
                                            )
        
        widget_list.append(self.language_param_widget)
        
        # --------------------------------------------------------------------------------------------
        self.LineEdit_language_detection_threshold = LineEdit()
        self.language_detection_threshold_param_widget = ParamWidget(
                                                                        self.__tr("语言检测阈值"),
                                                                        self.__tr("自动检测音频时，语言检测的阈值。如果某种语言的最大概率高于此值，则会检测为该语言。"),
                                                                        self.LineEdit_language_detection_threshold
                                                                    )    
        widget_list.append(self.language_detection_threshold_param_widget)

        # --------------------------------------------------------------------------------------------
        self.lienEdit_language_detection_segments:LineEdit =  LineEdit()
        self.lienEdit_language_detection_segments.setText("1")
        self.language_detection_segments_param_widget = ParamWidget(
                                                                        self.__tr("语言检测段落数"),
                                                                        self.__tr("自动检测音频时，语言检测需考虑的分段数。"),
                                                                        self.lienEdit_language_detection_segments
                                                                    )
        widget_list.append(self.language_detection_segments_param_widget)

        # --------------------------------------------------------------------------------------------
    
        self.switchButton_Translate_to_English = SwitchButton()
        self.switchButton_Translate_to_English.setChecked(False)

        self.task_param_widget = ParamWidget(self.__tr("翻译为英语"),
                                                self.__tr("输出转写结果翻译为英语的翻译结果"),
                                                self.switchButton_Translate_to_English
                                            )
        widget_list.append(self.task_param_widget)

        # --------------------------------------------------------------------------------------------
        self.switchButton_without_timestamps = SwitchButton()
        self.switchButton_without_timestamps.setChecked(False)

        self.without_timestampels_param_widget = ParamWidget(self.__tr("关闭时间戳细分"),
                                                            self.__tr("开启时将会输出长文本段落并对应长段落时间戳，不再进行段落细分以及相应的时间戳输出"),
                                                            self.switchButton_without_timestamps
                                                        )
        
        widget_list.append(self.without_timestampels_param_widget)

        # --------------------------------------------------------------------------------------------
        self.switchButton_word_level_timestampels = SwitchButton()
        self.switchButton_word_level_timestampels.setChecked(False)
    
        self.word_level_timestampels_param_widget = ParamWidget(self.__tr("单词级时间戳"),
                                                                self.__tr("输出卡拉OK式歌词，支持 SMI VTT LRC 格式"),
                                                                self.switchButton_word_level_timestampels
                                                            )

        widget_list.append(self.word_level_timestampels_param_widget)

        # --------------------------------------------------------------------------------------------
        self.switchButton_aggregate_contents_according_to_the_speaker = SwitchButton()
        self.switchButton_aggregate_contents_according_to_the_speaker.setChecked(False)
        self.aggregate_contents_param_widget = ParamWidget(self.__tr("根据说话人聚合内容"),
                                                                self.__tr("按顺序将相同说话人的内容聚合到一起，仅支持 txt 格式输出"),
                                                                self.switchButton_aggregate_contents_according_to_the_speaker
                                                            )
        widget_list.append(self.aggregate_contents_param_widget)

        # =======================================================================================================
        self.titleLabel_audio_segments = TitleLabel(self.__tr("音频分段设置"))
        widget_list.append(self.titleLabel_audio_segments)

        # --------------------------------------------------------------------------------------------
        self.LineEdit_max_new_tokens:LineEdit = LineEdit()
        self.LineEdit_max_new_tokens.setText("448")
        self.max_new_tokens_param_widget = ParamWidget(self.__tr("最大新令牌数"),
                                                    self.__tr("Whisper 为每个音频块生成的新令牌的最大数量。"),
                                                    self.LineEdit_max_new_tokens
                                                )
        
        widget_list.append(self.max_new_tokens_param_widget)

        # --------------------------------------------------------------------------------------------
        self.LineEdit_chunk_length:LineEdit = LineEdit()
        self.LineEdit_chunk_length.setText("30")
        self.chunk_length_param_widget = ParamWidget(self.__tr("音频块长度"),
                                                    self.__tr("音频段的长度，默认为 30 秒"),
                                                    self.LineEdit_chunk_length
                                                )
        
        widget_list.append(self.chunk_length_param_widget)

        # --------------------------------------------------------------------------------------------
        
        self.ComboBox_clip_mode:ComboBox = ComboBox()

        self.ComboBox_clip_mode.addItems([self.__tr("不启用手动分段"),self.__tr("按秒分割"),self.__tr("按时间按戳分割")])
        self.ComboBox_clip_mode.setCurrentIndex(0)
        self.clip_mode_param_widget = ParamWidget(self.__tr("音频分段模式"),
                                                    self.__tr("手动输入音频分段时要使用的分段标记方式,启用的情况下可以输入分段起止时间戳、秒为单位的分段起止点。"),
                                                    self.ComboBox_clip_mode
                                                )
        
        widget_list.append(self.clip_mode_param_widget)

        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_clip_timestamps:LineEdit = LineEdit()
        self.LineEdit_clip_timestamps.setClearButtonEnabled(True)
        self.LineEdit_clip_timestamps.setEnabled(False)
        self.clip_timestamps_param_widget = ParamWidget(
                                                            self.__tr("分段时间戳"),
                                                            self.__tr("手动输入音频分段，可输入分段时间戳，或者分段的起止秒数点，\n用\"-\"分隔起止点，用\";\"分隔不同段，最后一个结束时间戳默认为音频结尾。"),
                                                            self.LineEdit_clip_timestamps
                                                        )
        
        self.clip_timestamps_param_widget.mainHLayout.setStretch(2,6)
        widget_list.append(self.clip_timestamps_param_widget)

        # =======================================================================================================
        self.titleLabel_auditory_hallucination = TitleLabel(self.__tr("幻听参数"))
        widget_list.append(self.titleLabel_auditory_hallucination)

        # --------------------------------------------------------------------------------------------
        
        self.lineEdit_hallucination_silence_threshold:LineEdit = LineEdit()
        self.lineEdit_hallucination_silence_threshold.setText("0")
        self.hallucination_silence_threshold_param_widget = ParamWidget(self.__tr("幻听静音阈值"),
                                                    self.__tr("如果开启 单词级时间戳 ，当检测到可能的幻觉时，跳过长于此阈值（以秒为单位）的静默期。"),
                                                    self.lineEdit_hallucination_silence_threshold                           
        )
        widget_list.append(self.hallucination_silence_threshold_param_widget)

        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_patience = LineEdit()
        self.LineEdit_patience.setText("1.0")
        self.patience_param_widget = ParamWidget(self.__tr("搜索耐心"),
                                                    self.__tr("搜索音频块时的耐心因子"),
                                                    self.LineEdit_patience
                                                )
        
        widget_list.append(self.patience_param_widget)

        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_length_penalty = LineEdit()
        self.LineEdit_length_penalty.setText("1.0")
        
        self.length_penalty_param_widget = ParamWidget(self.__tr("惩罚常数"),
                                                        self.__tr("指数形式的长度惩罚常数"),
                                                        self.LineEdit_length_penalty
                                                    )
        widget_list.append(self.length_penalty_param_widget)

        # --------------------------------------------------------------------------------------------
    
        self.LineEdit_compression_ratio_threshold = LineEdit()
        self.LineEdit_compression_ratio_threshold.setText("2.4")
        
        self.compression_ratio_threshold_param_widget = ParamWidget(self.__tr("gzip 压缩比阈值"),
                                                                    self.__tr("如果音频的gzip压缩比高于此值，则视为失败。"),
                                                                    self.LineEdit_compression_ratio_threshold
                                                                )
        widget_list.append(self.compression_ratio_threshold_param_widget)

        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_log_prob_threshold = LineEdit()
        self.LineEdit_log_prob_threshold.setText("-1.0")
        
        self.log_prob_thresthold_param_widget = ParamWidget(self.__tr("采样概率阈值"),
                                                            self.__tr("如果采样标记的平均对数概率阈值低于此值，则视为失败"),
                                                            self.LineEdit_log_prob_threshold
                                                        )
        widget_list.append(self.log_prob_thresthold_param_widget)

        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_no_speech_threshold = LineEdit()
        self.LineEdit_no_speech_threshold.setText("0.6")

        self.no_speech_threshold_param_widget = ParamWidget(self.__tr("静音阈值"),
                                                            self.__tr("音频段的如果非语音概率高于此值，并且对采样标记的平均对数概率低于阈值，则将该段视为静音。"),
                                                            self.LineEdit_no_speech_threshold
                                                        )
        widget_list.append(self.no_speech_threshold_param_widget)
        
        # --------------------------------------------------------------------------------------------
        
        self.switchButton_condition_on_previous_text = SwitchButton()
        self.switchButton_condition_on_previous_text.setChecked(False)

        self.condition_on_previous_text_param_widget = ParamWidget(self.__tr("循环提示"),
                                                                    self.__tr("如果启用，则将模型的前一个输出作为下一个音频段的提示;禁用可能会导致文本在段与段之间不一致，\n但模型不太容易陷入失败循环，比如重复循环或时间戳失去同步。"),
                                                                    self.switchButton_condition_on_previous_text
                                                                )
        widget_list.append(self.condition_on_previous_text_param_widget)

        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_repetition_penalty = LineEdit()
        self.LineEdit_repetition_penalty.setText("1.0")

        self.repetition_penalty_param_switch = ParamWidget(self.__tr("重复惩罚"),
                                                            self.__tr("对先前输出进行惩罚的分数（防重复），设置值>1以进行惩罚"),
                                                            self.LineEdit_repetition_penalty 
                                                        )
        widget_list.append(self.repetition_penalty_param_switch)

        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_no_repeat_ngram_size = LineEdit()
        self.LineEdit_no_repeat_ngram_size.setText("0")
        
        self.no_repeat_ngram_size_param_widget = ParamWidget(self.__tr("禁止重复的ngram大小"),
                                                                self.__tr("如果重复惩罚配置生效，该参数防止程序反复使用此相同长度的语句进行重复检查"),
                                                                self.LineEdit_no_repeat_ngram_size
                                                            )
        widget_list.append(self.no_repeat_ngram_size_param_widget)
        

        # --------------------------------------------------------------------------------------------
        
        self.switchButton_suppress_blank = SwitchButton()
        self.switchButton_suppress_blank.setChecked(True)

        self.suppress_blank_param_widget = ParamWidget(self.__tr("空白抑制"),
                                                        self.__tr("在采样开始时抑制空白输出。"),
                                                        self.switchButton_suppress_blank
                                                    )
        widget_list.append(self.suppress_blank_param_widget)

        # ============================================================================================
        self.titleLabel_performance= TitleLabel(self.__tr("性能设置"))
        widget_list.append(self.titleLabel_performance)

        # --------------------------------------------------------------------------------------------

        self.LineEdit_beam_size = LineEdit()
        self.LineEdit_beam_size.setText("5")

        self.beam_size_param_widget = ParamWidget(self.__tr("分块大小"), 
                                                self.__tr("用于解码的音频块的大小。值越大占用越多计算机性能，速度越慢。但该值也影响转写效果"),
                                                self.LineEdit_beam_size
                                            )
        
        widget_list.append(self.beam_size_param_widget)

        # ============================================================================================
        self.titleLabel_temperature= TitleLabel(self.__tr("概率分布"))
        widget_list.append(self.titleLabel_temperature)

        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_best_of = LineEdit()
        self.LineEdit_best_of.setText("1")

        self.best_of_param_widget = ParamWidget(self.__tr("温度回退候选值个数"), 
                                                self.__tr("采样时使用非零热度的候选值个数，也即回退配置生效的时的回退次数"), 
                                                self.LineEdit_best_of
                                            )
        widget_list.append(self.best_of_param_widget)

        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_temperature = LineEdit()
        self.LineEdit_temperature.setText("0")

        self.temperature_param_widget = ParamWidget(self.__tr("温度候选"), self.__tr("温度。用于调整概率分布，从而生成不同的结果，可用于生成深度学习的数据标注。同时\n当程序因为压缩比参数或者采样标记概率参数失败时会依次使用,输入多个值时使用英文逗号分隔"), self.LineEdit_temperature)
        widget_list.append(self.temperature_param_widget)

        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_prompt_reset_on_temperature = LineEdit()
        self.LineEdit_prompt_reset_on_temperature.setText("0.5")

        self.prompt_reset_on_temperature_param_widget = ParamWidget(self.__tr("温度回退提示重置"), 
                                                                    self.__tr("如果运行中温度回退配置生效，则配置温度回退步骤后，应重置带有先前文本的提示词"), 
                                                                    self.LineEdit_prompt_reset_on_temperature
                                                                )
        widget_list.append(self.prompt_reset_on_temperature_param_widget)

        
        # ============================================================================================
        self.titleLabel_other_settings  = TitleLabel(self.__tr("其他设置"))
        widget_list.append(self.titleLabel_other_settings)
        
        # --------------------------------------------------------------------------------------------
        
        self.LineEdit_initial_prompt = LineEdit()
        
        self.initial_prompt_param_widget = ParamWidget(self.__tr("初始提示词"), 
                                                        self.__tr("为第一个音频段提供的可选文本字符串或词元 id 提示词，可迭代项。"), 
                                                        self.LineEdit_initial_prompt
                                                    )
        
        widget_list.append(self.initial_prompt_param_widget)

        # --------------------------------------------------------------------------------------------
        self.LineEdit_prefix = LineEdit()

        self.prefix_param_widget = ParamWidget(self.__tr("初始文本前缀"), 
                                            self.__tr("为初始音频段提供的可选文本前缀。"), 
                                            self.LineEdit_prefix
                                        )
        
        widget_list.append(self.prefix_param_widget)

        # --------------------------------------------------------------------------------------------
        self.LineEdit_hotwords:LineEdit = LineEdit()
        self.LineEdit_hotwords.setText("")
        self.hotwords_param_widget = ParamWidget(
                                                    self.__tr("热词/提示短语"), 
                                                    self.__tr("为模型提供的热词/提示短语。如果给定了 初始文本前缀 则热词无效。"),
                                                    self.LineEdit_hotwords
                                                )
        widget_list.append(self.hotwords_param_widget)

        # --------------------------------------------------------------------------------------------
        self.LineEdit_suppress_tokens = LineEdit()
        self.LineEdit_suppress_tokens.setText("-1")

        self.suppress_tokens_param_widget = ParamWidget(self.__tr("特定标记抑制"), 
                                                        self.__tr("要抑制的标记ID列表。 -1 将抑制模型配置文件 config.json 中定义的默认符号集。"),
                                                        self.LineEdit_suppress_tokens
                                                    )
        widget_list.append(self.suppress_tokens_param_widget)

        # --------------------------------------------------------------------------------------------
        self.LineEdit_max_initial_timestamp = LineEdit()
        self.LineEdit_max_initial_timestamp.setText("1.0")

        self.max_initial_timestamp_param_widget = ParamWidget(self.__tr("最晚初始时间戳"), 
                                                            self.__tr("首个时间戳不能晚于此时间。"),
                                                            self.LineEdit_max_initial_timestamp
                                                        )
        
        widget_list.append(self.max_initial_timestamp_param_widget )

        # --------------------------------------------------------------------------------------------
        self.LineEdit_prepend_punctuations = LineEdit()
        self.LineEdit_prepend_punctuations.setText("\"'“¿([{-")

        self.prepend_punctuations_param_widget = ParamWidget(self.__tr("标点向后合并"),
                    self.__tr("如果开启单词级时间戳，则将这些标点符号与下一个单词合并。"),
                    self.LineEdit_prepend_punctuations
                )
        
        widget_list.append(self.prepend_punctuations_param_widget)

        # --------------------------------------------------------------------------------------------
        self.LineEdit_append_punctuations = LineEdit()
        self.LineEdit_append_punctuations.setText("\"'.。,，!！?？:：”)]}、")

        self.append_punctuations_param_widget = ParamWidget(self.__tr("标点向前合并"), 
                    self.__tr("如果开启单词级时间戳，则将这些标点符号与前一个单词合并。"), 
                    self.LineEdit_append_punctuations
                )
        widget_list.append(self.append_punctuations_param_widget)

        # 批量添加控件到布局中
        
        for i ,item in enumerate(widget_list):
            try:
                GridBoxLayout_other_paramters.addWidget(item, i, 0)
            except Exception as e:
                pass
            # GridBoxLayout_other_paramters.addWidget(item[1], i, 1)

    
        self.toolBar.buttonLayout.insertSpacing(1,10)

        self.saveParamButton = PushButton()
        self.saveParamButton.setText(self.__tr("保存参数"))
        self.saveParamButton.setToolTip(self.__tr("将转写参数保存到文件"))
        self.toolBar.buttonLayout.insertWidget(2, self.saveParamButton)
        
        self.loadParamsButton = PushButton()
        self.loadParamsButton.setText(self.__tr("载入参数"))
        self.loadParamsButton.setToolTip(self.__tr("从参数文件中加载以前保存的参数"))
        self.toolBar.buttonLayout.insertWidget(3, self.loadParamsButton)
        
        
    def loadParamsFromFile(self):

        outputWithDateTime("LoadParaments")

        file,_ = QFileDialog.getOpenFileName(   self,
                                                self.__tr("选择参数文件"),
                                                self.paramDir,
                                                "file(*.pa)"
                                            )

        paraDir, _ = os.path.split(file)
        self.paramDir = paraDir

        if not file:
            return

        params = None
        try:
            with open(file, "r", encoding="utf8") as f:
                params:dict = json.load(f)
        except Exception as e:
            print(f"read paraments error: \n{str(e)}")
            InfoBar.error(self.__tr("读取参数"),
                                self.__tr("读取失败 查看 fasterWhisperGUI.log 可能会获取更多信息"),
                                duration=-1,
                                position=InfoBarPosition.TOP,
                                parent=self.toolBar
                            )
            params = None

        if params is None:
            return
        
        for key,value in params.items():
            print(f"{key}:{value}")
        
        print("")

        try:
            self.setParam(params)
            print("set paraments over")
        except Exception as e:
            print(f"set paraments error: \n{str(e)}")
            InfoBar.error(self.__tr("设置参数"),
                                self.__tr("设置失败 查看 fasterWhisperGUI.log 可能会获取更多信息"),
                                duration=-1,
                                position=InfoBarPosition.TOP,
                                parent=self.toolBar
                            )
            return

        InfoBar.success(
            self.__tr("设置参数"),
            self.__tr("设置成功"),
            duration=-1,
            position=InfoBarPosition.TOP,
            parent=self.toolBar
        )

    def setParam(self, Transcribe_params:dict) -> None:

        self.switchButton_aggregate_contents_according_to_the_speaker.setChecked(Transcribe_params["aggregate_contents"])

        self.combox_language.setCurrentIndex(Transcribe_params["language"])
        # Transcribe_params["language"] = language_index

        self.switchButton_Translate_to_English.setChecked(Transcribe_params["task"])
        # Transcribe_params["task"] = task

        self.LineEdit_beam_size.setText(str(Transcribe_params["beam_size"]))
        # Transcribe_params["beam_size"] = beam_size

        self.LineEdit_best_of.setText(str(Transcribe_params["best_of"] ))
        # Transcribe_params["best_of"] = best_of

        self.LineEdit_patience.setText(str(Transcribe_params["patience"] ))
        # Transcribe_params["patience"] = patience

        self.LineEdit_length_penalty.setText(str(Transcribe_params["length_penalty"]))
        # Transcribe_params["length_penalty"] = length_penalty

        self.LineEdit_temperature.setText(str(Transcribe_params["temperature"] ))
        # Transcribe_params["temperature"] = temperature 

        self.LineEdit_compression_ratio_threshold.setText(str(Transcribe_params["compression_ratio_threshold"]))
        # Transcribe_params["compression_ratio_threshold"] = compression_ratio_threshold

        self.LineEdit_log_prob_threshold.setText(str(Transcribe_params["log_prob_threshold"]))
        # Transcribe_params["log_prob_threshold"] = log_prob_threshold

        self.LineEdit_no_speech_threshold.setText(str(Transcribe_params["no_speech_threshold"] ))
        # Transcribe_params["no_speech_threshold"] = no_speech_threshold

        self.switchButton_condition_on_previous_text.setChecked(Transcribe_params["condition_on_previous_text"] )
        # Transcribe_params["condition_on_previous_text"] = condition_on_previous_text

        self.LineEdit_initial_prompt.setText(str(Transcribe_params["initial_prompt"] ))
        # Transcribe_params["initial_prompt"] = initial_prompt

        self.LineEdit_prefix.setText(str(Transcribe_params["prefix"] ))
        # Transcribe_params["prefix"] = prefix

        self.switchButton_suppress_blank.setChecked(Transcribe_params["suppress_blank"])
        # Transcribe_params["suppress_blank"] = suppress_blank

        self.LineEdit_suppress_tokens.setText(str(Transcribe_params["suppress_tokens"] ))
        # Transcribe_params["suppress_tokens"] = suppress_tokens

        self.switchButton_without_timestamps.setChecked(Transcribe_params["without_timestamps"] )
        # Transcribe_params["without_timestamps"] = without_timestamps

        self.LineEdit_max_initial_timestamp.setText(str(Transcribe_params["max_initial_timestamp"]))
        # Transcribe_params["max_initial_timestamp"] = max_initial_timestamp

        self.switchButton_word_level_timestampels.setChecked(Transcribe_params["word_timestamps"] )
        # Transcribe_params["word_timestamps"] = word_timestamps

        self.LineEdit_prepend_punctuations.setText(str(Transcribe_params["prepend_punctuations"] ))
        # Transcribe_params["prepend_punctuations"] = prepend_punctuations

        self.LineEdit_append_punctuations.setText(str(Transcribe_params["append_punctuations"] ))
        # Transcribe_params["append_punctuations"] = append_punctuations

        self.LineEdit_repetition_penalty.setText(str(Transcribe_params['repetition_penalty'] ))
        # Transcribe_params['repetition_penalty'] = repetition_penalty  

        self.LineEdit_no_repeat_ngram_size.setText(str(Transcribe_params["no_repeat_ngram_size"] ))
        # Transcribe_params["no_repeat_ngram_size"]  = no_repeat_ngram_size 

        self.LineEdit_prompt_reset_on_temperature.setText(str(Transcribe_params['prompt_reset_on_temperature']  ))
        # Transcribe_params['prompt_reset_on_temperature']  = prompt_reset_on_temperature 

        try:
            self.LineEdit_chunk_length.setText(Transcribe_params["chunk_length"])
            self.ComboBox_clip_mode.setCurrentIndex(Transcribe_params["clip_mode"])
            self.LineEdit_max_new_tokens.setText(Transcribe_params["max_new_tokens"])
            self.LineEdit_clip_timestamps.setText(Transcribe_params["clip_timestamps"])
            self.lineEdit_hallucination_silence_threshold.setText(Transcribe_params["hallucination_silence_threshold"])
            self.LineEdit_hotwords.setText(Transcribe_params["hotwords"])
            self.LineEdit_language_detection_threshold.setText(Transcribe_params["language_detection_threshold"])
            self.language_detection_segments_param_widget.setText(Transcribe_params["language_detection_segments"])
        except:
            pass

    def getParam(self) -> dict:
        Transcribe_params = WhisperParameters()

        # 从数据模型获取文件列表

        Transcribe_params["aggregate_contents"] = self.switchButton_aggregate_contents_according_to_the_speaker.isChecked()
        
        language = self.combox_language.currentIndex()
        Transcribe_params["language"] = language
        

        task = self.switchButton_Translate_to_English.isChecked()
        # task = STR_BOOL[task]
        Transcribe_params["task"] = task

        beam_size = self.LineEdit_beam_size.text().replace(" ", "")
        Transcribe_params["beam_size"] = beam_size

        best_of = self.LineEdit_best_of.text().replace(" ", "")
        Transcribe_params["best_of"] = best_of

        patience = self.LineEdit_patience.text().replace(" ", "")
        Transcribe_params["patience"] = patience

        length_penalty = self.LineEdit_length_penalty.text().replace(" ", "")
        Transcribe_params["length_penalty"] = length_penalty

        temperature = self.LineEdit_temperature.text().replace(" ", "")
        # temperature = [float(t) for t in temperature.split(",")]
        Transcribe_params["temperature"] = temperature 

        compression_ratio_threshold = self.LineEdit_compression_ratio_threshold.text().replace(" ", "")
        Transcribe_params["compression_ratio_threshold"] = compression_ratio_threshold

        log_prob_threshold = self.LineEdit_log_prob_threshold.text().replace(" ", "")
        Transcribe_params["log_prob_threshold"] = log_prob_threshold

        no_speech_threshold = self.LineEdit_no_speech_threshold.text().replace(" ", "")
        Transcribe_params["no_speech_threshold"] = no_speech_threshold

        condition_on_previous_text = self.switchButton_condition_on_previous_text.isChecked()
        # condition_on_previous_text = STR_BOOL[condition_on_previous_text]
        Transcribe_params["condition_on_previous_text"] = condition_on_previous_text

        initial_prompt = self.LineEdit_initial_prompt.text().strip()
        # if not initial_prompt:
        #     initial_prompt = None
        # else:
        #     lambda_initial_prompt = lambda w : int(w) if (w.isdigit()) else w
        #     initial_prompt = [lambda_initial_prompt(w) for w in initial_prompt.split(",")]

        # if initial_prompt and isinstance(initial_prompt[0], str):
        #     initial_prompt = "".join(initial_prompt)
        # elif initial_prompt :
        #     initial_prompt = [initial_prompt]
        Transcribe_params["initial_prompt"] = initial_prompt

        prefix = self.LineEdit_prefix.text().replace(" ", "") 
        Transcribe_params["prefix"] = prefix

        suppress_blank = self.switchButton_suppress_blank.isChecked()
        # suppress_blank = STR_BOOL[suppress_blank]
        Transcribe_params["suppress_blank"] = suppress_blank

        suppress_tokens = self.LineEdit_suppress_tokens.text().replace(" ", "")
        # suppress_tokens = [int(s) for s in suppress_tokens.split(",")]
        Transcribe_params["suppress_tokens"] = suppress_tokens

        without_timestamps = self.switchButton_without_timestamps.isChecked()
        # without_timestamps = STR_BOOL[without_timestamps]
        Transcribe_params["without_timestamps"] = without_timestamps

        max_initial_timestamp = self.LineEdit_max_initial_timestamp.text().replace(" ", "")
        # max_initial_timestamp = float(max_initial_timestamp)
        Transcribe_params["max_initial_timestamp"] = max_initial_timestamp

        word_timestamps = self.switchButton_word_level_timestampels.isChecked()
        # word_timestamps = STR_BOOL[word_timestamps]
        Transcribe_params["word_timestamps"] = word_timestamps

        prepend_punctuations = self.LineEdit_prepend_punctuations.text().replace(" ", "")
        Transcribe_params["prepend_punctuations"] = prepend_punctuations

        append_punctuations = self.LineEdit_append_punctuations.text().replace(" ","")
        Transcribe_params["append_punctuations"] = append_punctuations

        repetition_penalty = self.LineEdit_repetition_penalty.text().strip()
        # repetition_penalty = float(repetition_penalty)
        Transcribe_params['repetition_penalty'] = repetition_penalty  

        no_repeat_ngram_size = self.LineEdit_no_repeat_ngram_size.text().strip()
        # no_repeat_ngram_size = int(no_repeat_ngram_size)
        Transcribe_params["no_repeat_ngram_size"]  = no_repeat_ngram_size 

        prompt_reset_on_temperature  = self.LineEdit_prompt_reset_on_temperature.text().strip()
        # prompt_reset_on_temperature = float(prompt_reset_on_temperature)
        Transcribe_params['prompt_reset_on_temperature']  = prompt_reset_on_temperature 

        Transcribe_params["chunk_length"] = self.LineEdit_chunk_length.text().strip()
        Transcribe_params["clip_mode"] = self.ComboBox_clip_mode.currentIndex()
        Transcribe_params["max_new_tokens"] = self.LineEdit_max_new_tokens.text().strip()
        Transcribe_params["clip_timestamps"] = self.LineEdit_clip_timestamps.text().strip()
        Transcribe_params["hallucination_silence_threshold"] = self.lineEdit_hallucination_silence_threshold.text().strip()
        Transcribe_params["hotwords"] = self.LineEdit_hotwords.text().strip()
        Transcribe_params["language_detection_threshold"] = self.LineEdit_language_detection_threshold.text().strip()
        Transcribe_params["language_detection_segments"] = self.lienEdit_language_detection_segments.text().strip()


        return Transcribe_params
    
