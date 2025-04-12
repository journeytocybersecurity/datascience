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
        newlis=[("<s>"+" "+sentence.rstrip()+" "+"</s>\n").split() for sentence in lis]       
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
        for sentence in newlis:
            for word in sentence:
                if "</s>"!=word: 
                    bigram_counts[word][sentence[sentence.index(word)+1]]+=1#defaultdict를 이용해 모든 딕셔너리의 value를 0으로 만들고 하나씩 더하기. 
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