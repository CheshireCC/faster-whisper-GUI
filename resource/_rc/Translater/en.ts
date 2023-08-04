<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="en_US" sourcelanguage="zh_CN">
<context>
    <name></name>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="641"/>
        <source>选择模型文件所在的文件夹</source>
        <translatorcomment>Tencent trnaslater </translatorcomment>
        <translation>Select the folder where the model file is located</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="673"/>
        <source>选择缓存文件夹</source>
        <translatorcomment>Tencent trnaslater </translatorcomment>
        <translation>Select cache folder</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="682"/>
        <source>选择音频文件</source>
        <translation>Select Target File</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="801"/>
        <source>模型未加载！进程退出</source>
        <translatorcomment>Tencent translater</translatorcomment>
        <translation>The model has not been loaded</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="805"/>
        <source>需要有效的音频文件！</source>
        <translatorcomment>Tencent translater</translatorcomment>
        <translation>A valid file is required!</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="950"/>
        <source>必须选择在线模型时才能使用本功能</source>
        <translation>Please Select Onlie-Model Mode</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="960"/>
        <source>模型转换：</source>
        <translation>Convert Model:</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="968"/>
        <source>
输出目录是必须的！</source>
        <translation>
Output directory is required!</translation>
    </message>
</context>
<context>
    <name>mainWin</name>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="94"/>
        <source>模型参数</source>
        <translation>Model Option</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="96"/>
        <source>VAD 参数</source>
        <translation>VAD Option</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="98"/>
        <source>转写参数</source>
        <translation>Transcribe Option</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="100"/>
        <source>执行转写</source>
        <translation>Process</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="187"/>
        <source>目标音频文件</source>
        <translation>Target File</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="191"/>
        <source>要转写的音频文件路径</source>
        <translation>Target File</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="196"/>
        <source>选择要转写的音频文件</source>
        <translation>Target File</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="205"/>
        <source>语言</source>
        <translation>Language</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="215"/>
        <source>音频中的语言。如果选择 Auto，则自动在音频的前30秒内检测语言。</source>
        <translation>The language spoken in the audio.If set &quot;Auto&quot;,
 the language will be detected in the first 30 seconds of audio.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="226"/>
        <source>翻译为英语</source>
        <translation>Translate</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="230"/>
        <source>输出转写结果翻译为英语的翻译结果</source>
        <translation>Translate result to English</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="234"/>
        <source>分块大小</source>
        <translation>beam_size</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="237"/>
        <source>用于解码的音频块的大小。</source>
        <translation>Beam size to use for decoding.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="241"/>
        <source>最佳热度</source>
        <translation>best_of</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="244"/>
        <source>采样时使用非零热度的候选数</source>
        <translation>Number of candidates when sampling with non-zero temperature</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="248"/>
        <source>搜索耐心</source>
        <translation>patience</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="250"/>
        <source>搜索音频块时的耐心因子</source>
        <translation>Beam search patience factor</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="255"/>
        <source>惩罚常数</source>
        <translation>length_penalty</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="258"/>
        <source>指数形式的长度惩罚常数</source>
        <translation>Exponential length penalty constant</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="262"/>
        <source>采样热度候选</source>
        <translation>temperature</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="265"/>
        <source>采样的温度。
当程序因为压缩比参数或者采样标记概率参数失败时会依次使用</source>
        <translation>Temperature for sampling. It can be a tuple of temperatures,
            which will be successively used upon failures according to either
            `compression_ratio_threshold` or `log_prob_threshold`</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="270"/>
        <source>gzip 压缩比阈值</source>
        <translation>compression_ratio_threshold</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="273"/>
        <source>如果音频的gzip压缩比高于此值，则视为失败。</source>
        <translation>If the gzip compression ratio is above this value, treat as failed.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="277"/>
        <source>采样概率阈值</source>
        <translation>log_prob_threshold</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="280"/>
        <source>如果采样标记的平均对数概率阈值低于此值，则视为失败</source>
        <translation>If the average log probability over sampled tokens is below this value, treat as failed</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="284"/>
        <source>静音阈值</source>
        <translation>no_speech_threshold</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="287"/>
        <source>音频段的如果非语音概率高于此值，
并且对采样标记的平均对数概率低于阈值，
则将该段视为静音。</source>
        <translation>If the no_speech probability is higher than this value AND
the average log probability over sampled tokens is below `log_prob_threshold`,
consider the segment as silent.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="291"/>
        <source>循环提示</source>
        <translation>condition_on_previous_text</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="295"/>
        <source>如果启用，则将模型的前一个输出作为下一个音频段的提示;
禁用可能会导致文本在段与段之间不一致，
但模型不太容易陷入失败循环，
比如重复循环或时间戳失去同步。</source>
        <translation>If True, the previous output of the model is provided
