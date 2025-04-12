#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle # load
import random # choice, choices
import sys
import math # log

################################################################################
# 빈도를 가중치로 적용하여 다음 단어 선택 (random.choices 사용)
# 현재 단어가 모델에 없는 경우, 유니그램에서 랜덤하게 단어 선택
def get_next_word(model, current_word):
    if current_word in model["bigram_counts"]:
        for nextword in model["bigram_counts"][current_word]:
            freq=[frequency for frequency in list(model["bigram_counts"][current_word].values())]#debugging: [current_word][nextword(이건 이미 key임)]와 같이 쓰면 안됨
            word_candidates=list(model["bigram_counts"][current_word].keys())#debugging: [current_word][nextword(이건 이미 key임)]와 같이 쓰면 안됨. key 또는 value리스트 만드려면 더 이전에 접근해야. 
            selectedword=random.choices(word_candidates,freq ,k=1)#구성요소 1개인 list 반환. 
    else:
        allwords=list(model["unigram_counts"].keys())#추가.
        selectedword=[random.choice(allwords)]#!! 위 random.choices가 list를 반환하니 이쪽도 list로 !!
    return selectedword[0]
 
                
################################################################################
# 문장의 로그 확률 계산 (로그 취한 개별 확률들의 합)
# 모델에 없는 단어 또는 단어 바이그램이 있으면 -100을 더함
def get_probability(model, sentence):
    # 로그 확률 초기화
    log_prob = 0.0
    splited=sentence.split()
    for word in splited:       
        if word in model["unigram_counts"] and word !="</s>" and [splited[(splited.index(word))+1]] in list(model["bigram_counts"][word].keys()):#!!keys,values로 만들어진 리스트는 인덱싱/슬라이싱 안됨. list()써서 변환하세요. 
            bifreq=model["bigram_counts"][word][splited[splited.index(word)+1]]
            log_prob+=math.log10(bifreq/mod["unigram_counts"][word])
        elif word=="</s>":
            break
        else:
            log_prob+=-100
    return log_prob

################################################################################
# 랜덤 문장 생성
# start_with : 생성할 문장의 시작 단어(들). 없으면 '<s>'로 초기화
def generate_sentence(model, start_with):
    if start_with=='':#!!\n을 ''로 바꾸니 이 부분에서는 디버깅 완료.  
        start="<s>"
    else:
        start=start_with   
    if ' ' in start:#공백문자 있으면 맨 마지막 단어만!
        splited=start.split()
        word=splited[-1]#마지막 단어가 word
        sentence=start
    else:
        word=start 
        sentence=word#!!공백 없을 때 앞단어가 빠지는 문제 수정(but 뒤에서 반복 돌리기 위한 공통변수 word는 유지)
    while True:#for i in range():대신 사용하여 무한루프 생성.
        sentence=sentence+" "+get_next_word(model,word)#!!단어와 단어 사이 공백 추가. 
        word=get_next_word(model,word)
        if word=="</s>":
            break
    if "<s>" in sentence:
        sentence=sentence.replace("</s>","")
        sentence=sentence.replace("<s>","")
    else:
        sentence=sentence.replace("</s>","")
    return ' '.join(sentence)

################################################################################
def load_model(model_file):
    with open(model_file, 'rb') as f:
        return pickle.load(f)
        

################################################################################
def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} model_file")
        sys.exit(1)
    
    model_file = sys.argv[1]
    model = load_model(model_file)
    
    print("2-gram 언어 모델 문장 생성기")
    
    while True:
        cmd = input("\n엔터 또는 문장 시작 단어(들) (q=종료): ")
        
        if cmd.lower() == 'q':
            print("프로그램을 종료합니다.")
            break
        else:
            print("\n<<<< 생성된 문장 >>>>")
            
            for i in range(10):
                sentence = generate_sentence(model, cmd)
                log_prob = get_probability(model, sentence)
                print(f"문장{i+1} : {sentence} (로그 확률: {log_prob:.4f})")
################################################################################
if __name__ == "__main__":
    main() 









