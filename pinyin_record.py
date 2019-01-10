# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 11:56:30 2019

@author: yxy

Record all pinyin.
"""

# Save in object of dict, instead of saving in file
# Maybe faster for searching
import collections

class pinyin_record(object):
    def __init__(self):
        self.pinyin = collections.defaultdict(int)
        self.pf = collections.defaultdict(int)  # prefix
        self.define_record()
        
    def define_record(self):
        self.pinyin["a"] = 1
        self.pinyin["ai"] = 1
        self.pinyin["an"] = 1
        self.pinyin["ao"] = 1
        self.pinyin["ang"] = 1
        
        self.pf["b"] = 1
        self.pinyin["ba"] = 1
        self.pinyin["bai"] = 1
        self.pinyin["ban"] = 1
        self.pinyin["bang"] = 1
        self.pinyin["bao"] = 1
        self.pf["be"] = 1
        self.pinyin["bei"] = 1
        self.pinyin["ben"] = 1
        self.pinyin["beng"] = 1
        self.pinyin["bi"] = 1
        self.pf["bia"] = 1
        self.pinyin["bian"] = 1
        self.pinyin["biao"] = 1
        self.pinyin["bie"] = 1
        self.pinyin["bin"] = 1
        self.pinyin["bing"] = 1
        self.pinyin["bo"] = 1
        self.pinyin["bu"] = 1
        
        self.pf["c"] = 1
        self.pinyin["ca"] = 1
        self.pinyin["cai"] = 1
        self.pinyin["can"] = 1
        self.pinyin["cang"] = 1
        self.pinyin["cao"] = 1
        self.pinyin["ce"] = 1
        self.pinyin["cen"] = 1
        self.pinyin["ceng"] = 1
        self.pinyin["ci"] = 1
        self.pf["co"] = 1
        self.pf["con"] = 1
        self.pinyin["cong"] = 1
        self.pinyin["cou"] = 1
        self.pinyin["cu"] = 1
        self.pf["cua"] = 1
        self.pinyin["cuan"] = 1
        self.pinyin["cui"] = 1
        self.pinyin["cun"] = 1
        self.pinyin["cuo"] = 1
        
        self.pf["d"] = 1
        self.pinyin["da"] = 1
        self.pinyin["dai"] = 1
        self.pinyin["dan"] = 1
        self.pinyin["dang"] = 1
        self.pinyin["dao"] = 1
        self.pinyin["de"] = 1
        self.pinyin["dei"] = 1
        self.pf["den"] = 1
        self.pinyin["deng"] = 1
        self.pinyin["di"] = 1
        self.pinyin["dia"] = 1
        self.pinyin["dian"] = 1
        self.pinyin["diao"] = 1
        self.pinyin["die"] = 1
        self.pinyin["din"] = 1
        self.pinyin["ding"] = 1
        self.pinyin["diu"] = 1
        self.pf["do"] = 1
        self.pf["don"] = 1
        self.pinyin["dong"] = 1
        self.pinyin["dou"] = 1
        self.pinyin["du"] = 1
        self.pf["dua"] = 1
        self.pinyin["duan"] = 1
        self.pinyin["dui"] = 1
        self.pinyin["dun"] = 1
        self.pinyin["duo"] = 1
        
        self.pinyin["e"] = 1
        self.pinyin["ei"] = 1
        self.pinyin["en"] = 1
        self.pinyin["er"] = 1
        
        self.pf["f"] = 1
        self.pinyin["fa"] = 1
        self.pinyin["fan"] = 1
        self.pinyin["fang"] = 1
        self.pf["fe"] = 1
        self.pinyin["fei"] = 1
        self.pinyin["fen"] = 1
        self.pinyin["feng"] = 1
        self.pf["fi"] = 1
        self.pf["fia"] = 1
        self.pinyin["fiao"] = 1  # 覅
        self.pinyin["fo"] = 1
        self.pinyin["fou"] = 1
        self.pinyin["fu"] = 1
        
        self.pf["g"] = 1
        self.pinyin["ga"] = 1
        self.pinyin["gai"] = 1
        self.pinyin["gan"] = 1
        self.pinyin["gang"] = 1
        self.pinyin["gao"] = 1
        self.pinyin["ge"] = 1
        self.pinyin["gei"] = 1
        self.pinyin["gen"] = 1
        self.pinyin["geng"] = 1
        self.pf["go"] = 1
        self.pf["gon"] = 1
        self.pinyin["gong"] = 1
        self.pinyin["gou"] = 1
        self.pinyin["gu"] = 1
        self.pinyin["gua"] = 1
        self.pinyin["guai"] = 1
        self.pinyin["guan"] = 1
        self.pinyin["guang"] = 1
        self.pinyin["gui"] = 1
        self.pinyin["gun"] = 1
        self.pinyin["guo"] = 1
        
        self.pf["h"] = 1
        self.pinyin["ha"] = 1
        self.pinyin["hai"] = 1
        self.pinyin["han"] = 1
        self.pinyin["hang"] = 1
        self.pinyin["hao"] = 1
        self.pinyin["he"] = 1
        self.pinyin["hei"] = 1
        self.pinyin["hen"] = 1
        self.pinyin["heng"] = 1
        self.pf["hon"] = 1
        self.pinyin["hong"] = 1
        self.pf["ho"] = 1
        self.pinyin["hou"] = 1
        self.pinyin["hu"] = 1
        self.pinyin["hua"] = 1
        self.pinyin["huai"] = 1
        self.pinyin["huan"] = 1
        self.pinyin["huang"] = 1
        self.pinyin["hui"] = 1
        self.pinyin["hun"] = 1
        self.pinyin["huo"] = 1
        
        self.pf["j"] = 1
        self.pinyin["ji"] = 1
        self.pinyin["jia"] = 1
        self.pinyin["jian"] = 1
        self.pinyin["jiang"] = 1
        self.pinyin["jiao"] = 1
        self.pinyin["jie"] = 1
        self.pinyin["jin"] = 1
        self.pinyin["jing"] = 1
        self.pf["jio"] = 1
        self.pf["jion"] = 1
        self.pinyin["jiong"] = 1
        self.pinyin["jiu"] = 1
        self.pinyin["ju"] = 1
        self.pf["jua"] = 1
        self.pinyin["juan"] = 1
        self.pinyin["jue"] = 1
        self.pinyin["jun"] = 1
        
        self.pf["k"] = 1
        self.pinyin["ka"] = 1
        self.pinyin["kai"] = 1
        self.pinyin["kan"] = 1
        self.pinyin["kang"] = 1
        self.pinyin["kao"] = 1
        self.pinyin["ke"] = 1
        self.pinyin["ken"] = 1
        self.pinyin["keng"] = 1
        self.pf["ko"] = 1
        self.pf["kon"] = 1
        self.pinyin["kong"] = 1
        self.pinyin["kou"] = 1
        self.pinyin["ku"] = 1
        self.pinyin["kui"] = 1
        self.pinyin["kun"] = 1
        self.pinyin["kua"] = 1
        self.pinyin["kuai"] = 1
        self.pinyin["kuan"] = 1
        self.pinyin["kuang"] = 1
        self.pinyin["kuo"] = 1
        
        self.pf["l"] = 1
        self.pinyin["la"] = 1
        self.pinyin["lai"] = 1
        self.pinyin["lan"] = 1
        self.pinyin["lang"] = 1
        self.pinyin["lao"] = 1
        self.pinyin["le"] = 1
        self.pinyin["lei"] = 1
        self.pf["len"] = 1
        self.pinyin["leng"] = 1
        self.pinyin["li"] = 1
        self.pinyin["lia"] = 1
        self.pinyin["lian"] = 1
        self.pinyin["liang"] = 1
        self.pinyin["liao"] = 1
        self.pinyin["lie"] = 1
        self.pinyin["lin"] = 1
        self.pinyin["ling"] = 1
        self.pinyin["liu"] = 1
        self.pinyin["lo"] = 1
        self.pf["lon"] = 1
        self.pinyin["long"] = 1
        self.pinyin["lou"] = 1
        self.pinyin["lu"] = 1
        self.pf["lua"] = 1
        self.pinyin["luan"] = 1
        self.pinyin["lun"] = 1
        self.pinyin["luo"] = 1
        self.pinyin["lv"] = 1
        self.pinyin["lve"] = 1
        
        self.pf["m"] = 1
        self.pinyin["ma"] = 1
        self.pinyin["mai"] = 1
        self.pinyin["man"] = 1
        self.pinyin["mang"] = 1
        self.pinyin["mao"] = 1
        self.pinyin["me"] = 1
        self.pinyin["mei"] = 1
        self.pinyin["men"] = 1
        self.pinyin["meng"] = 1
        self.pinyin["mi"] = 1
        self.pf["mia"] = 1
        self.pinyin["mian"] = 1
        self.pinyin["miao"] = 1
        self.pinyin["mie"] = 1
        self.pinyin["min"] = 1
        self.pinyin["ming"] = 1
        self.pinyin["miu"] = 1
        self.pinyin["mo"] = 1
        self.pinyin["mou"] = 1
        self.pinyin["mu"] = 1
        
        self.pf["n"] = 1
        self.pinyin["na"] = 1
        self.pinyin["nai"] = 1
        self.pinyin["nan"] = 1
        self.pinyin["nang"] = 1
        self.pinyin["nao"] = 1
        self.pinyin["ne"] = 1
        self.pinyin["nei"] = 1
        self.pinyin["nen"] = 1
        self.pinyin["neng"] = 1
        self.pinyin["ni"] = 1
        self.pf["nia"] = 1
        self.pinyin["nian"] = 1
        self.pinyin["niang"] = 1
        self.pinyin["niao"] = 1
        self.pinyin["nie"] = 1
        self.pinyin["nin"] = 1
        self.pinyin["ning"] = 1
        self.pinyin["niu"] = 1
        self.pf["non"] = 1
        self.pf["no"] = 1
        self.pinyin["nong"] = 1
        self.pinyin["nou"] = 1
        self.pinyin["nu"] = 1
        self.pf["nua"] = 1
        self.pinyin["nuan"] = 1
        self.pinyin["nun"] = 1
        self.pinyin["nuo"] = 1
        self.pinyin["nv"] = 1
        self.pinyin["nve"] = 1
        
        self.pinyin["o"] = 1
        self.pinyin["ou"] = 1
        
        self.pf["p"] = 1          ###
        self.pinyin["pa"] = 1
        self.pinyin["pai"] = 1
        self.pinyin["pan"] = 1
        self.pinyin["pang"] = 1
        self.pinyin["pao"] = 1
        self.pinyin["pe"] = 1
        self.pinyin["pei"] = 1
        self.pinyin["pen"] = 1
        self.pinyin["peng"] = 1
        self.pinyin["pi"] = 1
        self.pf["pia"] = 1
        self.pinyin["pian"] = 1
        self.pinyin["piao"] = 1
        self.pinyin["pie"] = 1
        self.pinyin["pin"] = 1
        self.pinyin["ping"] = 1
        self.pinyin["po"] = 1
        self.pinyin["pou"] = 1
        self.pinyin["pu"] = 1
        
        self.pf["q"] = 1
        self.pinyin["qi"] = 1
        self.pinyin["qia"] = 1
        self.pinyin["qian"] = 1
        self.pinyin["qiang"] = 1
        self.pinyin["qiao"] = 1
        self.pinyin["qie"] = 1
        self.pinyin["qin"] = 1
        self.pinyin["qing"] = 1
        self.pf["qio"] = 1
        self.pf["qion"] = 1
        self.pinyin["qiong"] = 1
        self.pinyin["qiu"] = 1
        self.pinyin["qu"] = 1
        self.pf["qua"] = 1
        self.pinyin["quan"] = 1
        self.pinyin["que"] = 1
        self.pinyin["qun"] = 1
        
        self.pf["r"] = 1
        self.pf["ra"] = 1
        self.pinyin["ran"] = 1
        self.pinyin["rang"] = 1
        self.pinyin["rao"] = 1
        self.pinyin["re"] = 1
        self.pinyin["ren"] = 1
        self.pinyin["reng"] = 1
        self.pinyin["ri"] = 1
        self.pf["ro"] = 1
        self.pf["ron"] = 1
        self.pinyin["rong"] = 1
        self.pinyin["rou"] = 1
        self.pinyin["ru"] = 1
        self.pf["rua"] = 1
        self.pinyin["ruan"] = 1
        self.pinyin["rui"] = 1
        self.pinyin["run"] = 1
        self.pinyin["ruo"] = 1
        
        self.pf["s"] = 1
        self.pinyin["sa"] = 1
        self.pinyin["sai"] = 1
        self.pinyin["san"] = 1
        self.pinyin["sang"] = 1
        self.pinyin["sao"] = 1
        self.pinyin["se"] = 1
        self.pinyin["sen"] = 1
        self.pinyin["seng"] = 1
        self.pinyin["si"] = 1
        self.pf["son"] = 1
        self.pf["so"] = 1
        self.pinyin["song"] = 1
        self.pinyin["sou"] = 1
        self.pinyin["su"] = 1
        self.pf["sua"] = 1
        self.pinyin["suan"] = 1
        self.pinyin["sui"] = 1
        self.pinyin["sun"] = 1
        self.pinyin["suo"] = 1
        
        self.pf["t"] = 1
        self.pinyin["ta"] = 1
        self.pinyin["tai"] = 1
        self.pinyin["tan"] = 1
        self.pinyin["tang"] = 1
        self.pinyin["tao"] = 1
        self.pinyin["te"] = 1
        self.pinyin["tei"] = 1
        self.pf["ten"] = 1
        self.pinyin["teng"] = 1
        self.pinyin["ti"] = 1
        self.pf["tia"] = 1
        self.pinyin["tian"] = 1
        self.pinyin["tiao"] = 1
        self.pinyin["tie"] = 1
        self.pf["tin"] = 1
        self.pf["ton"] = 1
        self.pf["to"] = 1
        self.pinyin["ting"] = 1
        self.pinyin["tong"] = 1
        self.pinyin["tou"] = 1
        self.pinyin["tu"] = 1
        self.pf["tua"] = 1
        self.pinyin["tuan"] = 1
        self.pinyin["tui"] = 1
        self.pinyin["tun"] = 1
        self.pinyin["tuo"] = 1
        
        self.pf["w"] = 1
        self.pinyin["wa"] = 1
        self.pinyin["wai"] = 1
        self.pinyin["wan"] = 1
        self.pinyin["wang"] = 1
        self.pf["we"] = 1
        self.pinyin["wei"] = 1
        self.pinyin["wen"] = 1
        self.pinyin["weng"] = 1
        self.pinyin["wo"] = 1
        self.pinyin["wu"] = 1
        
        self.pf["x"] = 1
        self.pinyin["xi"] = 1
        self.pinyin["xia"] = 1
        self.pinyin["xian"] = 1
        self.pinyin["xiang"] = 1
        self.pinyin["xiao"] = 1
        self.pinyin["xie"] = 1
        self.pinyin["xin"] = 1
        self.pinyin["xing"] = 1
        self.pf["xion"] = 1
        self.pinyin["xiong"] = 1
        self.pinyin["xiu"] = 1
        self.pinyin["xu"] = 1
        self.pf["xua"] = 1
        self.pinyin["xuan"] = 1
        self.pinyin["xue"] = 1
        self.pinyin["xun"] = 1
        
        self.pf["y"] = 1
        self.pinyin["ya"] = 1
        self.pinyin["yan"] = 1
        self.pinyin["yang"] = 1
        self.pinyin["yao"] = 1
        self.pinyin["ye"] = 1
        self.pinyin["yi"] = 1
        self.pinyin["yin"] = 1
        self.pinyin["ying"] = 1
        self.pinyin["yo"] = 1
        self.pf["yon"] = 1
        self.pinyin["yong"] = 1
        self.pinyin["you"] = 1
        self.pinyin["yu"] = 1
        self.pf["yua"] = 1
        self.pinyin["yuan"] = 1
        self.pinyin["yue"] = 1
        self.pinyin["yun"] = 1
        
        self.pf["z"] = 1
        self.pinyin["za"] = 1
        self.pinyin["zai"] = 1
        self.pinyin["zan"] = 1
        self.pinyin["zang"] = 1
        self.pinyin["zao"] = 1
        self.pinyin["ze"] = 1
        self.pinyin["zei"] = 1
        self.pinyin["zen"] = 1
        self.pinyin["zeng"] = 1
        self.pinyin["zi"] = 1
        self.pf["zon"] = 1
        self.pf["zo"] = 1
        self.pinyin["zong"] = 1
        self.pinyin["zou"] = 1
        self.pinyin["zu"] = 1
        self.pf["zua"] = 1
        self.pinyin["zuan"] = 1
        self.pinyin["zui"] = 1
        self.pinyin["zun"] = 1
        self.pinyin["zuo"] = 1
        
        self.pf["ch"] = 1
        self.pinyin["cha"] = 1
        self.pinyin["chai"] = 1
        self.pinyin["chan"] = 1
        self.pinyin["chang"] = 1
        self.pinyin["chao"] = 1
        self.pinyin["che"] = 1
        self.pinyin["chen"] = 1
        self.pinyin["cheng"] = 1
        self.pinyin["chi"] = 1
        self.pf["cho"] = 1
        self.pf["chon"] = 1
        self.pinyin["chong"] = 1
        self.pinyin["chou"] = 1
        self.pinyin["chu"] = 1
        self.pinyin["chua"] = 1
        self.pinyin["chuai"] = 1
        self.pinyin["chuan"] = 1
        self.pinyin["chuang"] = 1
        self.pinyin["chui"] = 1
        self.pinyin["chun"] = 1
        self.pinyin["chuo"] = 1
        
        self.pf["sh"] = 1
        self.pinyin["sha"] = 1
        self.pinyin["shai"] = 1
        self.pinyin["shan"] = 1
        self.pinyin["shang"] = 1
        self.pinyin["shao"] = 1
        self.pinyin["she"] = 1
        self.pinyin["shei"] = 1
        self.pinyin["shen"] = 1
        self.pinyin["sheng"] = 1
        self.pinyin["shi"] = 1
        self.pf["sho"] = 1
        self.pinyin["shou"] = 1
        self.pinyin["shu"] = 1
        self.pinyin["shua"] = 1
        self.pinyin["shuai"] = 1
        self.pinyin["shuan"] = 1
        self.pinyin["shuang"] = 1
        self.pinyin["shui"] = 1
        self.pinyin["shun"] = 1
        self.pinyin["shuo"] = 1
        
        self.pf["zh"] = 1
        self.pinyin["zha"] = 1
        self.pinyin["zhai"] = 1
        self.pinyin["zhan"] = 1
        self.pinyin["zhang"] = 1
        self.pinyin["zhao"] = 1
        self.pinyin["zhe"] = 1
        self.pinyin["zhei"] = 1
        self.pinyin["zhen"] = 1
        self.pinyin["zheng"] = 1
        self.pinyin["zhi"] = 1
        self.pf["zho"] = 1
        self.pf["zhon"] = 1
        self.pinyin["zhong"] = 1
        self.pinyin["zhou"] = 1
        self.pinyin["zhu"] = 1
        self.pinyin["zhua"] = 1
        self.pinyin["zhuai"] = 1
        self.pinyin["zhuan"] = 1
        self.pinyin["zhuang"] = 1
        self.pinyin["zhui"] = 1
        self.pinyin["zhun"] = 1
        self.pinyin["zhuo"] = 1
    
    def get_record(self):
        return self.pinyin, self.pf
