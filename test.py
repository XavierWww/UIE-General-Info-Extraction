'''
@Author: Xavier WU
@Date: 2022-08-09
@LastEditTime: 2022-08-30
@Description: This file is for testing resume info extraction results. 
@All Right Reserve
'''

from paddlenlp import Taskflow
from seqeval.metrics import classification_report
from seqeval.scheme import IOBES
  
mapping_dic = {
    '姓名': 'NAME',
    '国籍': 'CONT',
    '民族': 'RACE',
    '学历': 'EDU',
    '组织': 'ORG',
    '职位': 'TITLE',
    '居住地': 'LOC',
    '专业': 'PRO'
}
schema = ['姓名', '国籍', '民族', '学历', '组织', '职位', '居住地', '专业']
acc = 0.5
ie = Taskflow('information_extraction', schema=schema, position_prob=acc, device_id=1)

'''
    读取数据
'''
def read_data(path):
    sents_list = []
    tags_list = []
    with open(path, 'r', encoding="utf-8") as f:
        data = f.read()
        examples = data.split("\n\n")
        for e in examples:
            lines = e.split("\n")
            sents = []
            tags = []
            for line in lines:
                line = line.strip()
                if line == "":
                    continue
                char, tag = line.split(" ")
                if tag[0] == 'M':
                    tag = 'I'+tag[1:]
                sents.append(char)
                tags.append(tag)
            if len(sents) == 0:
                continue
            sents_list.append(sents)
            tags_list.append(tags)
    temp =  ["".join(i) for i in sents_list]
    return sents_list, tags_list, temp

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
        # sents: '高勇：男，中国国籍，无境外居留权，'
        # res: {'姓名': [{'text': '高勇', 'start': 0, 'end': 2, 'probability': 0.9856215395192862}], '国籍': [{'text': '中国国籍', 'start': 5, 'end': 9, 'probability': 0.9691900758494185}]}
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
    
    path = './data/test.char.bmes'
    sents_list, tags_list, input_data = read_data(path)
    res = ie(input_data)
    pred_list = zipped(input_data, res)
    print(classification_report(tags_list, pred_list, mode='strict', scheme=IOBES))
