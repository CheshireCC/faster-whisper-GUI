# coding:utf-8
default_Huggingface_user_token = "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"

Language_without_space = ["ja","zh","ko","yue"]
Language_dict = {
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
                "yue": "cantonese"
            }

Preciese_list = ['int8',
                'int8_float16',
                'int8_bfloat16',
                'int16',
                'float16',
                'float32',
                'bfloat16'
            ]

Model_names = ["tiny", "tiny.en", "base", "base.en", "small", 
                "small.en", "medium", "medium.en", "large-v1", "large-v2","large-v3"]

Device_list = ["cpu", "cuda", "auto"]
Task_list = ["transcribe" , "translate"]

STR_BOOL = {"False" : False, "True" : True}

SUBTITLE_FORMAT = ["SRT", "TXT", "VTT", "LRC", "SMI"]

CAPTURE_PARA = [
    {"rate": 44100
    ,"channel": 2
    ,"dType": 16
    ,"quality": "CD Quality"
    },
    {"rate": 48000
    ,"channel": 2
    ,"dType": 16
    ,"quality": "DVD Quality"
    },
    {"rate": 44100
    ,"channel": 2
    ,"dType": 24
    ,"quality": "Studio Quality"
    },
    {"rate": 48000
    ,"channel": 2
    ,"dType": 24
    ,"quality": "Studio Quality"
    }
]

STEMS = ["All Stems","Vocals", "Other","Bass", "Drums"]
ENCODING_DICT = {"UTF-8":"utf8", 
                    "UTF-8 BOM":"utf_8_sig", 
                    "GBK":"gbk", 
                    "GB2312":"gb18030", 
                    "ANSI":"ansi"
                }
