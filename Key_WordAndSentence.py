#-*- coding: utf-8 -*-

from summa.summarizer import summarize
from summa import keywords
from konlpy.tag import Komoran
from hanspell import spell_checker
import re



# konlpy 사용 위해 java, jdk, jpype 설치 필요 => https://beausty23.tistory.com/54 참조


def Morpheme(sentence):
    komoran = Komoran()
    morphs = komoran.pos(sentence)
    #print(morphs)

    noun_morph = []
    for morph in morphs:
        if morph[1] == 'NNP':
            noun_morph.append(morph[0]) # 명사만 추출

    return noun_morph


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
    final_key_sentence = key_sent.split('.')[0]     # 핵심 문장은 1개

    return final_key_sentence, final_key_word


def Preprocessing(sentence):
    # 특수기호 제거
    pre_sentence = re.sub('[-=.><#/?:$~!^&*()_+}]', '', sentence)
    # 불필요한 글자 제거
    pre_sentence = pre_sentence.replace("ㅋ", "")
    pre_sentence = pre_sentence.replace("ㅎ", "")
    pre_sentence = pre_sentence.replace("ㅠ", "")
    pre_sentence = pre_sentence.replace("ㅜ", "")
    pre_sentence = pre_sentence.replace("ㅡ", "")
    pre_sentence = pre_sentence.replace("ㅏ", "")


    pre_result = str()
    for i in range(len(pre_sentence)//500+1):
        pre_part = pre_sentence[i*500:i*500+500]   # 500자씩 가져옴 (500 넘어가면 spell_checker 작동하지 않음)

        # 띄어쓰기 처리, 불용어 제거
        pre_dict = spell_checker.check(pre_part).as_dict()
        pre_result += pre_dict['checked']

    return pre_result



if __name__ == '__main__':
    sentence = "디지털 뉴딜(Digital New Deal)이 화두로 떠오르고 있다. 디지털 뉴딜이란 코로나19 사태 이후 경기 회복을 위해 마련된 범국가적 프로젝트다. \
                국내 산업의 디지털화를 가속하고 비대면화를 촉진시켜 디지털 기반의 일자리 창출 및 경제 혁신 가속화를 추진한다는 의미다.  이처럼 코로나19 \
                사태를 극복할 새로운 원동력으로 디지털 뉴딜 정책이 각광을 받고 있는 상황에서 지난 3일 전남대학교에서는 포스트 코로나 시대, 전환포럼 2020이 \
                개최되어 주목을 끌었다. 포스트 코로나 시대, 과학기술의 역할과 한국형 뉴딜 실현이라는 주제로 대통령직속 정책기획위원회가 주관한 이번 행사는\
                코로나19 사태 이후 전개될 시대를 전환적 관점에서 바라보면서 새로운 미래와 성장의 기회를 모색하자는 취지로 마련됐다. 포스트 코로나 시대, \
                디지털 뉴딜 정책 방향에 대해 발제를 맡은 고진 4차산업혁명위원회 위원은 디지털 뉴딜을 코로나19 사태로 인해 벌어진 경제 위기를 극복하기 위한\
                우리만의 D.N.A 기반 회복 전략이라고 정의했다. D.N.A란 데이터(Data)와 네트워크(Network), 그리고 인공지능(AI)을 뜻한다. 뉴딜(New Deal) 정책은 \
                세계 대공황 시절에 미국의 루스벨트 대통령이 위기 극복을 위해 채택한 정책이다. 대규모 공공 토목사업을 통해 일자리를 창출하는 정책으로서 당시의\
                핵심 사업장은 후버댐 건설이었다. 디지털 뉴딜은 미국의 뉴딜과 비슷하면서도 다르다. 유사한 점은 정책 추진을 통해 대규모 일자리를 창출한다는 \
                점이고, 다른 점은 토목사업이 아닌 디지털 기술을 통해 일자리를 만든다는 점이다. 뉴딜 정책의 핵심 사업장이 후버댐이라면, 디지털 뉴딜의 핵심사업은\
                데이터댐이라는 것이 고 위원의 설명이다. 데이터댐이란 공공기관이나 민간기업이 데이터를 수집하고, 이를 가공하여 쓸모 있는 정보로 재구성한 집합 \
                시스템을 가리킨다. 이를 활용하면 더 스마트한 AI를 개발할 수 있고, 기존의 굴뚝산업을 혁신산업으로 변신시킬 수도 있다. 데이터댐을 구축하려면 \
                데이터를 수집하고 이를 표준화시켜야만 한다. 또한 데이터를 가공하거나 결합시켜 새로운 데이터를 만들어내기도 한다. 이 과정은 모두 사람의 힘을\
                통해 이루어져야 하기 때문에 그 과정에서 많은 일자리가 생겨날 수밖에 없다. 데이터댐과 관련된 대표적 사례로는 최근 정부가 내년까지 조성하기로 \
                발표한 국가 바이오 데이터 스테이션(data station)을 꼽을 수 있다. 국가 바이오 데이터스테이션이란 과학기술정보통신부를 비롯한 10개 부처가 \
                R&D 사업을 통해 확보한 바이오 관련 데이터를 한곳에 모아 활용할 수 있는 데이터댐이다."
        
        
        
    print("전처리 전 : ", sent)
    pre_sent = Preprocessing(sent)
    print("전처리 후 : ", pre_sent)

    key_sent, key_word = Get_key(pre_sent)  # 핵심 문장 1개, 핵심 단어 (최대) 5개
    print("핵심 문장 : ", key_sent)
    print("핵심 단어 : ", key_word)


