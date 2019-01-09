# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 15:16:48 2019

@author: yxy

Offline evaluation of pinyin input method.
"""

import re
from GodTian_Pinyin import GodTian_Pinyin
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--test-acc", type=str, default="top5", help="test mode: top5 or top10")
args = parser.parse_args()

if __name__ == "__main__":
    input_list = []
    expected_output_list = []
    test_file = open('test_set.txt')
    for line in test_file:
        # 测试集是一行拼音一行文字
        # 将拼音和文字分开
        is_char_low = re.match(r'[a-z\']', line[0]) 
        is_char_up = re.match(r'[A-Z\']', line[0])
        if is_char_low or is_char_up:
            input_list.append(line)
        else:
            expected_output_list.append(line)
     
    
    # 将测试样本中的每句话的每个中文字对应的拼音提取，用单个中文字去测试
    godtian = GodTian_Pinyin()
    test_num = 0
    correct_num = 0
    for test_line_num in range(len(input_list)):
        hz_list = input_list[test_line_num].split(' ')
        # print("测试句子",hz_list)
        for hz_idx in range(len(hz_list)):
            test_num += 1
            py = [] # 单个字的测试
            if "\n" in hz_list[hz_idx]:
                hz_list[hz_idx] = hz_list[hz_idx][:-1]
            py.append(hz_list[hz_idx])
            if "".join(py) not in godtian.cache:
                hz, two_part = godtian.handle_current_input("".join(py), 15, 15)
                godtian.cache["".join(py)] = hz
            else:
                hz = godtian.cache["".join(py)]
            
            # print("hz ",hz)
            res_py_list = []
            res_score_list = []
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
        
    print("测试模式{}：完成{}个句子的测试，准确率为{}".format(args.test_acc, len(input_list), float(correct_num/test_num)))       


