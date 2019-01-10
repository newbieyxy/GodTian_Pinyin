
import os
import math
import logging
import argparse
import collections
import pickle
from pypinyin import lazy_pinyin, NORMAL
import PinyinTrie
logging.basicConfig(filename='trainingDebug.log', level=logging.DEBUG)

def isChinese(ch):
	return u'\u4e00' <= ch <= u'\u9fff' or ch == u'〇'

def isChineseString(str):
	return any(isChinese(ch) for ch in str)

#作为lazy_pinyin中的errors参数的回调函数
def no_pinyin(ch):
	return ''

def first_training():
	#从空白开始训练
	pi = collections.defaultdict(float)
	trans = collections.defaultdict(lambda: collections.defaultdict(float))
	emit = collections.defaultdict(lambda: collections.defaultdict(float))
	py2ch = collections.defaultdict(lambda: collections.defaultdict(float))     #拼音对应的汉字
	pytrie = PinyinTrie.PinyinTrie()
	corpus_path = os.getcwd()+ '\\corpus\\SogouQ'
	logging.info('first trainning! create default dict!')
	return train(pi, trans, emit, py2ch, pytrie, corpus_path)


def incremental_traning(corpus_path = os.getcwd()+ '\\SogouQ'):
	#读取已有的，然后用新的语料库生成新的训练结果，添加进去
	pi = pickle.load(open('Pi.freq', 'rb'))
	trans = pickle.load(open('trans.freq', 'rb'))
	emit = pickle.load(open('emit.freq', 'rb'))
	py2ch = pickle.load(open('py2ch.freq', 'rb'))     #拼音对应的汉字
	pytrie = pickle.load(open('pytrie.tr', 'rb'))
	logging.info('incremental training! loading freq_dict from files!')
	return train(pi, trans, emit, py2ch, pytrie, corpus_path)

def savefiles(pi, trans, emit, py2ch, pytrie):
	# 存储频率
	file_list = ['Pi.freq', 'trans.freq', 'emit.freq', 'py2ch.freq']
	dict_list = [dict(pi), dict(trans), dict(emit), dict(py2ch)]
	for i in range(len(file_list)):
		with open(file_list[i], 'wb') as f:
			pickle.dump(dict_list[i], f, True)
			logging.info('save to \'%s\''%file_list[i])
	# 频率计算概率
	count = 0.0
	for start in pi:
		count += pi[start]
	for start in pi:
		pi[start] = math.log(pi[start] / count)

	for start in trans:
		count = 0.0
		for end in trans[start]:
			count += trans[start][end]
		for end in trans[start]:
			trans[start][end] = math.log(trans[start][end] / count)

	for start in emit:
		count = 0.0
		for end in emit[start]:
			count += emit[start][end]
		for end in emit[start]:
			emit[start][end] = math.log(emit[start][end] / count)

	for start in py2ch:
		count = 0.0
		for end in py2ch[start]:
			count += py2ch[start][end]
		for end in py2ch[start]:
			py2ch[start][end] = math.log(py2ch[start][end] / count)
	# 存储概率
	file_list = ['Pi.mat','trans.mat', 'emit.mat', 'py2ch.mat']
	dict_list = [dict(pi), dict(trans), dict(emit), dict(py2ch)]
	for i in range(len(file_list)):
		with open(file_list[i], 'wb') as f:
			pickle.dump(dict_list[i], f, True)
			logging.info('save to \'%s\', total length of keys:%d'%(file_list[i], len(dict_list[i].keys())))
	# 存储trie树
	with open('pyintrie.tr', 'wb') as f:
		pickle.dump(pytrie, f, True)
		logging.info('save to \'pyintrie.tr\'')



