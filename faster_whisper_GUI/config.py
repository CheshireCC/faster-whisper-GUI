# coding:utf-8
default_Huggingface_user_token = "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"

Language_without_space = ["ja","zh","ko","yue"]
Language_dict = {
                "en": "english",
                "zht": "Traditional Chinese",
                "zhs": "Simplified Chinese ",
                "yue": "cantonese",
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

Preciese_list = ['int8',
                'int8_float16',
                'int8_bfloat16',
                'int16',
                'float16',
                'float32',
                'bfloat16'
            ]

Model_names = [
                "tiny", 
                "tiny.en", 
                "base", 
                "base.en", 
                "small", 
                "small.en", 
                "medium", 
                "medium.en", 
                "large-v1", 
                "large-v2",
                "large-v3",
                "large-v3-turbo",
                "distil-large-v3",
                "distil-large-v2",
                "distil-medium.en",
                "distil-small.en",
            ]

Device_list = ["cpu", "cuda", "auto"]
Task_list = ["transcribe" , "translate"]

STR_BOOL = {"False" : False, "True" : True}

SUBTITLE_FORMAT = ["ASS", "JSON", "LRC", "SMI", "SRT", "TXT", "VTT"]

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

STEMS = [
            "All Stems", 
            "Vocals", 
            "Other",
            "Bass", 
            "Drums", 
            "Vocals and Others dichotomy"
        ]

ENCODING_DICT = {"UTF-8":"utf8", 
                    "UTF-8 BOM":"utf_8_sig", 
                    "GBK":"gbk", 
                    "GB2312":"gb18030", 
                    "ANSI":"ansi"
                }

THEME_COLORS = [
    "#009faa",
    "#81D8CF",
    "#ff009f",
    "#84BE84",
    "#aaff00",
    "#FF9500",
    "#00CD00",
    "#DB4437",
    "#23CD5E",
    "#E61D34",
    "#00FF00",
    "#FF00FF",
    "#1ABC9C",
    "#FF3300",
    "#FFFF00",
    "#FFC019",
    "#FF6600",
    "#00FFFF",
    "#FF7A1D",
    "#E71A1B",
    "#FF8800",
    "#3388FF",
    "#F4B400",
    "#0069B7",
    "#FFCC00",
    "#0078D4",
]

tableItem_dark_warning_BackGround_color = "#50ffff00" # QColor(255,255,0, a=80)
tableItem_light_warning_BackGround_color  = "#50ff0000" # QColor(255,0,0,a=127)
