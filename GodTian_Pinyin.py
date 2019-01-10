#! usr/bin/python
# coding=utf-8
"""
File Name: GodTian_Pinyin.py
Description: GodTian_Pinyin main function, with veterbi algorithm
Date: 2016-11-13
Author: QIU HU
"""

# import cPickle as pickle
import pickle as pickle
from Priotityset import PrioritySet
import SplitPinyin as sp
import re
import os
from pypinyin import lazy_pinyin
MIN_PROB = -500.0  # after log
import time
import collections

# transition possibility p(b|a)
def trans_a_b(trans, a, b):
    if a in trans:
        if b in trans[a]:
            return max(trans[a][b], MIN_PROB)
    return MIN_PROB


def Pi_state(Pi, state):
    if state in Pi:
        return max(Pi[state], MIN_PROB)
    else:
        return MIN_PROB


def emit_a_b(emit, a, b):
    if a in emit:
        if b in emit[a]:
            return max(emit[a][b], MIN_PROB)
    return MIN_PROB

def emit_a_b_many(emit,hanyu,pinyin):
    if hanyu in emit:
        judge = 0
        max_pinyin = -9999
        # max_i = -1 # useless
        for val in emit[hanyu]:
            for i in range(0,len(val)):
                if pinyin == val[:i]:
                    judge = 1
                    if emit[hanyu][val] > max_pinyin:
                        max_pinyin = emit[hanyu][val]
        if judge == 1:
            return max(max_pinyin, MIN_PROB)
    return MIN_PROB

def serch_in_dict(pyl,dict):
    res = ""
    # ii = 15 # useless
    for i in pyl:
        if i!=" ":
            res += i
    res += "  "
    if res in dict:
        list =  PrioritySet(15)
        s = sorted(dict[res].items(), key=lambda d: d[1], reverse=True) # dict.itertiems(python2) --> dict.items(python3)
        mm = 0
        for j in s:
            list1 = []
            for o in j[0]:
                list1.append(o)
            list.put(j[1],list1)
            mm += 1
        return list
    else:
        return []


