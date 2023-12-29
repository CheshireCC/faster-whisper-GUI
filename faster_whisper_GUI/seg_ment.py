
from faster_whisper import  (Segment, Word)
from typing import List

class segment_Transcribe():

    def __init__(self, segment: Segment=None, start:float = 0, end: float = 0, text:str = "", words : list = None, speaker:str=None):
        if segment:
            self.start = float(segment.start)
            self.end = float(segment.end)
            self.text = segment.text
            try:
                if segment.words is not None:
                    self.words = segment.words
                else:
                    self.words = []
            except Exception:
                self.words = []
            self.speaker = None

        else:
            self.start = float(start)
            self.end = float(end)
            self.text = text
            self.words = words
            self.speaker = speaker


# ---------------------------------------------------------------------------------------------------------------------------
def segmentListToDictionaryList(segment_result:List[Segment]) -> List[dict]:
    dict_result = []
    for segment in segment_result:
        words = segment.words
        words_ = []
        if words and len(words) > 0 :
            for word in words:
                words_.append({"word":word.word, "start":word.start, "end":word.end, "score":word.probability})

        dict_result.append({"start":segment.start, "end":segment.end, "text":segment.text, "words":words_})

    return dict_result

def dictionaryListToSegmentList(dict_result:List[dict]) -> List[segment_Transcribe]:
    segment_result = []
    for item in dict_result:
        words = item['words']
        words_ = []
        if len(words)>0:
            start = 0
            end = 0
            for word in words:
                # print(word)
                try:
                    start=word['start']
                    end=word['end']
                    word=word['word']
                    probability=['score']
                    word_ = Word(start=start, end=end, word=word, probability=probability)
                except KeyError:
                    # 无时间戳的情况下只添加字幕数据 不修改其他数据
                    probability=['score']
                    word=word['word']
                    word_ = Word(start, end, word=word, probability=probability)
                words_.append(word_)
        
        # 合并掉无时间戳的单词数据
        words_c = []
        start = -1
        end = -1
        for word_ in words_:
            if start == word_.start and end == word_.end:
                words_c[-1] = Word(start,end,words_c[-1].word+word_.word, words_c[-1].probability)
            else:
                start = word_.start
                end = word_.end
                words_c.append(word_)
        try:
            segment_result.append(segment_Transcribe(start=item['start'], end=item['end'], text=item['text'], words=words_c, speaker=item["speaker"]))
        except KeyError:
            segment_result.append(segment_Transcribe(start=item['start'], end=item['end'], text=item['text'], words=words_c))

    return segment_result

def Removerepetition(result_a):
    # 清理输出结果 
    start = -1
    end = -1
    try:
        result_a_c = {"segments":[],"word_segments":result_a['word_segments']}
    except KeyError:
        result_a_c = {"segments":[]}

    for segment in result_a["segments"]:
        
        start_, end_ = segment['start'], segment['end']
        if start == start_ and end == end_:
            # result_a['segments'].remove(segment)
            pass
        else:
            # print(start, end)
            start, end = segment['start'], segment['end']
            result_a_c['segments'].append(segment)
            print(f"  [{start:.2f}s --> {end:.2f}s] {segment['text']}")
    
    return result_a_c
# ---------------------------------------------------------------------------------------------------------------------------

