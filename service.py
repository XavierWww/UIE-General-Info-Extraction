'''
@Author: Xavier WU
@Date: 2022-08-09
@LastEditTime: 2022-08-30
@Description: This file is resume and general info extraction server. 
@All Right Reserve
'''

import sanic.response
import json
from sanic import Sanic
from paddlenlp import Taskflow
from collections import OrderedDict
import re

class TaskExtractionService:
    
    def __init__(self, name, host, port):
        
        self.host = host
        self.port = port
        self.app = Sanic(name)
        self.app_add_routes()
        self.response = None
        self.schema = ['姓名', '国籍', '民族', '居住地', '学历', '专业', '组织', '职位']
        self.schema2 = ['地址', '书名', '公司', '游戏', '政府', '电影', '姓名', '机构组织', '职位', '景点']
        self.acc = 0.6
        self.ie = Taskflow('information_extraction', schema=self.schema, position_prob=self.acc, device_id=1)
        self.ie2 = Taskflow('information_extraction', schema=self.schema2, position_prob=self.acc, device_id=1)
        self.app.run(host=self.host, port=self.port)

    def app_add_routes(self):
        
        self.app.add_route(self.resume_info_extraction, "/resume_info_extraction", methods=["POST"])
        self.app.add_route(self.general_info_extraction, "/general_info_extraction", methods=["POST"])

    def general_info_extraction(self, request):
        
        init_vocab = '[\\[\\]{《》}【】]'
        raw_text = request.body.decode('utf-8')
        raw_text = json.loads(raw_text)
        raw_text = [re.sub(init_vocab, " ", t) for t in raw_text]  
        uie_outputs = self.ie2(raw_text)           # 抽取
        new_outputs = self.process2(uie_outputs)   # 处理
        return sanic.response.json(new_outputs, ensure_ascii=False)
    
    def resume_info_extraction(self, request):

        init_vocab = '[\\[\\]{《》}【】]'
        raw_text = request.body.decode('utf-8')
        raw_text = json.loads(raw_text)
        raw_text = [re.sub(init_vocab, " ", t) for t in raw_text]  
        uie_outputs = self.ie(raw_text)          # 抽取
        new_outputs = self.process(uie_outputs)  # 处理
        return sanic.response.json(new_outputs, ensure_ascii=False)
                        
    '''
        对抽取结果进行处理
    '''
    def process(self, uie_list):
        
        res = []
        init_vocab = '[@!"#$%^&*\+_~\\[\\];:?“”‘’。！,、·？__{|}<=>]'            
        # 对每一条抽取结果里每个实体类别的抽取信息进行处理
        for dic in uie_list:
            res_dict = {
                '姓名': '',
                '国籍': '',
                '民族': '',
                '居住地': '',
                '学历': '',
                '专业': '',
                '组织': '',
                '职位': ''
            }
            for s in self.schema:
                if dic.get(s):
                    dic[s].sort(key=lambda e: (e['start']))
                    if s == '学历' or s == '专业' or s == '组织' or s == '职位':
                        if res_dict.get(s) == '':      
                            res_dict[s]=[]
                        for i in dic[s]:
                            res_dict[s].append(re.sub(init_vocab, "", i['text'].strip().replace(" ", "").replace("\n", "")))
                    else:
                        if res_dict.get(s) == '':
                            res_dict[s] = re.sub(init_vocab, "", dic[s][0]['text'].strip().replace(" ", "").replace("\n", ""))
            res.append(res_dict)
        return res
    
    '''
        对抽取结果进行处理
    '''
    def process2(self, uie_list):
        
        res = []
        # 对每一条抽取结果里每个实体类别的抽取信息进行处理
        for dic in uie_list:
            res_dict  = OrderedDict()
            for s in self.schema2:
                if dic.get(s):
                    temp = []
                    dic[s].sort(key=lambda e: (e['start']))
                    for i in dic[s]:
                        temp.append(i['text'].strip().replace("\n", ""))
                    res_dict[s] = temp
            res.append(res_dict)
        return res
    
if __name__ == '__main__':
    host = '0.0.0.0' # 192.168.50.121 0.0.0.0
    port = 8080 # 8989 8080
    Service1 = TaskExtractionService('service', host, port)  # build service
     