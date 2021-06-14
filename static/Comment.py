import os
import pickle
import string
import sys
import time
import jieba
import django
import numpy as np
from typing import List, Dict, Tuple
from keras.preprocessing import sequence
from keras.models import load_model

import datetime
import json


class CommentAnalysisSystem:
    """情感分析系统，主要分析病人评论，使用前需要初始化"""

    def __init__(self):
        self.stop_punctuation = string.punctuation + ':#0123456789，。！@#…*（）-+=】【】；：[]丶、~《》～？”' + ' ' + '\xa0' + '\n' + '\ue627' + '\r' + '\u3000'
        self.stop_list = []
        with open('LSTM_model/stopwords_list.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()  # 去除\n
                self.stop_list.append(line)
        with open('LSTM_model/dict_酒店.pkl', 'rb') as f:
            self.w2indx = pickle.load(f)  # 读取储存的数据
            self.w2vec = pickle.load(f)
        self.LSTM_model = load_model('LSTM_model/酒店_LSTM.h5')

    def single_predict(self, sentence):
        """
        输入一条单句，返回单句评分
        :param sentence: 单句
        :return: 评分，float
        """

        text = str(sentence)
        for punctuation in self.stop_punctuation:
            text = text.replace(punctuation, '')
        word_list = list(jieba.cut(text))

        for word in word_list:
            if word in self.stop_list:
                while word in word_list:
                    word_list.remove(word)

        new_sentences = []
        for word in sentence:
            new_sentences.append(np.array(self.w2indx.get(word, 0)))  # 单词转索引数字
        sentence_array = np.array([new_sentences])
        pad_sentence_array = sequence.pad_sequences(list(sentence_array), maxlen=150)
        predict_list = self.LSTM_model.predict(pad_sentence_array)
        print(sentence, predict_list[0][0])
        return predict_list[0][0]

    def multiple_predict(self, raw_sentence_list):
        """提供医生id，返回该医生的所有评价综合评分"""
        """很奇怪，输入数组的时候与输入单个句子会不一样，每生成一条评论就存一次数据库"""
        # raw_sentence_list = CommentSystem.find_all_comment(doctor_id)
        processed_text_list = []
        for text in raw_sentence_list:
            text = str(text)
            for punctuation in self.stop_punctuation:
                text = text.replace(punctuation, '')
            word_list = list(jieba.cut(text))
            for word in word_list:
                if word in self.stop_list:
                    while word in word_list:
                        word_list.remove(word)
            processed_text_list.append(word_list)

        new_sentences = []
        for sen in processed_text_list:
            new_sen = []
            for word in sen:
                new_sen.append(self.w2indx.get(word, 0))  # 单词转索引数字
            new_sentences.append(np.array(new_sen))
        sentence_array = np.array(new_sentences)  # 转numpy数组
        pad_sentence_array = sequence.pad_sequences(list(sentence_array), maxlen=150)
        predict_list = self.LSTM_model.predict(pad_sentence_array)
        predict_list = list(np.array(predict_list).reshape((len(predict_list),)))
        print(predict_list)
        return predict_list