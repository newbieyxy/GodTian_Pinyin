# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 15:16:48 2019

@author: yxy

Offline evaluation of pinyin input method.
"""
import numpy as np
import re
from pypinyin import lazy_pinyin, NORMAL
# from py2hz_Pinyin import py2hz_Pinyin
from Pinyin2Hanzi import Pinyin2Hanzi
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--test-acc", type=str, default="top5", help="test mode: top5 or top10")
parser.add_argument("--test-mode", type=str, default="single", help="test method: single(one word) or phrase(more than one word)")
args = parser.parse_args()

def no_pinyin(ch):
    return ' '

# for debug viterbi 
def debug_test(py2hz):
    py_data = ["Da","nihaoy"]
    # 对整个词组进行测试
    test_num = 0
    # correct_num = 0
    for phrase_idx  in range(len(py_data)):
        test_num += 1
        py = "".join(py_data[phrase_idx])
        if py not in py2hz.cache:
            hz = py2hz.handle_current_input(py, 15, 15)
            py2hz.cache[py] = hz
        else:
            print("py存在cache中")
            hz = py2hz.cache[py]
    
    return None, test_num


# 测试集为多个句子，将其中的字一个一个提取出来进行测试
def single_word_test(file_path, py2hz):
    input_list = []
    expected_output_list = []
    # test_file = open(file_path, "rb")
    test_file = open(file_path)
    for line in test_file:
        is_char_low = re.match(r'[a-z\']', line[0]) 
        is_char_up = re.match(r'[A-Z\']', line[0])
        if is_char_low or is_char_up:
            input_list.append(line)
        else:
            expected_output_list.append(line)
     
    # 将测试样本中的每句话的每个中文字对应的拼音提取，用单个中文字去测试
    test_num = 0
    correct_num = 0
    viterbi_cost_time = 0.
    use_viterbi_num = 0
    for test_line_num in range(len(input_list)):
        # 整个句子的拼音
        hz_list = input_list[test_line_num].split(' ')
        for hz_idx in range(len(hz_list)):
            # 一个字的拼音
            test_num += 1
            py = [] # 单个字的测试
            if "\n" in hz_list[hz_idx]:
                hz_list[hz_idx] = hz_list[hz_idx][:-1]
            py.append(hz_list[hz_idx])
            if "".join(py) not in py2hz.cache:
                use_viterbi_num += 1
                start = time.time()
                hz = py2hz.handle_current_input("".join(py), 15, 15)
                end = time.time()
                viterbi_cost_time += (end-start)
                py2hz.cache["".join(py)] = hz
            else:
                hz = py2hz.cache["".join(py)]
            
            # print("hz ",hz)
            if args.test_acc == "top5":
                for i in range(5):
                    if i > len(hz)-1:
                        break
                    if hz[i].path[0] == expected_output_list[test_line_num][hz_idx]:
                        correct_num += 1
            elif args.test_acc == "top10":
                for i in range(10):
                    if i > len(hz)-1:
                        break
                    if hz[i].path[0] == expected_output_list[test_line_num][hz_idx]:
                        correct_num += 1
            else:
                raise Exception
        
    return float(correct_num/test_num), test_num, (viterbi_cost_time/use_viterbi_num)

# 测试集为多个词组，对整个词组进行测试
def combination_test(file_path, py2hz):
    fopen = open(file_path, "rb")
    py_data = []
    hz_data = []
    count = 0
    for line in fopen:
        line = line.decode("utf-8")
        line = line.split(" ")
        if len(line)>=1:
            word = line[0].split("\t")
            word = word[0]
            py_list = lazy_pinyin(word, style=NORMAL, errors=no_pinyin) # 将词组转换为拼音
            if py_list[0] == " ":
                continue # 文件开头，第一个词的前面会有空格
            py_data.append(py_list)
            hz_data.append(word)
                       
        count += 1
        if count>=10000:
        #     print("hz_data",hz_data)
        #     print("py_data",py_data)
            break
    
    # 对整个词组进行测试
    test_num = 0
    correct_num = 0
    viterbi_cost_time = 0.
    use_viterbi_num = 0
    for phrase_idx  in range(len(py_data)):
        test_num += 1
        py = "".join(py_data[phrase_idx])
        if py not in py2hz.cache:
            use_viterbi_num += 1
            start = time.time()
            hz = py2hz.handle_current_input(py, 15, 15)
            end = time.time()
            viterbi_cost_time += (end - start)
            py2hz.cache[py] = hz
        else:
            hz = py2hz.cache[py]

        if args.test_acc == "top5":
            for i in range(5):
                if i > len(hz)-1:
                    break
                if "".join(hz[i].path) == hz_data[phrase_idx]:
                    correct_num += 1
        elif args.test_acc == "top10":
            for i in range(10):
                if i > len(hz)-1:
                    break
                if "".join(hz[i].path) == hz_data[phrase_idx]:
                    correct_num += 1
        else:
            raise Exception
    
    return float(correct_num/test_num), test_num, (viterbi_cost_time/use_viterbi_num)


if __name__ == "__main__":
    # py2hz = py2hz_Pinyin()
    py2hz = Pinyin2Hanzi()
    if args.test_mode == "single":
        file_path = "./test_dataset/sentence.txt"
        correct_rate, test_num, avg_viterbi_cost = single_word_test(file_path, py2hz)
    elif args.test_mode == "phrase":
        file_path = "./test_dataset/sogou_dic_new.txt"
        correct_rate, test_num, avg_viterbi_cost = combination_test(file_path, py2hz)
    elif args.test_mode == "debug":
        correct_rate, test_num = debug_test(py2hz)
    else:
        raise Exception
    np.save("{}_{}.npy".format(args.test_mode, args.test_acc), np.array([correct_rate, avg_viterbi_cost]))
    print("完成{}个样本的测试，测试模式{}，测试精度{}，准确率为{}".format(test_num, args.test_mode, args.test_acc, correct_rate))