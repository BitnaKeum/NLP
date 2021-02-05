#-*- coding: utf-8 -*-

from summa.summarizer import summarize
from summa import keywords
from konlpy.tag import Komoran


# 핵심 단어와 핵심 문장 추출 (기사와 같이 문장 끝마다 .이 찍혀있어야 함)
def Get_key(sentence):
    key_sent = summarize(sentence, ratio=0.1)   # ratio는 전체 문장 수에 비례하여 추출할 핵심 문장의 비율
    key_word = keywords.keywords(sentence, ratio=0.2)  # 핵심 단어 15개 추출

    key_sent_noun = Morpheme(key_sent)  # 핵심 문장에서 명사만 추출
    key_word_noun = Morpheme(key_word)  # 핵심 단어에서 명사만 추출


    # 핵심 문장의 명사 단어 중 핵심 단어의 명사 단어와 겹치는 것의 빈도 수 측정
    word_cnt = {}
    for noun in key_sent_noun:
        if noun in key_word_noun:
            if noun in word_cnt.keys():
                word_cnt[noun] += 1
            else:
                word_cnt[noun] = 1

    # 빈도 수가 높은 순서로 정렬
    sorted_word_cnt = sorted(word_cnt.items(), reverse=True, key=lambda item: item[1])  # 리스트

    num = min(5, len(sorted_word_cnt))      # 핵심 단어는 최대 5개
    final_key_word = []
    final_key_word.append([sorted_word_cnt[i][0] for i in range(num)])
    final_key_word = final_key_word[0]
    #print("final: ", final_key_word)

    final_key_sentence = key_sent.split('.')[0]     # 핵심 문장은 1개

    return final_key_sentence, final_key_word
