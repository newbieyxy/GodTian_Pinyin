#! usr/bin/python
# coding=utf-8
"""
File Name: SplitPinyin.py
Description: Split user's input (pinyin sequence)
Date: 2016-11-12
Author: QIU HU
"""

import pinyin_record

class SplitPinyin(object):

    def __init__(self):
        pinyin_and_pf = pinyin_record.pinyin_record()
        self.pinyin, self.prefix = pinyin_and_pf.get_record()

    ##### 拼音的发现 #####
    # 1）采用最长匹配的方式，用户输入的首个串是拼音或者某个合法拼音的前缀，则继续向后发现，等待用户输入（即拼音或者前缀的匹配）
    # 2）直到用户输完后发现，当前字符(n)与原来的前n-1个字符构成的字符串，不是合法的拼音也不是合法的拼音的前缀，此时将前面的n-1字符串切分成拼音
    ##### 实时输入的显示 #####
    # 每一时刻都需要有输出
    # 1）先切分拼音，最多只会有最后一个是不完整的拼音前缀，将完整的和不完整的分开处理
    # 2）完整的拼音，放入Viterbi算法中，通过HMM得出概率最大的输出串
    # 3）最后的非完整字符，在训练过的trie树中搜索出所有以该字符为前缀的字，以及他们出现的频率，取频率最高的若干个，作为下一个状态的可能集合
    # 4）与前面的完整拼音组合，通过Viterbi算法计算频率最高对应的最可能的中文串
    def split_pinyin(self, input):
        """
        Assume input is a valid pinyin sequence pre-processed.
        Split input sequence to single pinyin list
        :param input: sequence of character
        :return: list of string
        """
        two_part = False
        many_part = False
        res_list = []
        input_lis = input.split('\'') # input has been preprocessed, with ' inside
        for idx, input in enumerate(input_lis):
            input += '$' 
            # 如果最后输入的字符为分隔符'，那么split得到的结果最后一个是''，
            # 因此给每个分隔得到的结果后面加上$，防止空字符。
            length = len(input)
            tmp = ""
            i = 0
            while i < length:                    
                attempt = tmp + input[i]
                # print("tmp {} 和input[i] {} 组成 attempt {}".format(tmp, input[i], attempt))
                if attempt not in self.pinyin and attempt not in self.prefix:
                    # print("--|attempt {} 不在拼音且前缀中".format(attempt))
                    if tmp in self.pinyin: # The former part is pinyin
                        # print("----|tmp {} 在拼音中，更新tmp为 {}".format(tmp, input[i]))
                        res_list.append(tmp)
                        tmp = input[i] # The the current char will be the start of attempt
                    else:
                        # print("----||tmp {} 不在拼音中".format(tmp))
                        now_idx = i
                        now_tmp = tmp
                        
                        ###############
                        # 在这种情况下，tmp只可能是单个字符或sh
                        while len(tmp) > 0 and tmp not in self.pinyin: 
                            tmp = tmp[:-1] # tmp一直取它最后一个字符之前的所有拼音
                            i -= 1
                        
                            
                        # two_part 和 many_part：不完整的拼音出现的地方
                        # 如果是two part，就是最后一个字符是不完整的拼音(其他地方可能也有)；
                        # 如果是many part 就是中间的字出现有不完整的拼音
                        if len(tmp) == 0:
                            # The now_tmp is not in pinyin; the input[i] is the last char
                            if idx == len(input_lis) - 1 and input[now_idx] == '$':  # 最后了
                                res_list.append(now_tmp)
                                two_part = True
                                # print("----||two_part=True")
                                break
                            else:
                                res_list.append(now_tmp[0]) # now_tmp[0]实际上是tmp
                                i += 1
                                # print("----||many_part=True")
                                many_part = True

                        if many_part == False:
                            # print("----||many_part=False")
                            res_list.append(tmp)
                        tmp = input[i]
                        # print("----||更新tmp为 {}".format(input[i]))
                else:
                    # print("--||attempt {} 在拼音或者前缀中".format(attempt))
                    # print("--||更新tmp为 {}".format(attempt))
                    tmp = attempt
                i += 1
        
        # 只有一个字符的输入        
        if len(res_list) == 1 and res_list[0] not in self.pinyin:
            two_part = True
        return res_list, two_part,many_part



if __name__ == '__main__':

    a = SplitPinyin()
    print(a.split_pinyin("wsh"))
