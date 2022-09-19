# -*- coding: utf-8 -*-

'''
@Author: Xavier WU
@Date: 2022-08-09
@LastEditTime: 2022-08-30
@Description: This file is resume and general info extraction client. 
@All Right Reserve
'''

import requests
import json

url = 'http://192.168.50.121:8989/resume_info_extraction'   # 简历服务地址
url = 'http://192.168.50.121:8989/general_info_extraction'  # 通用服务地址

input_data = [
    '''常建良，男，1963年出生，工科学士，高级工程师，北京物资学院客座副教授。1985年8月—1993年在国家物资局、物资部、国内贸易部金属材料流通司从事国家统配钢材中特种钢材品种的全国调拔分配工作，先后任科员、副主任科员、主任科员。1993年5月—1999年5月受国内贸易部委派到国内贸易部、冶金部、天津市政府共同领导组建的北洋(天津)钢材批发交易市场任理事长助理、副总裁。1999年5月—2010年4月任天津一德投资集团有限公司董事。2010年5月任天津一德投资集团公司董事、副总裁。''', 
    '''陈学军先生：1967年5月出生，大学毕业，高级经济师。1986年7月进入无锡威孚高科技集团股份有限公司。历任公司采供处处长兼党支部书记，党委工作处处长。无锡威孚高科技集团股份有限公司第四届、第五届监事会主席，第六届董事会副董事长兼总经理，第七届董事会董事长。现任大股东无锡产业发展集团有限公司董事局董事、无锡威孚高科技集团股份有限公司党委书记。'''
]

input_data = [
    '''6月15日，河南省文物考古研究所曹操高陵文物队公开发表声明承认：“从来没有说过出土的珠子是墓主人的''', 
    '''诸侯曰类宫。”东汉蔡邕的《明堂丹令论》解释为：“取其四面环水，圆如壁，后世遂名辟雍。”魏晋南北朝、'''
]

resp = requests.request("POST", url, data=json.dumps(input_data)) 
print(json.dumps(resp.json(), ensure_ascii=False, indent=4))