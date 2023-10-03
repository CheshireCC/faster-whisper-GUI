import json
from pathlib import Path
import sys
import os
import time
from threading import Thread

from PySide6.QtWidgets import (
                                QFileDialog
                                , QMessageBox
                            )

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
                        )

from .config import (
                    Language_dict
                    # , Preciese_list
                    # , Model_names
                    # , Device_list
                    , Task_list
                    , STR_BOOL
                    # , SUBTITLE_FORMAT
                    , CAPTURE_PARA
                )

from .modelLoad import loadModel
from .convertModel import ConvertModel
from .transcribe import (
                        TranscribeWorker
                        , AudioStreamTranscribeWorker
                        , CaptureAudioWorker
                    )
from .UI_MainWindows import UIMainWin

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
    
    log = open(r"./fasterwhispergui.log" ,"a" ,encoding="utf8")

    def __init__(self):
        
        # 重定向输出
        self.redirectErrOutpur = RedirectOutputSignalStore()
        self.redirectErrOutpur.outputSignal.connect(lambda text: self.log.write(text))
        # self.redirectErrOutpur.outputSignal.connect(self.writeLog)
        # self.redirectErrOutpur.outputSignal.connect(lambda text: Thread(target=self.log.write, args=(text)).start())
        sys.stderr = self.redirectErrOutpur
        sys.stdout = self.redirectErrOutpur

        super().__init__()

        self.transcribe_thread = None
        self.audio_capture_thread = None
        self.stateTool = None

        self.statusToolSignalStore = statusToolsSignalStore()

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
    
    def getFileName(self):
        """
        get a file name from a dialog
        """
        fileNames, _ = QFileDialog.getOpenFileNames(self, self.__tr("选择音频文件"), r"./", "All file type(*.*);;Wave file(*.wav);;MPEG 4(*.mp4)")
        if fileNames:
            self.page_process.LineEdit_audio_fileName.setText(";;".join(fileNames))
        else:
            return

        rootDir = Path(fileNames[0]).absolute().resolve().parent.as_posix()
        self.page_process.LineEdit_output_dir.setText(rootDir)
    
    # ==============================================================================================================
    # 废弃 将在下一个版本删除
    # ==============================================================================================================
    def setTextAndMoveCursorToModelBrowser(self, text:str):
        self.modelLoderBrower.moveCursor(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
        self.modelLoderBrower.insertPlainText(text)

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
        # self.modelLoderBrower.setText("")

        # 重定向输出
        # self.redirectOutput(self.setTextAndMoveCursorToModelBrowser)
        self.log.write("\n==========LoadModel==========\n")
        
        model_param = self.getParam_model()
        for key, value in model_param.items():
            print(f"{key}: {value}")

        model_size_or_path = model_param["model_size_or_path"]

        if model_size_or_path == "":
            InfoBar.warning(
                            title='',
                            content=self.__tr("需要模型所在目录或者有效的模型名称。"),
                            orient=Qt.Horizontal,
                            isClosable=True, 
                            position=InfoBarPosition.TOP_RIGHT,
                            duration=-1,
                            parent=self
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
                    orient=Qt.Vertical,    # vertical layout
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
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
        self.setStateTool("加载模型", "模型加载中，请稍候", False)

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
        self.log.write("\n==========Process==========\n")

        # 重定向输出
        self.redirectOutput(self.setTextAndMoveCursorToProcessBrowser)

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
                self.transcribeOver()
                return
            
            rate_channel_dType = self.combox_capture.currentIndex()
            rate_channel_dType : dict = CAPTURE_PARA[rate_channel_dType]
            rate = rate_channel_dType["rate"]
            channels = rate_channel_dType["channel"]
            dType = rate_channel_dType["dType"]

            # if dType == 16:
            #     dType = "int16"
            # elif dType == 24:
            #     dType = "int24"

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
        is_WhisxperX_TimeStampel_alignment_avilible = False
        if self.page_VAD.timeStampleAlignment_check.isChecked():
            is_WhisxperX_TimeStampel_alignment_avilible = True
        
        dict_WhisperXParams["alignment"] = is_WhisxperX_TimeStampel_alignment_avilible

        is_WhisxperX_Speaker_Diarize_avilible = False
        if self.page_VAD.speakerDiarize_check.isChecked():
            is_WhisxperX_Speaker_Diarize_avilible = True
        
        dict_WhisperXParams["speakerDiarize"] = is_WhisxperX_Speaker_Diarize_avilible

        if is_WhisxperX_Speaker_Diarize_avilible:
            dict_WhisperXParams["use_auth_token"] = self.page_VAD.LineEdit_use_auth_token.text()

            dict_WhisperXParams["min_speaker"] = int(self.page_VAD.SpinBox_min_speaker.text())
            dict_WhisperXParams["max_speaker"] = int(self.page_VAD.SpinBox_max_speaker.text())

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
                InfoBar.error(
                    title=self.__tr("错误")
                    , content=self.__tr("模型未加载！")
                    , orient=Qt.Orientation.Horizontal
                    , isClosable=True
                    , duration=-1
                    , position=InfoBarPosition.TOP
                    , parent=self
                )
                self.transcribeOver()
                return
            
            # print(Transcribe_params['audio'])
            if len(Transcribe_params['audio']) == 0 and self.page_process.transceibe_Files_RadioButton.isChecked():
                print("No input files!")
                self.transcribeOver()
                return
            
            files_exist = [os.path.exists(file) for file in Transcribe_params["audio"]]
            if not all(files_exist):
                ignore_file = [file for file in Transcribe_params['audio'] if not os.path.exists(file)]
                print(self.__tr("存在无效文件："))
                new_line = "\n                    "
                print(f"  Error FilesName : {new_line.join(ignore_file)}")
                new_line = "\n                "
                print(f"  ignore files: {new_line.join(ignore_file)}")
                Transcribe_params['audio'] = [file for file in Transcribe_params['audio'] if os.path.exists(file)]
            
            try:
                num_worker = int(self.page_model.LineEdit_num_workers.text())
            except Exception as e:
                num_worker = 1
            
            whisperXParams = self.getParamWhisperX()

            print(f"WhisperX Alignment: {whisperXParams['alignment']}")
            print(f"WhisperX Speaker Diarize: {whisperXParams['speakerDiarize']}")

            if whisperXParams["speakerDiarize"]:
                print(f"  User Token: {whisperXParams['use_auth_token']}")
                print(f"  min speakers: {whisperXParams['min_speaker']}")
                print(f"  max speakers: {whisperXParams['max_speaker']}")

            self.transcribe_thread = TranscribeWorker(model = self.FasterWhisperModel
                                                    , parameters = Transcribe_params
                                                    , vad_filter = vad_filter
                                                    , vad_parameters = VAD_param
                                                    , num_workers = num_worker
                                                    , output_format = self.page_transcribes.combox_output_format.currentText()
                                                    , output_dir = self.page_process.LineEdit_output_dir.text()
                                                    , alignment=whisperXParams["alignment"]
                                                    , speaker_diarize=whisperXParams["speakerDiarize"]
                                                    , use_auth_token=whisperXParams["use_auth_token"]
                                                    , min_speaker=whisperXParams["min_speaker"]
                                                    , max_speaker=whisperXParams["max_speaker"]
                                                )
            
            self.transcribe_thread.signal_process_over.connect(self.transcribeOver)
            self.page_process.button_process.setText(self.__tr("    取消"))
            self.page_process.button_process.setIcon(r":/resource/Image/Cancel_red.svg")
            self.transcribe_thread.is_running == True
            # self.button_process.clicked.disconnect(self.onButtonProcessClicked)
            # self.button_process.clicked.connect(self.cancelTrancribe)
            self.transcribe_thread.start()
            self.setStateTool(self.__tr("音频处理"), self.__tr("正在处理中"), False)
        
        elif self.transcribe_thread is not None and self.transcribe_thread.isRunning():
            # reply = QMessageBox.question(self
            #                             , self.__tr('取消')
            #                             , self.__tr("是否取消操作？")
            #                             , QMessageBox.Yes | QMessageBox.No
            #                             , QMessageBox.No
            #                         )

            messageBoxW = MessageBox(self.__tr("取消")
                                    , self.__tr("是否取消操作？")
                                    , self)
            
            if messageBoxW.exec():
                self.button_process.setEnabled(False)
                self.cancelTrancribe()
                sys.stdout = self.redirectErrOutpur
                self.setStateTool(text=self.__tr("已取消"),status=True)
    
    def resetButton_process(self):
        self.page_process.button_process.setEnabled(True)
        self.page_process.button_process.setText(self.__tr("    开始"))
        self.page_process.button_process.setIcon(r":/resource/Image/speak-16x24.svg")
        
    def cancelTrancribe(self):
        print("Canceling...")
        self.transcribe_thread.stop()
        self.transcribeOver()
        print("【Process Canceled By User!】")
        self.resetButton_process()
        
    def audioCaptureOver(self):
        self.audio_capture_thread.stop()
        while(self.audio_capture_thread.isRunning()):
            time.sleep(0.1)
        self.audio_capture_thread = None

    def transcribeOver(self):
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
        
    def getParamTranscribe(self) -> dict:
        Transcribe_params = {}

        audio = self.page_process.LineEdit_audio_fileName.text().strip()
        audio = audio.split(";;") if audio != "" else []
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
        
        # self.modelLoderBrower.setText("")
        # 重定向输出
        # self.redirectOutput(self.setTextAndMoveCursorToModelBrowser)

        if not self.page_model.model_online_RadioButton.isChecked():
            # QMessageBox.warning(self, "错误", "必须选择在线模型时才能使用本功能", QMessageBox.Yes, QMessageBox.Yes)
            print(self.__tr("Model Convert only Work In Onlie-Mode"))
            InfoBar.error(self.__tr("错误")
                        , self.__tr("转换功能仅在在线模式下工作")
                        , orient=Qt.Orientation.Horizontal
                        , isClosable=True
                        , duration=-1
                        , position=InfoBarPosition.TOP_RIGHT
                        , parent = self
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
        if not status:
            self.stateTool = StateToolTip(title, text , self)
            width = self.width()
            self.stateTool.move(width-290, 30)
            self.stateTool.show()
        else:
            self.stateTool.setContent(text)
            self.stateTool.setState(True)
            self.stateTool = None

    def loadModelResult(self, state:bool):
        if state and self.stateTool:
            self.setStateTool(text=self.__tr("加载完成"),status=state)
            InfoBar.success(
                            title=self.__tr('加载结束'),
                            content=self.__tr("模型加载成功"),
                            orient=Qt.Horizontal,
                            isClosable=True,
                            position=InfoBarPosition.TOP,
                            # position='Custom',   # NOTE: use custom info bar manager
                            duration=-1,
                            parent=self
                        )
            
        elif not state:
            self.setStateTool(text=self.__tr("结束"), status=True)
            InfoBar.error(
                title=self.__tr("错误")
                , content=self.__tr("加载失败，退出并检查 fasterWhispergui.log 文件可能会获取错误信息。")
                , orient=Qt.Horizontal
                , isClosable=True
                , position=InfoBarPosition.TOP
                # , position='Custom',   # NOTE: use custom info bar manager
                , duration=-1
                , parent=self
            )

    def setModelStatusLabelTextForAll(self, status:bool):
        
        for page in self.pages:
            try:
                page.setModelStatusLabelText(status)
            except Exception as e:
                self.log.write(str(e))
        
    def singleAndSlotProcess(self):
        """
        process single connect and others
        """
        self.statusToolSignalStore.LoadModelSignal.connect(self.loadModelResult)
        self.statusToolSignalStore.LoadModelSignal.connect(self.setModelStatusLabelTextForAll)

        self.page_model.toolPushButton_get_model_path.clicked.connect(self.getLocalModelPath)
        self.page_model.button_convert_model.clicked.connect(self.onButtonConvertModelClicked)

        set_model_output_dir = lambda path: path if path != "" else self.page_model.LineEdit_model_out_dir.text()
        self.page_model.button_set_model_out_dir.clicked.connect(lambda:self.page_model.LineEdit_model_out_dir.setText(set_model_output_dir(QFileDialog.getExistingDirectory(self,"选择转换模型输出目录", self.page_model.LineEdit_model_out_dir.text()))) )
        self.page_model.button_download_root.clicked.connect(self.getDownloadCacheDir)

        self.page_process.fileOpenPushButton.clicked.connect(self.getFileName)

        self.page_model.button_model_lodar.clicked.connect(self.onModelLoadClicked)
        self.page_process.button_process.clicked.connect(self.onButtonProcessClicked)

        # self.modelLoderBrower.textChanged.connect(lambda: self.modelLoderBrower.moveCursor(QTextCursor.MoveOperation.End, mode=QTextCursor.MoveMode.MoveAnchor))
        self.page_process.processResultText.textChanged.connect(lambda: self.page_process.processResultText.moveCursor(QTextCursor.MoveOperation.End, mode=QTextCursor.MoveMode.MoveAnchor))
        
        set_output_file = lambda path: path if path != "" else self.LineEdit_output_dir.text()
        self.page_process.outputDirChoseButton.clicked.connect(lambda:self.page_process.LineEdit_output_dir.setText(set_output_file(QFileDialog.getExistingDirectory(self,"选择输出文件存放目录", self.page_process.LineEdit_output_dir.text()))) )


    def closeEvent(self, event) -> None:
        # reply = QMessageBox.question(self
                                #     , self.__tr('退出')
                                #     , self.__tr("是否要退出程序？")
                                #     , QMessageBox.Yes | QMessageBox.No
                                #     , QMessageBox.No
                                # )
        
        messageBoxW = MessageBox(self.__tr('退出'), self.__tr("是否要退出程序？"), self)
        if messageBoxW.exec():
            self.use_auth_token_speaker_diarition = self.page_VAD.LineEdit_use_auth_token.text() if (self.use_auth_token_speaker_diarition != self.page_VAD.LineEdit_use_auth_token.text() and self.page_VAD.LineEdit_use_auth_token.text() != "") else self.use_auth_token_speaker_diarition
            # if self.use_auth_token_speaker_diarition != self.page_VAD.LineEdit_use_auth_token.text() and self.page_VAD.LineEdit_use_auth_token.text() != "":
            #     self.use_auth_token_speaker_diarition = self.page_VAD.LineEdit_use_auth_token.text()

            with open(r'./fasterWhisperGUIConfig.json','w',encoding='utf8')as fp:
                json.dump({"use_auth_token":self.use_auth_token_speaker_diarition},fp,ensure_ascii=False)
            sys.stderr = sys.__stderr__
            self.log.close()
            # del self.FasterWhisperModel
            event.accept()
        else:
            event.ignore()
        
