# coding:utf-8
import os
from PySide6.QtCore import QThread, Signal
from torchaudio.pipelines import HDEMUCS_HIGH_MUSDB_PLUS
import torch
from torchaudio.transforms import Fade
import av
import soundfile
import numpy as np
import gc

from faster_whisper import decode_audio

from .config import STEMS


class DemucsWorker(QThread):

    signal_vr_over = Signal(bool)
    file_process_status = Signal(dict)

    def __init__(
                    self, parent, 
                    audio:list[str],
                    stems:str,
                    model_path:str,
                    *,
                    segment:float=10,
                    overlap:float=0.1,
                    sample_rate:int=44100,
                    output_path:str=""
                    ) -> None:
        
        super().__init__(parent)
        self.is_running = False
        self.model_path = model_path
        self.model = None
        self.audio = audio
        self.sampleRate = sample_rate
        self.segment = segment
        self.overlap = overlap
        self.stems = stems
        self.output_path = output_path


    def run(self) -> None:
        self.is_running = True

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"device: {device}")

        if not self.is_running:
            return
        
        self.file_process_status.emit({"file":"", "status":False, "task": "load model"})
        if self.model is None:
            try:
                self.loadModel(self.model_path, device=device)
            except Exception as e:
                print(f"load model error: \n{str(e)}")
                self.signal_vr_over.emit(False)
                self.stop()

        for audio in self.audio:
            
            if not self.is_running:
                del samples
                del sources
                del audio
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                print("exit")
                return
            
            self.file_process_status.emit({"file":audio, "status":False, "task": "reasmple audio"})
            print(f"current task: {audio}")
            print("reasmple audio...")

            try:
                samples = self.reSampleAudio(audio, 44100, device=device)
                samples = np.asarray(samples)
                print("samples shape: ", samples.shape)
                # samples = torch.tensor(samples,dtype=torch.float32).to(device)
            except Exception as e:
                print(f"resample audio error:\n{str(e)}")
                self.signal_vr_over.emit(False)
                self.stop()

            if not self.is_running:
                del samples
                del audio
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                print("exit")
                return
            
            print("separate sources...")
            self.file_process_status.emit({"file":audio, "status":False, "task": "separate sources"})

            try:
                sources = self.separate_sources(
                                                self.model, 
                                                samples[None], 
                                                self.segment, 
                                                self.overlap, 
                                                device, 
                                                self.sampleRate
                                            )
            except Exception as e:
                print(f"\nseparate audio sources error:\n    {str(e)}")
                self.signal_vr_over.emit(False)
                self.stop()

            if (sources is None) or (not self.is_running):
                print("exit")
                del samples
                del sources
                del audio
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                return
            
            self.file_process_status.emit({"file":audio, "status":False, "task": "save files"})
            print("save files...")

            try:
                self.saveResult(
                                sources=sources, 
                                file_path=audio, 
                                model=self.model, 
                                stems=self.stems, 
                                output_path=self.output_path
                            )
                
            except Exception as e:
                print(f"save audio file error:\n{str(e)}")
                self.signal_vr_over.emit(False)
                self.stop()

            if not self.is_running:
                print("exit")
                del samples
                del sources
                del audio
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                return

            self.file_process_status.emit({"file":audio, "status":False, "task": "file over"})
            del samples
            del sources
            del audio
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
        self.signal_vr_over.emit(True)
        print("over!")
        
        # self.model.to("cpu")
        del self.model
        self.model = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        # print(torch.cuda.memory_allocated(device=device))
        # print(torch.cuda.memory_reserved())
        # print(torch.cuda.memory_stats(device=device))
    
        gc.collect()

        self.requestInterruption()
        self.stop()

    
    def stop(self):
        self.is_running = False

    def separate_sources(self,
                        model,
                        mix,
                        segment=10.0,
                        overlap=0.1,
                        device=None,
                        sample_rate=44100,
                    ):
        """
        Apply model to a given mixture. Use fade, and add segments together in order to add model segment by segment.

        Args:
            segment (int): segment length in seconds
            device (torch.device, str, or None): if provided, device on which to
                execute the computation, otherwise `mix.device` is assumed.
                When `device` is different from `mix.device`, only local computations will
                be on `device`, while the entire tracks will be stored on `mix.device`.
        """
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
        else:
            device = device

        batch, channels, length = mix.shape

        chunk_len = int(sample_rate * segment * (1 + overlap))
        start = 0
        end = chunk_len
        overlap_frames = overlap * sample_rate
        fade = Fade(fade_in_len=0, fade_out_len=int(overlap_frames), fade_shape="linear")

        final = torch.zeros(batch, len(model.sources), channels, length, device=device)

        while start < length - overlap_frames:
            if not self.is_running:
                return None
            
            chunk = mix[:, :, start:end]
            chunk = torch.tensor(chunk, dtype=torch.float32).to(device)
            with torch.no_grad():
                out = model.forward(chunk)

            if not self.is_running:
                return None
            
            out = fade(out)
            final[:, :, :, start:end] += out
            if start == 0:
                fade.fade_in_len = int(overlap_frames)
                start += int(chunk_len - overlap_frames)
            else:
                start += chunk_len
            end += chunk_len
            if end >= length:
                fade.fade_out_len = 0

            del out
            del chunk
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        # del model
        
        del fade
        del mix
        return final

    def loadModel(self, model_path:str, device=None):

        download_path = os.path.abspath(model_path)
        print(f"download_path: {download_path}")

        if os.path.exists(download_path):
            print("found existed model file")
        else:
            self.file_process_status.emit({"file":"","status":False,"task":"download model"})

        bundle = HDEMUCS_HIGH_MUSDB_PLUS
        bundle._model_path = download_path
        bundle._sample_rate = 44100

        sample_rate = bundle.sample_rate
        print(f"Sample rate: {sample_rate}")

        if not self.is_running:
            return

        self.model = bundle.get_model()

        if not self.is_running:
            return
        
        del bundle
        self.model.to(device)

    def reSampleAudio(self, audio, sample_rate, device) -> np.ndarray:
        file_path = os.path.abspath(audio)

        split_setore = True
        with av.open(file_path) as av_file:
            stream_ = next(s for s in av_file.streams if s.codec_context.type == 'audio')
            audio_channel_num = stream_.channels
            if audio_channel_num < 2:
                print("单声道音频")
                split_setore = False
            else:
                print("双声道音频")

        print("resample audio data")
        samples = decode_audio(file_path, sample_rate, split_setore)
        # samples = np.array(samples)

        # samples_t = torch.tensor(samples,dtype=torch.float32).to(device)
        # del samples
        return samples
    
    def saveResult(self, model, file_path:str, sources:torch.Tensor, stems:str, output_path:str, sample_rate=44100):


        sources_list = model.sources
        print(f"sources_list: {sources_list}")
        # print(stems.lower() in sources_list)
        # print(stems.lower())
        # print(stems.lower()==sources_list[-1])
        # print(sources.shape)

        sources = list(sources[0])

        audios = dict(zip(sources_list, sources))


        data_dir,file_output = os.path.split(file_path)
        
        file_output = file_output.split(".")
        file_output = file_output[:-1]

        if stems.lower() == "all stems":
            stems = STEMS[1:]
        
        else:
            stems = [stems]
        
        if not output_path:
            output_path = data_dir

        # if not os.path.exists(output_path):
        #     os.mkdir(output_path)

        for stem in stems:
            spec = audios[stem.lower()][:, :].cpu()
            output_path_ = os.path.join(output_path, stem)
            if not os.path.exists(output_path_):
                print(f"create output folder: {stem}")
                os.makedirs(output_path_)
            
            output_fileName = os.path.join(output_path_, ".".join(file_output+[f"_{stem.lower()}", "wav"]))
            print(f"save file: {output_fileName}")

            soundfile.write(output_fileName, spec.numpy().T,  sample_rate)
        
