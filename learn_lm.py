#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle # dump
from collections import defaultdict

# 2gram 언어 모델 학습
# unigram 빈도와 bigram 빈도를 리턴. unigram은 n이 1일 때!
# 문장의 앞뒤에 시작(<s>)과 끝(</s>)을 나타내는 가상의 단어를 포함해야 함
# 단어 토큰은 공백을 기준으로 분리(.split)
def learn_bigram_language_model(input_file):
    # 단어 빈도를 저장할 dictionary(각 단어별 빈도)
    unigram_counts = defaultdict(int)
    bigram_counts = {} # dictionary of dictionary
    with open(input_file,"r+") as f:
        lis=f.readlines()
        newlis=[("<s>"+" "+sentence.rstrip()+" "+"</s>\n").split() for sentence in lis]#각 문장에 시작문자 끝문자 붙인 후 단어 단위로 분해.    
        for sentence in newlis:#unigram 빈도수 계산. 
            for word in sentence:
                if word in unigram_counts:
                    unigram_counts[word]+=1#있으면, 원래 쌓인 빈도에 1 추가. 
                else:
                    unigram_counts[word]=1
                #없으면, 일단 한 번은 나온 것이므로 1을 넣는다. (이 부분 알고리즘 기억해두기)
                #defaultdict 는 기본적으로 모든 value가 0이다. 
        for sentence in newlis:
            for word in sentence:
                bigram_counts[word]=defaultdict(int)
                #일단 defaultint로 dict 안 dict의 모든 value를 0으로.
        curr_word="<s>"                
        for sentence in newlis:
            for word in sentence:
                prev_word=curr_word
                curr_word=word #처음엔 둘다 "<s>"로 같겠지만 그다음부터 1씩 차이.#같을 때에 대해서도 고려해주어야 한다. 
                #"</s>"에 이르면 sentence 가 끝나 </s>가 prev_word 가 되는 일은 없다.    
                if curr_word!="<s>":
                    bigram_counts[prev_word][curr_word]+=1#value들이 0으로 리셋된 dict 안 dict 에 공기어 빈도 추가. 
    return unigram_counts, bigram_counts
 #learn_bigram_language_model(input_file)은 두개의 딕셔너리가 들어간 tuple을 반환해야한다
################################################################################
def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input_file output_file(pickle)")#output 파일은 확장자가 p여야. 
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # 모델 학습
    unigram_counts, bigram_counts = learn_bigram_language_model(input_file)
   
    # 모델 저장
    model = {
        'unigram_counts': unigram_counts,
        'bigram_counts': bigram_counts
    }
    
    with open(output_file, 'wb') as f:
        pickle.dump(model, f)#model안의 딕셔너리들을 그대로 output_file(확장자 p)에 저장. 

################################################################################
if __name__ == "__main__":
    main() 