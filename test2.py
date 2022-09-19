'''
@Author: Xavier WU
@Date: 2022-08-31
@LastEditTime: 2022-08-31
@Description: This file is for testing general info extraction results. 
@All Right Reserve
'''

import os
import json 
from paddlenlp import Taskflow
from seqeval.metrics import classification_report
from seqeval.scheme import IOBES

mapping_dic = {
    '地址': 'address',
    '书名': 'book',
    '公司': 'company',
    '游戏': 'game',
    '政府': 'government',
    '电影': 'movie',
    '姓名': 'name',
    '机构组织': 'organization',
    '职位': 'position',
    '景点': 'scene',
}
schema = ['地址', '书名', '公司', '游戏', '政府', '电影', '姓名', '机构组织', '职位', '景点']
acc = 0.5
ie = Taskflow('information_extraction', schema=schema, position_prob=acc, device_id=1)

'''
    读取数据
'''
def load_dataset(mode="dev"):
    assert mode in ["train", "dev", "test"]
    data_path = os.path.join(path, mode+".json")
    labels = []
    texts = []
    with open(data_path, "r", encoding="utf-8") as f:
        for line in f:
            # 保存该行样本整理后的数据
            line = json.loads(line.strip())
            text = line["text"]
            texts.append(text)
            tag_entities = line.get("label", None)
            words = list(text)
            tags = ["O"] * len(words)
            if tag_entities is not None:
                for tag_name, tag_value in tag_entities.items():
                    for entity_name, entity_index in tag_value.items():
                        for start_index, end_index in entity_index:
                            assert "".join(words[start_index:end_index+1]) == entity_name
                            if start_index == end_index:
                                tags[start_index] = "S-" + tag_name
                            else:
                                tags[start_index] = "B-" + tag_name
                                tags[start_index + 1:end_index] = ["I-" + tag_name] * (len(entity_name) - 2)
                                tags[end_index] = "E-" + tag_name
            labels.append(tags)
    return texts, labels

'''
    返回UIE抽取结果
''' 
def uie_extract(data):
    return ie(data)

'''
    对齐预测结果和标签
'''
def zipped(sents_list, uie_res):
    
    #sents_list: [, ,]
    #uie_res: [{}, {}, {}]
    tags_list = []
    for sents, res in zip(sents_list, uie_res):
        temp = ['O' for _ in range(len(sents))]
        if not res:
            tags_list.append(temp)
        else:
            # 返回标注后的 list
            temp = gen_tags(res, temp)
            tags_list.append(temp)
    return tags_list

'''
    为每一个句子生成tag
'''
def gen_tags(dic_list, tagged_list):
    
    for k, v in dic_list.items():
        for en in v:
            text = en['text']
            s_pos = en['start']
            e_pos = en['end']
            tags = mapping(text, mapping_dic, k)
            for i in range(s_pos, e_pos):
                tagged_list[i] = tags[i-s_pos]
    return tagged_list

'''
    为句子中每个实体的token打上tag
'''     
def mapping(text, dic, type):
    
    temp = [('I-'+ dic[type]) for _ in range(len(text))]
    if len(text) == 1:
        return ['S-'+dic[type]]
    else:
        temp[0] = 'B-'+dic[type]
        temp[-1] = 'E-'+dic[type]
    return temp   

if __name__ == "__main__":
    
    path = './data2'
    texts, labels = load_dataset(mode="dev")
    res = ie(texts)
    pred_list = zipped(texts, res)
    print(classification_report(labels, pred_list, mode='strict', scheme=IOBES))
    