# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   transfer_raw_to_rasa_nlu.py
 
@Time    :   2019-09-25 14:23
 
@Desc    :  将处理好的对话数据转换为rasa nlu数据
 
'''

import json
import requests
import pypinyin
from pypinyin import lazy_pinyin
import copy
from time_convert import TimeNormalizer


# url = 'http://172.18.103.43:8000/api/payback_class'
url = 'http://172.18.103.43:8009/api/intent_class'
id2label = {0:"will_pay", 1:"not_pay", 2:"payed", 3:"ask_probelm", 4:"other"}

# id2label = {"接受":"accept", 1:"deny", 2:"busy", 3:"notimepay", 4:"wrongcall", 5:"zhapian", 6:"unkonwn", }
def build_stand_sen(file, text):
    dic = json.load(open(file, "r"))
    maps = dic.keys()
    maps = sorted(maps, key=lambda x: len(dic[x]))
    for i in maps:
        for j in dic[i]:
            if j in text:
                return lazy_pinyin(i)
    return ['-1']

# def build_stand_sen(file, text):
#     dic = json.load(open(file, "r"))
#     maps = dic.keys()
#     maps = sorted(maps, key=lambda x: len(dic[x]))
#     temp, word = [], []
#     for i in maps:
#         for j in dic[i]:
#             if j in text:
#                 label = [1 if j in w or w in j else 0 for w in word]
#                 if 1 in label:
#                     continue
#                 temp.append("".join(lazy_pinyin(i)))
#                 word.append(j)
#                 break
#     if temp == []:
#         res = "other"
#     else:
#         res = "+".join(temp)
#     return res


def get_intent_slot_rawdata(in_file, out_file, file4):
    '''
    从原始对话数据中提取意图和实体
    :param in_file:
    :param out_file:
    :return:
    '''
    fou = open(out_file, 'w', encoding='utf-8')
    with open(in_file, encoding='utf-8') as fin:
        ssss = []
        for row in fin.readlines():
            if row.startswith('A:'):
                # 请求意图和实体接口
                try:
                    if len(row.strip().split('\t')) < 2:
                        continue
                    text = row.strip().split('\t')[1]
                    intent = ''.join(build_stand_sen(file4, text))

                    # res = requests.post(url, json={"msg": que_})
                    # reponse = json.loads(res.content).get('res1', '-1')
                    # repon = sorted([{'intent':w['intent'], 'prob':w['prob']} for w in reponse if 'sentence' in w.keys()], key = lambda x:x['prob'], reverse=True)

                    if intent == '-1':
                        intent = 'other'
                    ssss.append(intent)
                    time = ''
                    fou.write(text + '\t' + intent + '\t' + time + '\n')
                    print(intent)
                except Exception as e:
                    print(str(e))
        for i in set(ssss):
            print('- ' + i)

def rawdata2rasa(in_file, out_file):
    '''

    :param in_file:
    :param out_file:
    :return:
    '''
    fout = open(out_file, 'w', encoding='utf-8')
    with open(in_file, encoding='utf-8') as fin:
        train_set = {}
        train_set["rasa_nlu_data"] = {}
        train_set["rasa_nlu_data"]["common_examples"] = []
        train_set["rasa_nlu_data"]["regex_features"] = []
        train_set["rasa_nlu_data"]["entity_synonyms"] = []

        dict_set = []
        entities_name = []
        for line in fin:
            if line.strip() == "":
                continue
            elif "\t" in line:
                entities_name = []
                cols = line.strip().split("\t")
                for name in cols[2:]:
                    entities_name.append(name)
            tokens = line.strip().split('\t')
            common_example = {}
            common_example["text"] = tokens[0]
            common_example["intent"] = tokens[1]
            common_example["entities"] = []

            if len(tokens) < 3:
                train_set["rasa_nlu_data"]["common_examples"].append(common_example)
                continue
            entitiys = tokens[2].split(",")
            entitiys = entitiys[:1]
            for i, e in enumerate(entitiys):
                try:
                    start = tokens[0].index(e)
                    end = tokens[0].index(e) + len(e)
                    entity = {}
                    entity["start"] = start
                    entity["end"] = end
                    entity["value"] = e
                    # entity["entity"] = entities_name[0]
                    entity["entity"] = "time"
                    common_example["entities"].append(entity)
                    dict_set.append(e)
                    # print start, end,  tokens[0][start:end]
                except:
                    # print line
                    pass

            train_set["rasa_nlu_data"]["common_examples"].append(common_example)

        fout.write(json.dumps(train_set, ensure_ascii=False, indent=2))
        dict_set = set(dict_set)
        for e in dict_set:
            print(e)


if __name__ == '__main__':

    file1 = '/home/xsq/nlp_code/Dialogue_management/data/dialogue/dialogue0925.txt'

    file2 = '/home/xsq/nlp_code/Dialogue_management/data/dialogue/dialogue_with_label_3.txt'

    file3 = '/home/xsq/nlp_code/Dialogue_management/data/dialogue/rasa_nlu.json'

    file4 = '/home/xsq/nlp_code/Dialogue_management/data/intends2.json'

    # build_stand_sen(file4)

    # get_intent_slot_rawdata(file1, file2, file4)

    rawdata2rasa(file2, file3)