#基于base的三个矩阵添加训练，或是从头开始
def train(pi, trans, emit, py2ch, pytrie, corpus_path):
	#语料库列表
	try:
		corpus_list = os.listdir(corpus_path)
	except Exception as e:
		logging.error('the path of corpus is wrong!!!!!')
	else:
		logging.info('training from corpus: %s'%corpus_path)
		for corpus in corpus_list:
			lineNum = 0
			with open(corpus_path+'\\'+corpus, 'r', errors='ignore') as f:
				for line in f.readlines():
					lineNum += 1
					line=line.strip()
					if len(line) < 2:
						continue
					#字节用utf8解码成字符串
					if type(line) == bytes:
						line = line.decode('utf8')
					#一个汉字也没有
					if not isChineseString(line):
						continue
					ch_str = ''.join([ch if isChinese(ch) else ' ' for ch in line])
					ch_str = ch_str.strip()
					sentences_list = []
					for s in ch_str.split(' '):
						if len(s) >= 1:
							sentences_list.append(s)
					if lineNum < 10:
						logging.debug('{}:sentences:{}'.format(lineNum, sentences_list))
					#将每个子句转为拼音，统计频率
					for sentence in sentences_list:
						py_list = lazy_pinyin(sentence, style=NORMAL, errors=no_pinyin)
						pi[sentence[0]] += 1
						for i in range(len(sentence)):
							if i+1 < len(sentence):
								trans[sentence[i]][sentence[i+1]] += 1
							if py_list[i] != '':
								emit[sentence[i]][py_list[i]] += 1
								py2ch[py_list[i]][sentence[i]] += 1
								pytrie.add(py_list[i], sentence[i])        #添加拼音及其对应的字到trie树
						if lineNum < 3:
							logging.debug('{}:sentence:{}, pi:{}, emit:{}, trans:{}'.format(lineNum, sentence, pi, emit, trans))

		savefiles(pi, trans, emit, py2ch, pytrie)
		return pi, trans, emit, py2ch, pytrie



def prefix_ch_dict():
	# 从语料库中训练 多个拼音前缀及对应的词组出现的词频，如 dict['mt']['明天'] = 5, dict['mt']['媒体']=7
	# 新弄一棵trie树不就行了?? 噢这个是加词频。。trie树是加一。。 
	pr_ch_dict = {}
	with open('dictword', 'rb') as f:
		for line in f.readlines():
			if type(line) == bytes:
				line.decode('utf8')
			line = line.split()
			#每一行至少包含词组，词频
			if len(line) < 2:
				continue
			words, freq = line[:2]
			if type(words) == bytes:
				words = words.decode('utf')
			py_list = lazy_pinyin(words, style=NORMAL, errors=no_pinyin)
			#过滤掉没有拼音的字
			prefix_str = ''
			word_str = words
			for i, py in enumerate(py_list):
				if py[0] != '':
					prefix_str += py[0]
				else:
					word_str=word_str[:i]+' '+word_str[i+1:]
			word_str = ''.join(word_str.split(' '))
			pr_ch_dict.setdefault(prefix_str, {})
			pr_ch_dict[prefix_str].setdefault(word_str, 0)
			pr_ch_dict[prefix_str][word_str] += int(freq)

	with open('pyall.tr', 'wb') as f:
		pickle.dump(pr_ch_dict, f, True)
		logging.info('save to %s'%('pyall.tr'))


def test():
    Pi, trans, emit, py2ch, pyintrie = first_training()
    #prefix_ch_dict()
    #pr_ch_trie = pickle.load(open('pyall.tr', 'rb'))
    #pr_ch_trie.display_trie()
    #Pi, trans, emit, py2ch = incremental_training()
    print("Training Done~")
    # Pi = pickle.load(open('Pi.mat', 'rb'))
    # emit = pickle.load(open('emit.mat', 'rb'))
    # trans = pickle.load(open('trans.mat', 'rb'))
    # print(emit[u'尼'])
    # print(emit[u'你'])
    # print(trans[u'你'][u'好'])
    # s = trans[u'你']
    # print(type(s))
    # t = sorted(s.items(), key=lambda x: x[1], reverse=True)
    # for r in t[:10]:
    #     print(r[0])
    #     print(r[1])
    # print(Pi[u'你'])
    #pyintrie = pickle.load(open('pyintrie.tr', 'rb'))
    #pyintrie.display_trie()


def parse_argument():
	parser = argparse.ArgumentParser(description='argument parser for training.py')
	parser.add_argument('corpus', type=str, help='the path of corpus')
	#dest指定对应参数在args中的属性名
	#choices来规范参数的合法性，指定只能从二者之中选
	parser.add_argument('-m', '--mode', dest='training_mode', action='store', choices={'first', 'add'}, default='first')

	args = parser.parse_args()
	corpus = args.corpus
	print(corpus)
	print(args.training_mode)
	return args

if __name__ == '__main__':
	#args = parse_argument()
	#print(os.listdir(args.corpus))
	test()