class GodTian_Pinyin(object):

    def __init__(self):
        self.Pi = pickle.load(open('Pi.mat', 'rb'))
        self.emit = pickle.load(open('emit.mat', 'rb'))
        self.trans = pickle.load(open('trans.mat', 'rb'))
        self.py2ch = pickle.load(open('py2ch.mat', 'rb'))
        self.pt = pickle.load(open('pyintrie.tr', 'rb'))
        self.dict = pickle.load(open("pyall.tr", "rb"))

        self.pat = re.compile("\d*\.*\d+")
        if "cache.cc" in os.listdir(os.curdir):
            self.cache = pickle.load(open('cache.cc', 'rb'))
        else:
            self.cache = {}
        self.memo = collections.defaultdict(lambda: collections.defaultdict(PrioritySet))
        if "memo.mm" in os.listdir(os.curdir):
            memo = pickle.load(open('memo.mm', 'rb'))
            for key1 in memo:
                for key2 in memo[key1]:
                    self.memo[key1][key2] = memo[key1][key2]
        self.sp = sp.SplitPinyin()

    # 预判断和计算Viterbi
    def use_viterbi(self, pylist, top=15, topp =100, words=[], mode=None):
        # pylist:split of pinyin -- [py1,py2,...]
        use_top = top
        use_topp = topp #只考虑前topp的结果
        use_words = words
        use_mode = mode
        print("use_viterbi, mode {}".format(mode))
        # V[idx]的结构是
        # {'汉字'：[<score, path>,<score, path>,...],
        #  '汉字'：[<score, path>,<score, path>,...],
        #  ...}; 
        V = [{} for _ in range(2)] # 两个字典，一个用来存当前的状态，另一个用来记录前一个状态
        START = 1
        pylist_len = len(pylist)
        
        # 处理第一个拼音（及对应的状态）
        cur_obs = pylist[0]
        if mode == "many_part":
            # self.pt.get_totalwords_of_prefix(self.pt.root, pylist[0], prefix_ans)
            prefix_ans = {}
            self.pt.get_totalwords_of_prefix(self.pt.root, cur_obs, prefix_ans)
            sorted_pf_ans = sorted(prefix_ans.items(), key=lambda x: x[1], reverse=True)
            words = [hz_freq[0] for hz_freq in sorted_pf_ans[:topp]]
            cur_cand_states = words
            for state in cur_cand_states:
                tao = Pi_state(self.Pi, state) + emit_a_b_many(self.emit, state, cur_obs)
                _path = [state]
                V[0].setdefault(state, PrioritySet(use_top))  # {...,'汉字':[]}
                V[0][state] = PrioritySet(use_top) # {...,'汉字':[]}
                V[0][state].put(tao, _path)# {...,'汉字':[<score, path>]}
        elif mode == "two_part":
            pre_pyseq = "".join(pylist[:-1]) # 将前面完整的拼音部分组合到一起            
            # 如果pre_pyseq在memo中，直接查询，不用重新计算，最后一个拼音pylist[-1]才使用Viterbi
            # 如果pre_pyseq不在memo中，从第一个状态开始计算Viterbi
            if pre_pyseq in self.memo:
                # 将memo中的pre_pyseq对应的可能状态都找出来
                cur_cand_states = []
                for state in self.memo[pre_pyseq]:
                    cur_cand_states.append(state)
                    V[pylist_len%2][state] = self.memo[pre_pyseq][state] # 因为最后一个时刻为pylist_len-1，因此前面的都存在V[(pylist_len)%2]中
                START = pylist_len - 1
            else:
                cur_cand_states = self.py2ch[cur_obs]
                for state in cur_cand_states:
                    tao = Pi_state(self.Pi, state) + emit_a_b_many(self.emit, state, cur_obs)
                    _path = [state]
                    V[0].setdefault(state, PrioritySet(use_top))
                    V[0][state] = PrioritySet(use_top)
                    V[0][state].put(tao, _path)
                
        res = self.viterbi(pylist, START, V, cur_cand_states, use_top, use_topp, use_words, use_mode)
        
        return res

    # Viterbi算法
    def viterbi(self, pylist, START, V, cur_cand_states, top=15, topp=100, words=[], mode=None):
        # 再处理pylist第二个及后面的拼音
        # 在trie树中找到pylist[0]即第一个拼音分割py1的所有以它为前缀的词组prefix_ans
        # 并对prefix_ans中的结果进行排序
        # 将前topp个结果赋给cur_cand_states作为可能状态（即可能的汉字）
        # 状态即为汉字
        pylist_len = len(pylist)
        idx = 0
        for t in range(START, pylist_len): # 状态的时刻
            cur_obs = pylist[t]
            idx = t % 2 # 存储V的索引
            # 实际上是一个递推的过程，因此只用考虑前一个状态，因为前一个状态的path已经考虑了再前面的状态
            V[idx] = {}
            prefix_ans = {}             
            # 更新上一时刻记录的状态    
            prev_states = cur_cand_states # 上一个拼音py的可能状态
            
            # 更新当前状态，即当前拼音对应的可能状态
            if mode == "many_part":
                # 同样地，在trie树中找到pylist[t]即当前py的所有以它为前缀的词组prefix_ans
                # 排序，并取前topp个结果，作为可能的状态（即可能的汉字）
                self.pt.get_totalwords_of_prefix(self.pt.root, cur_obs, prefix_ans)
                sorted_pf_ans = sorted(prefix_ans.items(), key=lambda x: x[1], reverse=True)
                words = [hz_freq[0] for hz_freq in sorted_pf_ans[:topp]]
                cur_cand_states = words
            elif mode == "two_part":
                if not words:
                    cur_cand_states = self.py2ch[cur_obs]
                else:
                    cur_cand_states = words

            # 当前记录V[idx][state]；上一个状态记录V[(idx+1)%2][prev]
            for state in cur_cand_states:  # 此时状态
                V[idx].setdefault(state, PrioritySet(top))
                for prev in prev_states:  # 前一个状态
                    for cand in V[(idx + 1) % 2][prev]:  # 前一个状态为prev, cand的概率
                        tao = trans_a_b(self.trans, prev, state) + emit_a_b_many(self.emit, state, cur_obs)
                        new_tao = tao + cand.score
                        _p = cand.path + [state]
                        V[idx][state].put(new_tao, _p)
                # print("V[{}] {}".format(idx, V[idx]))
                
        # 只用看最后的V[idx]，相当于包含了前面所有的路径
        results = PrioritySet(top)
        for last_state in V[idx]:
            if mode == "two_part":
                self.memo["".join(pylist)][last_state] = V[idx][last_state] # 将整个拼音串的所有最后状态(包括score和path)存入memo中
            for item in V[idx][last_state]:
                results.put(item.score, item.path)
        results = [item for item in results]
        return sorted(results, key=lambda x: x.score, reverse=True)

    def save_memo_and_cache(self):

        pickle.dump(self.cache, open('cache.cc', 'wb'), True)
        pickle.dump(dict(self.memo), open('memo.mm', 'wb'), True)

    def handle_current_input(self, input, topv=15, topp=15):
        # 将所有的大写都转成小写
        input = input.lower()
        if self.pat.findall(input):   # 全数字，直接返回
            return input
        pyl, two_part,many_parts = self.sp.split_pinyin(input)
        print(pyl, two_part, many_parts)
        if two_part == True and many_parts == False: # 只有最后一组拼音是不完整的
            prefix_ans = {}
            start = time.time()
            self.pt.get_totalwords_of_prefix(self.pt.root, pyl[-1], prefix_ans)
            sorted_pf_ans = sorted(prefix_ans.items(), key=lambda x: x[1], reverse=True)
            end = time.time()
            # print("GET PREFIX COST: {}".format(end-start))
            words = [hz_freq[0] for hz_freq in sorted_pf_ans[:topp]]
            # -------------------------
            best_viterbi_ans = []
            pinyins = map(lambda x: lazy_pinyin(x)[0], words)
            viterbi_ans = []
            start = time.time()
            for _, py in enumerate(pinyins):
                pyl[-1] = py
                # viterbi_ans = self.viterbi(pyl, topv, [words[_]])  # self.memo["".join(pyl[:-1]][state...] =
                viterbi_ans = self.use_viterbi(pyl, topv, [words[_]], mode="two_part")
            end = time.time()
            # print("VITERBI COST: {}".format(end-start))
            best_viterbi_ans.extend(viterbi_ans)
            return best_viterbi_ans, two_part
        elif many_parts: # 中间的拼音也是不完整的
            new_viterbi_ans = serch_in_dict(pyl,self.dict)
            # print ("new_viterbi_and ",new_viterbi_ans)
            if new_viterbi_ans ==[]:
               # new_viterbi_ans = self.newviterbi(pyl, topv, mode="many_part")
               new_viterbi_ans = self.use_viterbi(pyl, topv, mode="many_part")
            return new_viterbi_ans,two_part
        else: # 所有拼音都是完整的
            # viterbi_ans = self.viterbi(pyl, topv, [])
            viterbi_ans = self.use_viterbi(pyl, topv, mode="two_part")
            # print ("viterbi_ans ",viterbi_ans)
            return viterbi_ans, two_part

# if __name__ == '__main__':
#
#     a = sp.SplitPinyin()
#     godtian = GodTian_Pinyin()
#
#     while True:
#         input2 = input("input: ")
#         if input2 in ['Q', 'q']:
#             break
#         res1, two_part = godtian.handle_current_input(input2, 100, 100)
#         for _ in range(0, min(len(res1), 10)):
#             r = res1[_]
#             for i in r.path:
#                 print (i)
#             print("")


