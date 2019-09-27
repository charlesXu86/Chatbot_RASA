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

url = 'http://172.18.103.43:8000/api/payback_class'

id2label = {0:"will_pay", 1:"not_pay", 2:"payed", 3:"ask_probelm", 4:"other"}

def get_intent_slot_rawdata(in_file, out_file):
    '''
    从原始对话数据中提取意图和实体
    :param in_file:
    :param out_file:
    :return:
    '''
    fou = open(out_file, 'w', encoding='utf-8')
    with open(in_file, encoding='utf-8') as fin:
        for row in fin.readlines():
            if row.startswith('A:'):
                # 请求意图和实体接口
                try:
                    text = row.strip().split('\t')[1]
                    res = requests.post(url, json={"msg": text})
                    label = int(json.loads(res.content).get('res1', '-1'))
                    intent = id2label[label]
                    times = json.loads(res.content).get('pay_tim', '-1')
                    if 'key' in times:
                        time = times['key']
                    fou.write(text + '\t' + intent + '\t' + time + '\n')
                    print(res)
                except:
                    pass






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
            common_example["intent"] = tokens[1]     # 这个下面还要再加一个置信度
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
                    entity["entity"] = entitiys
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
    file2 = '/home/xsq/nlp_code/Dialogue_management/data/dialogue/dialogue_wih_label.txt'

    file3 = '/home/xsq/nlp_code/Dialogue_management/data/dialogue/rasa_nlu.json'
    # get_intent_slot_rawdata(file1, file2)

    rawdata2rasa(file2, file3)