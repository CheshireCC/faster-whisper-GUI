import json
import sys
import os
import time
import av
from threading import Thread

import datetime

from PySide6.QtWidgets import QFileDialog

from PySide6.QtGui import QTextCursor
from PySide6.QtCore import (
                            QCoreApplication
                            , QObject
                            , Qt
                            , Signal
                        )

from qfluentwidgets import (
                            StateToolTip
                            , InfoBar
                            , InfoBarPosition
                            , InfoBarIcon
                            , MessageBox
                            , TableView
                            , FluentIcon
                        )
from faster_whisper import TranscriptionInfo
from .config import (
                    Task_list
                    , STR_BOOL
                    , CAPTURE_PARA
                )

from .modelLoad import loadModel
from .convertModel import ConvertModel
from .transcribe import (
                        TranscribeWorker
                        , AudioStreamTranscribeWorker
                        , CaptureAudioWorker
                        , OutputWorker
                    )

from .fasterWhisperGuiIcon import FasterWhisperGUIIcon
from .UI_MainWindows import UIMainWin
from .tableModel_segments_path_info import TableModel
from .whisper_x import WhisperXWorker
from .de_mucs import DemucsWorker

# from .style_sheet import StyleSheet

from .subtitleFileRead import readSRTFileToSegments

# =======================================================================================
# SignalStore
# =======================================================================================
class RedirectOutputSignalStore(QObject):
    outputSignal = Signal(str)
    def flush( self ):
        pass
    def fileno( self ):
        return -1
    def write( self, text ):
        if ( not self.signalsBlocked() ):
            self.outputSignal.emit(str(text))

class statusToolsSignalStore(QObject):
    StateToolSignal = Signal(bool)
    LoadModelSignal = Signal(bool)

