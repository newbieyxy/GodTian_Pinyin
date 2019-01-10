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
        prefix_at_end = False # 最后一个字对应的不是完整拼音而是前缀
        prefix_at_mid = False # 在中间或前面出现拼音前缀
        res_list = []
        input_list = input.split('\'') # 如果有分隔符'，提前根据分隔符切割拼音串
        for idx, input_ in enumerate(input_list):
            input_ += '$'
            last = ""
            i = 0
            while i < len(input_):
                # cur : 从分隔处开始到当前字符
                # last: 从分隔处开始到当前的上一个字符
                # 遍历input的每个字符，判断是否达到分隔处，
                #    是则保存并继续处理； 否则
                cur = last + input_[i]
                #若当前不是拼音也不是前缀，可能已经到了分隔处
                if cur not in self.pinyin and cur not in self.prefix:
                    # 处理第一个字符是无效拼音的情况，即一直处理到出现的是有效拼音或前缀为止
                    if len(last) == 0: 
                        i += 1
                        continue
                    #若截止到前一个字符，可以形成完整的拼音串，则说明已经是分隔处，保存完整拼音串并清空last，继续分析input
                    elif last in self.pinyin: # The former part is pinyin
                        res_list.append(last)
                        last = input_[i]   #清空last，并置为分割处的第一个
                    else:
                    #若无法形成完整的拼音
                        cur_idx = i
                        valid_last = last 
                        # 回退直到出现有效的拼音
                        while len(valid_last) > 0 and valid_last not in self.pinyin: 
                            valid_last = valid_last[:-1]
                            i -= 1
                        # 整个last都没有有效拼音
                        if len(valid_last) == 0:
                            # 在最后出现不完整拼音串; 
                            if idx == len(input_list) - 1 and input_[cur_idx] == '$':
                                res_list.append(last)
                                prefix_at_end = True
                                break
                            # 还没到最后就出现不完整拼音串，只取第一个字母 'shm'会被分为's''h''m'
                            else:
                                res_list.append(last[0])
                                i += 1
                                prefix_at_mid = True
                        # else:
                        	# 会有这种情况么????
                            # print('len last != 0, last:{}'.format(last))
                        # maybe useless
                        # if prefix_at_mid == False: 
                        #     res_list.append(last) 
                        last = input_[i]
                else:
                    #若当前是某个拼音或前缀 更新last并继续分析下一个是不是分割处
                    last = cur
                i += 1

        #拼音串只有单个字母前缀，只代表一个字
        if len(res_list) == 1 and res_list[0] not in self.pinyin:
            prefix_at_end = True
        	
        return res_list, prefix_at_end, prefix_at_mid



if __name__ == '__main__':

    a = SplitPinyin()

    # py, pf = a.load_valid_pinyin()
    # pyJson = json.dumps(py)
    # pfJson = json.dumps(pf)
    # with open('valid_pinyin.json', 'w') as f:
    # 	f.write(pyJson)
    # with open('valid_pyprefix.json', 'w') as f:
    # 	f.write(pfJson)
    print(a.split_pinyin("nh"))