as a prompt for the next window; disabling may make the text inconsistent across
windows, but the model becomes less prone to getting stuck in a failure loop,
such as repetition looping or timestamps going out of sync.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="299"/>
        <source>初始提示词</source>
        <translation>initial_prompt</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="301"/>
        <source>为第一个音频段提供的可选文本字符串或词元 id 提示词，可迭代项。</source>
        <translation>Optional text string or iterable of token ids to provide as a prompt for the first window.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="305"/>
        <source>初始文本前缀</source>
        <translation>prefix</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="307"/>
        <source>为第初始音频段提供的可选文本前缀。</source>
        <translation>Optional text to provide as a prefix for the first window.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="311"/>
        <source>空白抑制</source>
        <translation>suppress_blank</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="315"/>
        <source>在采样开始时抑制空白输出。</source>
        <translation>Suppress blank outputs at the beginning of the sampling.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="319"/>
        <source>特定标记抑制</source>
        <translation>suppress_tokens</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="322"/>
        <source>要抑制的标记ID列表。 
-1 将抑制模型配置文件 config.json 中定义的默认符号集。</source>
        <translation>List of token IDs to suppress. -1 will suppress a default set
of symbols as defined in the model config.json file.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="326"/>
        <source>关闭时间戳</source>
        <translation>without_timestamps</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="330"/>
        <source>开启时将会仅输出文本不输出时间戳</source>
        <translation>Only sample text tokens</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="334"/>
        <source>最晚初始时间戳</source>
        <translation>max_initial_timestamp</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="337"/>
        <source>首个时间戳不能晚于此时间。</source>
        <translation>The initial timestamp cannot be later than this.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="342"/>
        <source>单词级时间戳</source>
        <translation>word_timestamps</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="346"/>
        <source>用交叉注意力模式和动态时间规整提取单词级时间戳，
并在每个段的每个单词中包含时间戳。</source>
        <translation>Extract word-level timestamps using the cross-attention pattern
and dynamic time warping, and include the timestamps for each word in each segment.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="350"/>
        <source>标点向后合并</source>
        <translation>prepend_punctuations</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="353"/>
        <source>如果开启单词级时间戳，
则将这些标点符号与下一个单词合并。</source>
        <translation>If word_timestamps is True, merge these punctuation symbols with the next word.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="357"/>
        <source>标点向前合并</source>
        <translation>append_punctuations</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="360"/>
        <source>如果开启单词级时间戳，
则将这些标点符号与前一个单词合并。</source>
        <translation>If word_timestamps is True, merge these punctuation symbols with the previous word.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="378"/>
        <source>使用本地模型</source>
        <translation>Local Model</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="379"/>
        <source>本地模型需使用经过 CTranslate2 转换工具，从 OpenAI 模型格式转换而来的模型</source>
        <translation>This mode need a local model that had been converted to CTranslate2 format</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="387"/>
        <source>模型文件路径</source>
        <translation>Model files path</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="402"/>
        <source>在线下载模型</source>
        <translation>Download Model Online</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="403"/>
        <source>下载可能会花费很长时间，具体取决于网络状态，
作为参考 large-v2 模型下载量最大约 6GB</source>
        <translation>download model from https://huggingface.co/models ，
you can also access this and download model by yourself</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="410"/>
        <source>模型名称</source>
        <translation>Model Name</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="428"/>
        <source>处理设备：</source>
        <translation>Device:</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="438"/>
        <source>设备号：</source>
        <translation>device_index:</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="441"/>
        <source>要使用的设备ID。也可以通过传递ID列表(例如0,1,2,3)在多GPU上加载模型。</source>
        <translation>ID of device that you want to use,
it support multi-value, just like: 0,1,2 .</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="449"/>
        <source>计算精度：</source>
        <translation>compute_type:</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="454"/>
        <source>要使用的计算精度，尽管某些设备不支持半精度，
但事实上不论选择什么精度类型都可以隐式转换。
请参阅 https://opennmt.net/CTranslate2/quantization.html。</source>
        <translation>Type to use for computation.
See https://opennmt.net/CTranslate2/quantization.html.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="460"/>
        <source>线程数（CPU）</source>
        <translation>cpu_threads ( CPU )</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="463"/>
        <source>在CPU上运行时使用的线程数(默认为4)。非零值会覆盖</source>
        <translation>Number of threads to use when running on CPU (4 by default).
A non zero value overrides the OMP_NUM_THREADS environment variable</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="469"/>
        <source>并发数</source>
        <translation>num_workers</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="472"/>
        <source>具有多个工作线程可以在运行模型时实现真正的并行性。