# =======================================================================================
# mainWindows function control class
# =======================================================================================
class MainWindows(UIMainWin):
    """C"""

    # def writeLog(self, text:str):
    #     def go(text:str):
    #         self.log.write(text)
    #     t1 = Thread(target=go, args=(text))
    #     t1.start()

    def __tr(self, text):
        return QCoreApplication.translate(self.__class__.__name__, text)

    def outputWithDateTime(self, text:str):
        dateTime_ = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        print(f"\n=========={dateTime_}==========")
        print(f"=========={text}==========\n")
    
    log = open(r"./fasterwhispergui.log" ,"a" ,encoding="utf8", buffering=1)

    def __init__(self):
        
        # 重定向输出
        self.redirectErrOutpur = RedirectOutputSignalStore()
        self.redirectErrOutpur.outputSignal.connect(lambda text: self.log.write(text))
        # self.redirectErrOutpur.outputSignal.connect(self.writeLog)
        # self.redirectErrOutpur.outputSignal.connect(lambda text: Thread(target=self.log.write, args=(text)).start())
        sys.stderr = self.redirectErrOutpur
        sys.stdout = self.redirectErrOutpur

        super().__init__()

        self.statusToolSignalStore = statusToolsSignalStore()

        self.transcribe_thread = None
        self.audio_capture_thread = None
        self.whisperXWorker = None
        self.outputWorker = None
        self.demucsWorker = None

        self.stateTool = None
        self.tableModel_list = {}

        self.result_whisperx_aligment = None
        self.result_faster_whisper = None
        self.result_whisperx_speaker_diarize = None

        self.modelRootDir = r"./"

        self.singleAndSlotProcess()


    def getDownloadCacheDir(self):
        """
        get path of local model dir
        """
        if path := QFileDialog.getExistingDirectory(
                                                    self
                                                    , self.__tr("选择缓存文件夹")
                                                    , self.page_model.LineEdit_download_root.text()
                                                ):
            self.page_model.LineEdit_download_root.setText(path)
            self.download_cache_path = path

    # ==============================================================================================================
    # 将于下一版本废弃
    # ==============================================================================================================
    def setTextAndMoveCursorToProcessBrowser(self, text:str):
        self.page_process.processResultText.moveCursor(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
        self.page_process.processResultText.insertPlainText(text)

    # ==============================================================================================================
    # 将于下一版本废弃
    # ==============================================================================================================
    def redirectOutput(self, target : callable):
        # 重定向输出
        sys.stdout = RedirectOutputSignalStore()
        sys.stdout.outputSignal.connect(target)

        # 错误输出已经重定向到 log 文件
        # sys.stderr = RedirectOutputSignalStore()
        # sys.stderr.outputSignal.connect(target)

    # ==============================================================================================================

    def onModelLoadClicked(self):

        del self.FasterWhisperModel
        self.FasterWhisperModel = None
        self.outputWithDateTime("LoadModel")
        
        model_param = self.getParam_model()
        for key, value in model_param.items():
            print(f"{key}: {value}")

        model_size_or_path = model_param["model_size_or_path"]

        if model_size_or_path == "":
            self.raiseErrorInfoBar(
                            title=self.__tr('模型名称错误'),
                            content=self.__tr("需要模型所在目录或者有效的模型名称。"),
                        )
            return

        if os.path.isdir(model_size_or_path):
            content = self.__tr("加载本地模型")
        else:
            content = self.__tr("在线下载模型")

        infoBar = InfoBar(
                    icon=InfoBarIcon.INFORMATION,
                    title='',
                    content=content,
                    isClosable=False,
                    orient=Qt.Orientation.Vertical,    # vertical layout
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
        
        infoBar.show()

        def go():
            self.FasterWhisperModel = loadModel(
                        model_size_or_path=model_param["model_size_or_path"]
                        , device=model_param["device"]
                        , device_index=model_param["device_index"]
                        , compute_type=model_param["compute_type"]
                        , cpu_threads=model_param["cpu_threads"]
                        , num_workers=model_param["num_workers"]
                        , download_root=model_param["download_root"]
                        , local_files_only=model_param["local_files_only"]
                        , setStatusSignal=self.statusToolSignalStore.LoadModelSignal
                    )
        
        thread_go = Thread(target= go, daemon=True)
        thread_go.start()
        self.setStateTool(self.__tr("加载模型"), self.__tr("模型加载中，请稍候"), False)

        # sys.stdout = self.oubak
        # sys.stderr = self.errbak

    def getParam_model(self) -> dict:
        """
        获取模型参数
        """
        if self.page_model.model_local_RadioButton.isChecked():
            model_size_or_path = self.page_model.lineEdit_model_path.text()
        else:
            model_size_or_path = self.page_model.combox_online_model.currentText()
        device: str = self.page_model.device_combox.currentText()
        device_index:str = self.page_model.LineEdit_device_index.text().replace(" ", "")
        device_index = [int(index) for index in device_index.split(",")]
        if len(device_index) == 1:
            device_index = device_index[0]

        compute_type: str = self.page_model.preciese_combox.currentText()
        cpu_threads: int = int(self.page_model.LineEdit_cpu_threads.text().replace(" ", ""))
        num_workers: int = int(self.page_model.LineEdit_num_workers.text().replace(" ", ""))
        download_root: str = self.page_model.LineEdit_download_root.text().replace(" ", "")
        local_files_only: str = self.page_model.combox_local_files_only.currentText()
        local_files_only = local_files_only != "False"
        model_dict : dict = {
                    "model_size_or_path" : model_size_or_path,
                    "device" : device,
                    "device_index" : device_index,
                    "compute_type" : compute_type,
                    "cpu_threads" : cpu_threads,
                    "num_workers" : num_workers,
                    "download_root" : download_root,
                    "local_files_only" : local_files_only
        }

        return model_dict

    def onButtonProcessClicked(self):
        
        self.result_whisperx_aligment = None
        self.result_faster_whisper = None
        self.result_whisperx_speaker_diarize = None
        

        if self.page_process.transceibe_Files_RadioButton.isChecked():
            self.transcribeProcess()

        elif self.page_process.audio_capture_RadioButton.isChecked():
            self.audioCaptureProcess()
        
    def audioCaptureProcess(self):
        
        if self.transcribe_thread is None and self.audio_capture_thread is None:
            self.processResultText.setText("")
            print("AudioCapture")
            VAD_param :dict = self.getVADparam()

            # vad 启用标识
            vad_filter = VAD_param["vad_filter"]
            print(f"vad_filter : {vad_filter}")
            
            if vad_filter:
                # VAD 参数
                VAD_param = VAD_param["param"]
                for key, Value in VAD_param.items():
                    print(f"  {key:<24} : {Value}")
            else:
                VAD_param = {}

            # 转写参数
            Transcribe_params : dict = self.getParamTranscribe()
            print("Transcribes options:")
            for key, value in Transcribe_params.items():
                print(f"  {key} : {value}")

            if self.FasterWhisperModel is None:
                print(self.__tr("模型未加载！进程退出"))
                self.transcribeOver(None)
                return
            
            rate_channel_dType = self.combox_capture.currentIndex()
            rate_channel_dType : dict = CAPTURE_PARA[rate_channel_dType]
            rate = rate_channel_dType["rate"]
            channels = rate_channel_dType["channel"]
            dType = rate_channel_dType["dType"]

            self.audio_capture_thread = CaptureAudioWorker(rate=rate
                                                            , channels=channels
                                                            , dType=dType
                                                        )
            self.audio_capture_thread.start()

            self.button_process.setText(self.__tr("  取消  "))
            self.button_process.setIcon(":/resource/Image/Cancel_red.svg")

        else:
            self.audioCaptureOver()
            self.resetButton_process()
            
    def getParamWhisperX(self) -> dict:
        dict_WhisperXParams = {}

        dict_WhisperXParams["use_auth_token"] = self.page_VAD.LineEdit_use_auth_token.text()

        dict_WhisperXParams["min_speaker"] = int(self.page_output.tableTab.SpinBox_min_speaker.text())
        dict_WhisperXParams["max_speaker"] = int(self.page_output.tableTab.SpinBox_max_speaker.text())

        if dict_WhisperXParams["min_speaker"] > dict_WhisperXParams["max_speaker"]:
            dict_WhisperXParams["max_speaker"] = dict_WhisperXParams["min_speaker"]
            
        if dict_WhisperXParams["min_speaker"] == 0 and dict_WhisperXParams["max_speaker"] == 0:
            dict_WhisperXParams["min_speaker"] = None
            dict_WhisperXParams["max_speaker"] = None
        else:
            dict_WhisperXParams["use_auth_token"] = None
            dict_WhisperXParams["min_speaker"] = None
            dict_WhisperXParams["max_speaker"] = None

        return dict_WhisperXParams

    def transcribeProcess(self):
        """
        process button clicked
        """
        if self.transcribe_thread is None :
            self.outputWithDateTime("Process")
            
            # 重定向输出
            self.redirectOutput(self.setTextAndMoveCursorToProcessBrowser)
            self.page_process.processResultText.setText("")
            VAD_param :dict = self.getVADparam()

            # vad 启用标识
            vad_filter = VAD_param["vad_filter"]

            output_str = f"vad_filter : {vad_filter}" + "\n"
            
            if vad_filter:
                # VAD 参数
                VAD_param = VAD_param["param"]
                for key, Value in VAD_param.items():
                    output_str = output_str + f"    -{key:<24} : {Value}" + "\n"
            else:
                VAD_param = {}
            
            print(output_str)

            # 转写参数
            Transcribe_params : dict = self.getParamTranscribe()
            print("Transcribes options:")
            for key, value in Transcribe_params.items():
                print(f"    -{key} : {value}")

            if self.FasterWhisperModel is None:
                print(self.__tr("模型未加载！进程退出"))
                self.raiseErrorInfoBar(title=self.__tr("错误") , content=self.__tr("模型未加载！"))
                self.transcribeOver(None)
                return
            
            # print(Transcribe_params['audio'])
            if len(Transcribe_params['audio']) == 0 and self.page_process.transceibe_Files_RadioButton.isChecked():
                print("No input files!")
                self.raiseErrorInfoBar(
                                        title=self.__tr("错误")
                                        , content=self.__tr("没有选择有效的音视频文件作为转写对象") 
                                    )
                
                self.transcribeOver(None)
                return
            
            try:
                num_worker = int(self.page_model.LineEdit_num_workers.text())
            except Exception as e:
                num_worker = 1

            self.transcribe_thread = TranscribeWorker(model = self.FasterWhisperModel
                                                    , parameters = Transcribe_params
                                                    , vad_filter = vad_filter
                                                    , vad_parameters = VAD_param
                                                    , num_workers = num_worker
                                                )
            
            self.transcribe_thread.signal_process_over.connect(self.transcribeOver)
            self.page_process.button_process.setText(self.__tr("取消"))
            self.page_process.button_process.setIcon(r":/resource/Image/Cancel_red.svg")
            # self.transcribe_thread.is_running == True
            self.transcribe_thread.start()
            self.setStateTool(self.__tr("音频处理"), self.__tr("正在处理中"), False)
        
        elif self.transcribe_thread is not None and self.transcribe_thread.isRunning():
            self.outputWithDateTime("Cancel")

            messageBoxW = MessageBox(self.__tr("取消")
                                    , self.__tr("是否取消操作？")
                                    , self)
            
            if messageBoxW.exec():
                self.page_process.button_process.setEnabled(False)
                self.cancelTrancribe()
                sys.stdout = self.redirectErrOutpur
                self.setStateTool(text=self.__tr("已取消"), status=True)
                
    
    def resetButton_process(self):
        self.page_process.button_process.setEnabled(True)
        self.page_process.button_process.setText(self.__tr("开始"))
        self.page_process.button_process.setIcon(FasterWhisperGUIIcon.PROCESS)
        
    def cancelTrancribe(self):
        print("Canceling...")
        self.transcribe_thread.stop()
        self.transcribe_thread.requestInterruption()
        self.raiseErrorInfoBar(title=self.__tr("取消"),content=self.__tr("操作已被用户取消"))
        print("【Process Canceled By User!】")
        self.resetButton_process()
        
    def audioCaptureOver(self):
        self.audio_capture_thread.stop()
        while(self.audio_capture_thread.isRunning()):
            time.sleep(0.1)
        self.audio_capture_thread = None
    
    def changeTableData(self, results) -> None:
        # 当转写结果列表 与表格数据模型列表长度不一致的时候 直接重新绘制所有表格
        # if len(results) != len(self.tableModel_list):
        #     self.tableModel_list = []
        #     self.showResultInTable(results=results)
        #     return

        # 获取文件名列表
        text_list = [os.path.split(result[1])[1] for result in results]
        # 获取文件目录列表
        file_list = [result[1] for result in results]
        # 获取表格标签列表
        tabBarItems = self.page_output.tableTab.tabBar.items

        # 遍历表格标签 删除已经不存在的转写结果 并改写存在的转写结果
        for tabBarItem in tabBarItems:
            if not(tabBarItem.text() in text_list):
                index = tabBarItems.index(tabBarItem)
                self.page_output.tableTab.tabBar.removeTab(index)
            else:
                for file in file_list:
                    if tabBarItem.text() == os.path.split(file)[1]:
                        self.tableModel_list[file]._data = results[file_list.index(file)][0]

        # 遍历转写结果列表，查找当前不存在的表格
        tabBarItems_text = [tabBarItem.text() for tabBarItem in self.page_output.tableTab.tabBar.items]
        for text in text_list:
            if not (text in tabBarItems_text):
                self.createResultInTable([results[text_list.index(text)]])

    def showResultInTable(self, results):
        if len(self.tableModel_list) == 0:
            print("Create Tables")
            self.createResultInTable(results=results)
        else:
            print("UPdata DataModel")
            self.changeTableData(results)

    def createResultInTable(self, results):
        i = len(self.page_output.tableTab.tabBar.items)
        for result in results:
            segments, file, _ = result
            table_view_widget = TableView()
            table_model = TableModel(segments)

            self.tableModel_list[file] = table_model

            _,text = os.path.split(file)
            table_view_widget.setObjectName(f"tab_{file}")
            table_view_widget.setModel(self.tableModel_list[file])

            self.page_output.tableTab.addSubInterface(
                                                    table_view_widget
                                                    , f"tab_{i}" 
                                                    , text
                                                    , None
                                                )
            
            i += 1
        
        print(f"len_model: {len(self.tableModel_list)}")

    def transcribeOver(self, segments_path_info:list):
        # self.button_process.clicked.disconnect(self.cancelTrancribe)
        # self.button_process.clicked.connect(self.onButtonProcessClicked)
        try:
            if self.transcribe_thread and self.transcribe_thread.is_running:
                self.transcribe_thread.stop()
        except Exception:
            pass
        while(self.transcribe_thread and self.transcribe_thread.isRunning()):
            time.sleep(0.1)

        self.setStateTool(text=self.__tr("结束"), status=True)
        self.transcribe_thread = None
        self.resetButton_process()
        sys.stdout = self.redirectErrOutpur

        if segments_path_info is not None:
            self.raiseSuccessInfoBar(
                                title=self.__tr("成功")
                                , content=self.__tr("转写完成")
                            )
            
            self.result_faster_whisper = segments_path_info
            for segments in self.result_faster_whisper:
                segment_, path, info = segments
                print(path, info.language)
                print(f"len:{len(segment_)}")
                for segment in segment_:
                    print(f"[{segment.start}s --> {segment.end}] | {segment.text}")
                    print(f"len_words: {len(segment.words)}")

            print(f"len_segments_path_info_result: {len(segments_path_info)}")
            self.showResultInTable(self.result_faster_whisper)
            self.stackedWidget.setCurrentWidget(self.page_output)
        
    def getParamTranscribe(self) -> dict:
        Transcribe_params = {}

        # audio = self.page_process.LineEdit_audio_fileName.text().strip()
        # audio = audio.split(";;") if audio != "" else []

        # 从数据模型获取文件列表
        audio = self.page_process.fileNameListView.FileNameModle.stringList()

        if self.page_process.audio_capture_RadioButton.isChecked():
            audio = "AudioStream"
        
        Transcribe_params["audio"] = audio

        language = self.page_transcribes.combox_language.text().split("-")[0]
        if language == "Auto":
            language = None
        Transcribe_params["language"] = language

        task = self.page_transcribes.combox_Translate_to_English.currentText()
        task = STR_BOOL[task]
        task = Task_list[int(task)]
        Transcribe_params["task"] = task

        beam_size = int(self.page_transcribes.LineEdit_beam_size.text().replace(" ", ""))
        Transcribe_params["beam_size"] = beam_size

        best_of = int(self.page_transcribes.LineEdit_best_of.text().replace(" ", ""))
        Transcribe_params["best_of"] = best_of

        patience = float(self.page_transcribes.LineEdit_patience.text().replace(" ", ""))
        Transcribe_params["patience"] = patience

        length_penalty = float(self.page_transcribes.LineEdit_length_penalty.text().replace(" ", ""))
        Transcribe_params["length_penalty"] = length_penalty

        temperature = self.page_transcribes.LineEdit_temperature.text().replace(" ", "")
        temperature = [float(t) for t in temperature.split(",")]
        Transcribe_params["temperature"] = temperature 

        compression_ratio_threshold = float(self.page_transcribes.LineEdit_compression_ratio_threshold.text().replace(" ", ""))
        Transcribe_params["compression_ratio_threshold"] = compression_ratio_threshold

        log_prob_threshold = float(self.page_transcribes.LineEdit_log_prob_threshold.text().replace(" ", ""))
        Transcribe_params["log_prob_threshold"] = log_prob_threshold

        no_speech_threshold = float(self.page_transcribes.LineEdit_no_speech_threshold.text().replace(" ", ""))
        Transcribe_params["no_speech_threshold"] = no_speech_threshold

        condition_on_previous_text = self.page_transcribes.combox_condition_on_previous_text.currentText()
        condition_on_previous_text = STR_BOOL[condition_on_previous_text]
        Transcribe_params["condition_on_previous_text"] = condition_on_previous_text

        initial_prompt = self.page_transcribes.LineEdit_initial_prompt.text().replace(" ", "")
        if not initial_prompt:
            initial_prompt = None
        else:
            lambda_initial_prompt = lambda w : int(w) if (w.isdigit()) else w
            initial_prompt = [lambda_initial_prompt(w) for w in initial_prompt.split(",")]
        if len(initial_prompt) == 1:
            initial_prompt = initial_prompt[0]
        Transcribe_params["initial_prompt"] = initial_prompt

        prefix = self.page_transcribes.LineEdit_prefix.text().replace(" ", "") or None
        Transcribe_params["prefix"] = prefix

        suppress_blank = self.page_transcribes.combox_suppress_blank.currentText()
        suppress_blank = STR_BOOL[suppress_blank]
        Transcribe_params["suppress_blank"] = suppress_blank

        suppress_tokens = self.page_transcribes.LineEdit_suppress_tokens.text().replace(" ", "")
        suppress_tokens = [int(s) for s in suppress_tokens.split(",")]
        Transcribe_params["suppress_tokens"] = suppress_tokens

        without_timestamps = self.page_transcribes.combox_without_timestamps.currentText()
        without_timestamps = STR_BOOL[without_timestamps]
        Transcribe_params["without_timestamps"] = without_timestamps

        max_initial_timestamp = self.page_transcribes.LineEdit_max_initial_timestamp.text().replace(" ", "")
        max_initial_timestamp = float(max_initial_timestamp)
        Transcribe_params["max_initial_timestamp"] = max_initial_timestamp

        word_timestamps = self.page_transcribes.combox_word_timestamps.currentText()
        word_timestamps = STR_BOOL[word_timestamps]
        Transcribe_params["word_timestamps"] = word_timestamps

        prepend_punctuations = self.page_transcribes.LineEdit_prepend_punctuations.text().replace(" ", "")
        Transcribe_params["prepend_punctuations"] = prepend_punctuations

        append_punctuations = self.page_transcribes.LineEdit_append_punctuations.text().replace(" ","")
        Transcribe_params["append_punctuations"] = append_punctuations

        repetition_penalty = self.page_transcribes.LineRdit_repetition_penalty.text().strip()
        repetition_penalty = float(repetition_penalty)
        Transcribe_params['repetition_penalty'] = repetition_penalty  

        no_repeat_ngram_size = self.page_transcribes.LineEdit_no_repeat_ngram_size.text().strip()
        no_repeat_ngram_size = int(no_repeat_ngram_size)
        Transcribe_params["no_repeat_ngram_size"]  = no_repeat_ngram_size 

        prompt_reset_on_temperature  = self.page_transcribes.LineEdit_prompt_reset_on_temperature.text().strip()
        prompt_reset_on_temperature = float(prompt_reset_on_temperature)
        Transcribe_params['prompt_reset_on_temperature']  = prompt_reset_on_temperature 

        return Transcribe_params
        

    def getVADparam(self) -> dict:
        """
        get param of VAD
        """

        vad_filter = self.page_VAD.VAD_check.isChecked()
        # print(vad_filter)
        VAD_param = {"vad_filter":vad_filter} 

        if not vad_filter:
            return VAD_param
        
        threshold = float(self.page_VAD.LineEdit_VAD_param_threshold.text().replace(" ", ""))
        min_speech_duration_ms = int(self.page_VAD.LineEdit_VAD_patam_min_speech_duration_ms.text().replace(" ", ""))
        max_speech_duration_s = float(self.page_VAD.LineEdit_VAD_patam_max_speech_duration_s.text().replace(" ", ""))
        min_silence_duration_ms = int(self.page_VAD.LineEdit_VAD_patam_min_silence_duration_ms.text().replace(" ", ""))
        window_size_samples = int(self.page_VAD.combox_VAD_patam_window_size_samples.currentText())
        speech_pad_ms = int(self.page_VAD.LineEdit_VAD_patam_speech_pad_ms.text().replace(" ", ""))

        VAD_param["param"] = {}
        VAD_param["param"]["threshold"] = threshold
        VAD_param["param"]["min_speech_duration_ms"] = min_speech_duration_ms
        VAD_param["param"]["max_speech_duration_s"] = max_speech_duration_s
        VAD_param["param"]["min_silence_duration_ms"] = min_silence_duration_ms
        VAD_param["param"]["window_size_samples"] = window_size_samples
        VAD_param["param"]["speech_pad_ms"] = speech_pad_ms

        return VAD_param

    def onButtonConvertModelClicked(self):

        if not self.page_model.model_online_RadioButton.isChecked():
            # QMessageBox.warning(self, "错误", "必须选择在线模型时才能使用本功能", QMessageBox.Yes, QMessageBox.Yes)
            print(self.__tr("Model Convert only Work In Onlie-Mode"))
            self.raiseErrorInfoBar(
                                    self.__tr("错误")
                                    , self.__tr("转换功能仅在在线模式下工作")
                                )
            return

        model_name_or_path = self.page_model.combox_online_model.currentText()
        model_output_dir = self.page_model.LineEdit_model_out_dir.text().replace(" ", "")
        download_cache_dir = self.page_model.LineEdit_download_root.text().replace(" ", "")
        quantization = self.page_model.preciese_combox.currentText()
        use_local_files = self.page_model.combox_local_files_only.currentText()
        use_local_files = STR_BOOL[use_local_files]

        print(self.__tr("Convert Model: "))
        print(f"  model_name_or_path : {model_name_or_path}")
        print(f"  model_output_dir   : {model_output_dir}")
        print(f"  download_cache_dir : {download_cache_dir}")
        print(f"  quantization       : {quantization}")
        print(f"  use_local_files    : {use_local_files}")

        if model_output_dir == "":
            print("\nOutput directory is required!")
            return
    
        thread_go = Thread(target=ConvertModel, daemon=True, args=[model_name_or_path, download_cache_dir,model_output_dir, quantization, use_local_files])
        thread_go.start()

    def setStateTool(self, title:str="", text:str="", status:bool=False):

        if self.stateTool is None:
            self.stateTool = StateToolTip(title, text , self)
            self.stateTool.show()

        else:
            self.stateTool.setContent(text)

        width = self.width()
        self.stateTool.move(width-self.stateTool.width()-30, 45)
        self.stateTool.setState(status)

        if  status:    
            self.stateTool = None

    def loadModelResult(self, state:bool):
        if state and self.stateTool:
            self.setStateTool(text=self.__tr("加载完成"),status=state)
            self.raiseSuccessInfoBar(
                                        title=self.__tr('加载结束'),
                                        content=self.__tr("模型加载成功")
                                    )
            
        elif not state:
            self.setStateTool(text=self.__tr("结束"), status=True)
            self.raiseErrorInfoBar(
                                    title=self.__tr("错误")
                                    , content=self.__tr("加载失败，退出并检查 fasterWhispergui.log 文件可能会获取错误信息。")
                                )

    def setModelStatusLabelTextForAll(self, status:bool):
        
        for page in self.pages:
            try:
                page.setModelStatusLabelText(status)
            except Exception as e:
                pass
    
    def getLocalModelPath(self):
        """
        get path of local model dir
        """

        path = QFileDialog.getExistingDirectory(self, self.__tr("选择模型文件所在的文件夹"), self.modelRootDir)

        if path:
            self.page_model.lineEdit_model_path.setText(path)
            self.model_path = path
            self.modelRootDir = os.path.abspath(os.path.join(path, os.pardir))

    
    def outputOver(self):
        self.setStateTool(self.__tr("保存文件"), self.__tr("结束"), True)
        self.raiseSuccessInfoBar(
                                title=self.__tr("保存完成")
                                , content=self.__tr("字幕文件已保存")
                            )

    def outputSubtitleFile(self):

        self.log.write("\n==========OutputSubtitleFiles==========\n")

        format = self.page_transcribes.combox_output_format.currentText()
        output_dir = self.page_output.outputGroupWidget.LineEdit_output_dir.text()

        result_to_write = self.result_faster_whisper if self.result_whisperx_aligment is None else (self.result_whisperx_aligment if self.result_whisperx_speaker_diarize is None else self.result_whisperx_speaker_diarize)

        self.outputWorker = OutputWorker(result_to_write, output_dir, format,self)
        self.outputWorker.signal_write_over.connect(self.outputOver)    
        self.outputWorker.start()
        self.setStateTool(self.__tr("保存文件"), self.__tr("输出字幕文件"), False)

    def raiseErrorInfoBar(self, title:str, content:str):
        InfoBar.error(
                        title=title
                        , content=content
                        , isClosable=True
                        , duration=-1
                        , orient=Qt.Orientation.Horizontal
                        , position=InfoBarPosition.TOP
                        # , position='Custom',   # NOTE: use custom info bar manager
                        , parent=self
                    ) 
        
    def aligmentOver(self, segments_path_info:list):

        self.setPageOutButtonStatus()
        
        self.setStateTool(title=self.__tr("WhisperX"), text=self.__tr("结束"), status=True)
        if segments_path_info is None:
            self.raiseErrorInfoBar(self.__tr("错误"),content=self.__tr("对齐失败，退出软件后检查 fasterwhispergui.log 文件可能会获取错误信息"))
            return
    
        self.result_whisperx_aligment = segments_path_info
        self.showResultInTable(results=self.result_whisperx_aligment)
        self.raiseSuccessInfoBar(
                                title=self.__tr("WhisperX")
                                , content=self.__tr("时间戳对齐结束")
                            )
        
        self.whisperXWorker = None

    def whisperXAligmentTimeStample(self):
        if self.result_faster_whisper is None:
            self.raiseErrorInfoBar(
                                    self.__tr("错误"),
                                    self.__tr("没有有效的 音频-字幕 转写结果，无法进行对齐")
            )
            return
        
        self.setPageOutButtonStatus()
        self.outputWithDateTime("TimeStample_Alignment")

        self.setStateTool(title=self.__tr("WhisperX"), text=self.__tr("时间戳对齐"), status=False)

        self.whisperXWorker = WhisperXWorker(self.result_faster_whisper, alignment=True,speaker_diarize=False, parent=self)
        self.whisperXWorker.signal_process_over.connect(self.aligmentOver)
        self.whisperXWorker.start()

    def whisperXDiarizeSpeakers(self):
        self.outputWithDateTime("Speaker_Diarize")
        
        whisperParams = self.getParamWhisperX()

        result_needed = self.result_whisperx_aligment if self.result_whisperx_aligment is not None else self.result_faster_whisper
        if result_needed is None:
            self.raiseErrorInfoBar(
                                    self.__tr("错误"),
                                    self.__tr("没有有效的 音频-字幕 转写结果，无法输出人声分离结果")
            )
            return

        self.setPageOutButtonStatus()

        if self.whisperXWorker is None:

            self.whisperXWorker = WhisperXWorker(result_needed
                                                , alignment=False
                                                , speaker_diarize=True
                                                , use_auth_token=whisperParams["use_auth_token"]
                                                , min_speaker=whisperParams["min_speaker"]
                                                , max_speaker=whisperParams["max_speaker"]
                                                , parent=self
                                            )

        else:
            self.whisperXWorker.segments_path_info = result_needed
            self.whisperXWorker.alignment = False
            self.whisperXWorker.speaker_diarize = True
            self.whisperXWorker.use_auth_token = whisperParams['use_auth_token']
            self.whisperXWorker.min_speaker = whisperParams['min_speaker']
            self.whisperXWorker.max_speaker = whisperParams['max_speaker']
            try:
                self.whisperXWorker.signal_process_over.disconnect(self.aligmentOver)
            except Exception as e:
                pass

        self.whisperXWorker.signal_process_over.connect(self.speakerDiarizeOver)
        self.setStateTool(title=self.__tr("WhisperX"), text=self.__tr("声源分离"), status=False)
        self.whisperXWorker.start()
    
    def setPageOutButtonStatus(self):
        self.page_output.WhisperXAligmentTimeStampleButton.setEnabled(not self.page_output.WhisperXAligmentTimeStampleButton.isEnabled())
        self.page_output.outputSubtitleFileButton.setEnabled(not self.page_output.outputSubtitleFileButton.isEnabled())
        self.page_output.WhisperXSpeakerDiarizeButton.setEnabled(not self.page_output.WhisperXSpeakerDiarizeButton.isEnabled())

    def speakerDiarizeOver(self, segments_path_info:list):
        self.setPageOutButtonStatus()

        self.setStateTool(title=self.__tr("WhisperX"), text=self.__tr("结束"), status=True)
        if segments_path_info is None:
            self.raiseErrorInfoBar(self.__tr("错误"),content=self.__tr("声源分离失败，退出软件后检查 fasterwhispergui.log 文件可能会获取错误信息"))
            return
        
        self.result_whisperx_speaker_diarize = segments_path_info
        self.showResultInTable(results=self.result_whisperx_speaker_diarize)
        self.raiseSuccessInfoBar(
                                title=self.__tr("WhisperX")
                                , content=self.__tr("声源分离结束")
                            )
        
        # for segments in self.result_whisperx_speaker_diarize:
        #         segment_, path, info = segments
        #         print(path, info.language)
        #         print(f"len:{len(segment_)}")
        #         for segment in segment_:
        #             try:
        #                 print(f"[{segment.start}s --> {segment.end}] | {segment['speaker']}:{segment.text}")
        #             except:
        #                 print(f"[{segment.start}s --> {segment.end}] | {segment.text}")

        #             print(f"len_words: {len(segment.words)}")

        self.whisperXWorker = None

    def raiseSuccessInfoBar(self, title:str, content:str):
        InfoBar.success(
                        title=title
                        , content=content
                        , isClosable=True
                        , duration=-1
                        , position=InfoBarPosition.TOP
                        , parent=self
                    )
    

    def is_audio_or_video(self, file_path:str) -> bool:
        flag = False

        # 判定打开的文件是否音视频文件
        try:
            av_cont = av.open(file_path)
            
            # 获取文件的全部 流数据
            av_streams = av_cont.streams
            for stream in av_streams:
                # 获取每个文件流的 type 信息
                if stream.codec_context.type == "audio":
                    flag = True
                    break

            if flag:
                    av_cont.close()
                    return True
            
            if not flag:
                print(f"No audio stream found in file: {file_path}")
            
            av_cont.close()
        except Exception as e:
            print(f"file open error: {e}")
            flag = None
            
        return flag
        
    def openExcitedFiles(self):
        
        self.outputWithDateTime("openExcitedFiles")

        # 必须手动选择正确的语言选项
        if self.page_transcribes.combox_language.currentText().lower() == "auto":
            messageBoxDia_ = MessageBox(self.__tr("选择语言"), self.__tr("必须选择正确的字幕语言"),self)
            messageBoxDia_.show()
            return
        
        file,_ = QFileDialog.getOpenFileName(self, self.__tr("选择音频文件"), self.page_process.fileNameListView.avDataRootDir)
        if not file:
            return

        if not self.is_audio_or_video(file):
            message_W = MessageBox(self.__tr("文件无效"),
                        self.__tr("不是音视频文件或文件无法找到音频流，请检查文件及文件格式"),
                        self)
            message_W.show()
            return

        print(f"open audio file: {file}")

        dataDir,_ = os.path.split(file)
        self.page_process.fileNameListView.avDataRootDir = dataDir
        # filesList = os.listdir(dataDir)
        
        file_subtitle_fileName = ".".join(file.split(".")[:-1]+["srt"])

        if os.path.exists(file_subtitle_fileName):
            print(f"find existed srt file: {file_subtitle_fileName}")
        else:
            file_subtitle_fileName,_ = QFileDialog.getOpenFileName(self, self.__tr("选择字幕文件"), self.page_process.fileNameListView.avDataRootDir, "SRT file(*.srt)")
            if file_subtitle_fileName and os.path.isfile(file_subtitle_fileName):
                print(f"get srt file: {file_subtitle_fileName}")
            else:
                messageBoxDia_ = MessageBox(self.__tr("无效文件"),self.__tr("必须要有有效的字幕文件"),self)
                messageBoxDia_.show()
                return
        
        segments = readSRTFileToSegments(file_subtitle_fileName)
        
        # 输出字幕文件内容
        for segment in segments:
            print(f"[{segment.start}s --> {segment.end}s] | {segment.speaker+':'+segment.text if segment.speaker else segment.text}")

        info = TranscriptionInfo(
                                    language=self.page_transcribes.combox_language.currentText().split("-")[0],
                                    language_probability=1,
                                    duration=None, 
                                    duration_after_vad=None,
                                    all_language_probs=[],
                                    transcription_options={},
                                    vad_options={}
                                )

        if file_subtitle_fileName and file:
            self.result_whisperx_aligment = None
            self.result_whisperx_speaker_diarize = None

            if self.result_faster_whisper is not None:
                self.result_faster_whisper.append((segments, file, info))
            else:
                self.result_faster_whisper = [(segments, file, info)]
            # self.tableModel_list[file] = file_subtitle_fileName
            self.showResultInTable(self.result_faster_whisper)

    def reSetButton_demucs_process(self):
        self.page_demucs.process_button.setText(self.__tr("提取"))
        self.page_demucs.process_button.setIcon( FluentIcon.IOT)
        self.page_demucs.process_button.setEnabled(True)
        

    def demucs_file_process_status(self, status:dict):
        if status["task"] == "reasmple audio":
            content = self.__tr("音频重采样")
        elif status["task"] == "separate sources":
            content = self.__tr("音轨分离")
        elif status["task"] == "save files":
            content = self.__tr("保存音频文件")
        elif status["task"] == "load model":
            content = self.__tr("加载模型...")
        elif status["task"] == "file over":
            content = self.__tr("结束")
        elif status["task"] == "download model":
            content = self.__tr("下载模型...")
        
        if status["file"] != "":
            _, fileName = os.path.split(status["file"])
        else:
            fileName = ""
        
        self.setStateTool(text=f"{fileName} {content}", status=status["status"])


    def demucs_process_over(self, status:bool):
        if status:
            self.setStateTool(text=self.__tr("分离完成"), status=True)
            self.raiseSuccessInfoBar(self.__tr("Demucs"), self.__tr("音轨分离成功"))

        else:
            self.setStateTool(text=self.__tr("结束"), status=True)
            self.raiseErrorInfoBar(self.__tr("Demucs"), self.__tr("分离失败"))

        self.reSetButton_demucs_process()

    def demucsProcess(self):
        
        if self.demucsWorker is not None and self.demucsWorker.isRunning():
            
            message_w = MessageBox(self.__tr("取消"), self.__tr('确定取消？'),self)

            if not message_w.exec():
                return

            self.outputWithDateTime("Cancel Demucs")
            self.page_demucs.process_button.setEnabled(False)
            self.demucsWorker.requestInterruption()
            self.demucsWorker.stop()

            while(self.demucsWorker.isRunning()):
                if self.stateTool is not None:
                    self.stateTool.setContent(self.__tr("正在取消操作"))
                    self.stateTool.setTitle(self.__tr("取消"))
                else:
                    self.setStateTool(self.__tr("取消"), self.__tr("正在取消操作"), False)

            self.reSetButton_demucs_process()
            self.setStateTool(self.__tr("取消"), self.__tr("用户取消操作"),True)
            return
        
        self.outputWithDateTime("Demucs")
    
        param = self.getDemucsParams()

        if len(param["audio"]) < 1:
            self.raiseErrorInfoBar(self.__tr("文件错误"), self.__tr("没有选择有效的音视频文件"))

        for key,value in param.items():
            print(f"{key}: {value}")

        if self.demucsWorker is None:
            self.demucsWorker = DemucsWorker(
                                            self,
                                            param["audio"],
                                            param["stems"],
                                            r"./cache/hdemucs_high_trained.pt",
                                            segment=param["segment"],
                                            overlap=param["overlap"],
                                            output_path=param["output_path"]
                                        )
        
        else:
            self.demucsWorker.audio = param["audio"]
            self.demucsWorker.stems = param["stems"]
            self.demucsWorker.segment = param["segment"]
            self.demucsWorker.overlap = param["overlap"]
            self.demucsWorker.output_path = param["output_path"]
        
        self.demucsWorker.signal_vr_over.connect(self.demucs_process_over)
        self.demucsWorker.file_process_status.connect(self.demucs_file_process_status)

        self.setStateTool(self.__tr("Demucs"), self.__tr("音轨分离"), False)
        self.demucsWorker.start()

        self.page_demucs.process_button.setText(self.__tr("取消"))
        self.page_demucs.process_button.setIcon(":/resource/Image/Cancel_red")


    def getDemucsParams(self):
        demucs_param = {}
        output_path = self.page_demucs.outputGroupWidget.LineEdit_output_dir.text().strip()
        demucs_param["output_path"] = output_path

        overlap = self.page_demucs.demucs_param_widget.spinBox_overlap.value()
        demucs_param["overlap"] = overlap

        segment = self.page_demucs.demucs_param_widget.spinBox_segment.value()
        demucs_param["segment"] = segment

        stems = self.page_demucs.demucs_param_widget.comboBox_stems.currentText()
        demucs_param["stems"] = stems

        audio = self.page_demucs.fileListView.avFileList
        demucs_param["audio"] = audio

        return demucs_param

    def singleAndSlotProcess(self):
        """
        process single connect and others
        """
        # TODO: there is too much function be writen in this file, 
        # and they are not all must be here, 
        # some of them could be in their own class-code file
        self.statusToolSignalStore.LoadModelSignal.connect(self.loadModelResult)
        self.statusToolSignalStore.LoadModelSignal.connect(self.setModelStatusLabelTextForAll)

        self.page_model.toolPushButton_get_model_path.clicked.connect(self.getLocalModelPath)
        self.page_model.button_convert_model.clicked.connect(self.onButtonConvertModelClicked)
        set_model_output_dir = lambda path: path if path != "" else self.page_model.LineEdit_model_out_dir.text()
        self.page_model.button_set_model_out_dir.clicked.connect(lambda:self.page_model.LineEdit_model_out_dir.setText(set_model_output_dir(QFileDialog.getExistingDirectory(self,"选择转换模型输出目录", self.page_model.LineEdit_model_out_dir.text()))) )
        self.page_model.button_download_root.clicked.connect(self.getDownloadCacheDir)
        self.page_model.button_model_lodar.clicked.connect(self.onModelLoadClicked)
        self.page_process.button_process.clicked.connect(self.onButtonProcessClicked)
        self.page_process.processResultText.textChanged.connect(lambda: self.page_process.processResultText.moveCursor(QTextCursor.MoveOperation.End, mode=QTextCursor.MoveMode.MoveAnchor))

        self.page_output.outputSubtitleFileButton.clicked.connect(self.outputSubtitleFile)
        self.page_output.WhisperXAligmentTimeStampleButton.clicked.connect(self.whisperXAligmentTimeStample)
        self.page_output.WhisperXSpeakerDiarizeButton.clicked.connect(self.whisperXDiarizeSpeakers)
        self.page_output.tableTab.tabBar.tabAddRequested.connect(self.openExcitedFiles)

        self.page_home.itemLabel_demucs.mainButton.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_demucs))
        self.page_home.itemLabel_faster_whisper.mainButton.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_process))
        self.page_home.itemLabel_whisperx.mainButton.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_output))
        self.page_home.itemLabel_faster_whisper.subButton.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.page_transcribes))

        self.page_demucs.process_button.clicked.connect(self.demucsProcess)

    def closeEvent(self, event) -> None:
        """
        点击窗口关闭按钮时的事件响应
        """

        messageBoxW = MessageBox(self.__tr('退出'), self.__tr("是否要退出程序？"), self)
        if messageBoxW.exec():
            self.use_auth_token_speaker_diarition = self.page_VAD.LineEdit_use_auth_token.text() if (self.use_auth_token_speaker_diarition != self.page_VAD.LineEdit_use_auth_token.text() and self.page_VAD.LineEdit_use_auth_token.text() != "") else self.use_auth_token_speaker_diarition
            
            overlap = self.page_demucs.demucs_param_widget.spinBox_overlap.value()
            segment = self.page_demucs.demucs_param_widget.spinBox_segment.value()

            with open(r'./fasterWhisperGUIConfig.json','w',encoding='utf8')as fp:
                json.dump(
                            {"use_auth_token":self.use_auth_token_speaker_diarition,
                            "overlap":overlap,
                            "segment":segment
                        },
                            fp,
                            ensure_ascii=False
                        )
            
            # 如果关键进程仍在运行 结束进程
            if self.transcribe_thread is not None and self.transcribe_thread.is_running:
                self.transcribe_thread.requestInterruption()
                self.transcribe_thread.stop()
            
            if self.whisperXWorker is not None and self.whisperXWorker.is_running:
                self.whisperXWorker.requestInterruption()
                self.whisperXWorker.stop()
            
            if self.outputWorker is not None and self.outputWorker.is_running:
                self.outputWorker.requestInterruption()
                self.outputWorker.stop()
            
            if self.demucsWorker is not None and self.demucsWorker.is_running:
                self.demucsWorker.requestInterruption()
                self.demucsWorker.stop()
            
            # 退还系统错误输出 和标准输出
            sys.stderr = sys.__stderr__
            sys.stdout = sys.__stdout__

            # 关闭日志文件 结束全部流
            self.log.close()

            # TODO:从内存或显存中手动卸除模型时，程序崩溃，该异常与 C++ 2015 运行时环境有关，
            # 尝试替换该运行时库的系统文件，该功能正常运行，但系统不能再正常开机，
            # 怀疑需要全面升级所有 C++ 运行时环境，暂时作罢
            # del self.FasterWhisperModel

            # 接受退出事件，程序正常退出
            event.accept()
        else:
            event.ignore()
    
    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self.stateTool is not None:
            width_tool = self.stateTool.width()
            width = self.width()
            self.stateTool.move(width-width_tool-30, 45)
        return 
    