这可以以增加内存使用为代价提高整体吞吐量。</source>
        <translation>When transcribe() is called from multiple Python threads,
having multiple workers enables true parallelism when running the model
This can improve the global throughput at the cost of increased memory usage.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="478"/>
        <source>下载缓存目录</source>
        <translation>download_root</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="481"/>
        <source>模型下载保存的目录。如果未修改,
则模型将保存在标准Hugging Face缓存目录中。</source>
        <translation>Directory where the models should be saved. If not set, the models
are saved in the standard Hugging Face cache directory.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="490"/>
        <source>是否使用本地缓存</source>
        <translation>local_files_only</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="494"/>
        <source>如果为True，在本地缓存的文件存在时返回其路径，不再重新下载文件。</source>
        <translation>If True, avoid downloading the file and return the path to the local cached file if it exists.
It&apos;s a force item for load model,but a Optional item for convert model.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="503"/>
        <source>模型输出目录</source>
        <translation>Convert Model to</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="507"/>
        <source>转换模型的保存目录，不会自动创建子目录</source>
        <translation>Convert model to this path</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="511"/>
        <source>转换模型</source>
        <translation>Convert Model</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="512"/>
        <source>转换 OpenAi 模型到本地格式，
必须选择在线模型</source>
        <translation>Convert OpenAI whisper model to faster-whisper model format</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="520"/>
        <source>加载模型</source>
        <translation>Load Model</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="540"/>
        <source>是否启用 VAD 及 VAD 参数</source>
        <translation>VAD Use</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="542"/>
        <source>VAD 模型常用来对语音文件的空白段进行筛除, 可以有效减小 Whsiper 模型幻听</source>
        <translation>Use VAD Model to preprocess data or not</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="554"/>
        <source>阈值</source>
        <translation>threshold</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="557"/>
        <source>语音阈值。
 Silero VAD为每个音频块输出语音概率,概率高于此值的认为是语音。
最好对每个数据集单独调整此参数,
但“懒散”的0.5对大多数数据集来说都非常好。</source>
        <translation>Speech threshold. Silero VAD outputs speech probabilities for each audio chunk,
probabilities ABOVE this value are considered as SPEECH. It is better to tune this
parameter for each dataset separately, but &quot;lazy&quot; 0.5 is pretty good for most datasets.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="563"/>
        <source>最小语音持续时间(ms)</source>
        <translation>min_speech_duration (ms)</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="566"/>
        <source>短于该参数值的最终语音块会被抛弃。</source>
        <translation>Final speech chunks shorter min_speech_duration_ms are thrown out.
max_speech_duration_s: Maximum duration of speech chunks in seconds. Chunks longer
than max_speech_duration_s will be split at the timestamp of the last silence that
lasts more than 100ms (if any), to prevent aggressive cutting. Otherwise, they will be
split aggressively just before max_speech_duration_s.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="572"/>
        <source>最大语音块时长(s)</source>
        <translation>max_speech_duration (s)</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="575"/>
        <source>语音块的最大持续时间(秒)。
比该参数值指定时长更长的块将在最后一个持续时间超过100ms的静音时间戳拆分(如果有的话),
以防止过度切割。
否则,它们将在参数指定值的时长之前强制拆分。</source>
        <translation>Maximum duration of speech chunks in seconds. Chunks longer
than max_speech_duration_s will be split at the timestamp of the last silence that
lasts more than 100ms (if any), to prevent aggressive cutting. Otherwise, they will be
split aggressively just before max_speech_duration_s.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="582"/>
        <source>最小静息时长(ms)</source>
        <translation>min_silence_duration (ms)</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="585"/>
        <source>在每个语音块结束时等待该参数值指定的时长再拆分它。</source>
        <translation>In the end of each speech chunk wait for min_silence_duration_ms before separating it.</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="592"/>
        <source>采样窗口大小</source>
        <translation>window_size_samples</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="596"/>
        <source>指定大小的音频块被馈送到silero VAD模型。
警告!
Silero VAD模型使用16000采样率训练得到512,1024,1536样本。
其他值可能会影响模型性能!</source>
        <translation>Audio chunks of window_size_samples size are fed to the silero VAD model.
WARNING! Silero VAD models were trained using 512, 1024, 1536 samples for 16000 sample rate.
Values other than these may affect model performance!!</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="602"/>
        <source>语音块前后填充</source>
        <translation>speech_pad (ms)</translation>
    </message>
    <message>
        <location filename="faster_whisper_GUI/UI_MainWindows.py" line="605"/>
        <source>最终的语音块前后都由指定时长的空白填充。</source>
        <translation>Final speech chunks are padded by speech_pad_ms each side.</translation>
    </message>
</context>
</TS>
