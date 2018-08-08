# -*- coding:utf-8 -*-
# 业主姓名、业主电话、代理人姓名、代理人电话、预算
import re
import os

file = r'E:\hongxing1\0808_1.txt'
wfile=r'E:\hongxing1\result0808_1.txt'

if(os.path.exists(wfile)):
    os.remove(wfile)
f1=open(file,'r')

# regId=re.compile(r'^[A-Za-z0-9-]+$')
# regPhone=re.compile(r"(\d{3,4}-\d{8,9})|(13\d|14[579]|15[^4\D]|17[^49\D]|18\d)\d{8}")
regId=re.compile(r'[A-Za-z-]*\d+')
# regId=re.compile(r'[A-Za-z-\d{3,4,5,6,7,8}]*')
regName=re.compile(r'[\u4e00-\u9fa5]+')
regPhone=re.compile(r'(\d{3}-\d{8}|\d{4}-\d{7,8})|(\d{11})|(\d{7,8})') #3位区号+8位/4位区号+7位或8位/11位手机号/8位固话
regBudget=re.compile(r'\d+[.,]*\d*')
# regTime=re.compile(r'(\d+[-/]\d+[-/]\d+:\d+)|(\d+\u5E74\d+\u6708\d+\u65E5\d{1,2}[:：]\d{1,2}\u65F6)|(\d+\u5E74\d+\u6708\d+\u65E5\d{1,2}[:：]\d{1,2})|(\d+\u5E74\d+\u6708\d+\u65E5)') #以“-”或"/"分隔的日期/以年月日分隔的日期

str="文件名称"+"\t"+"业主姓名"+"\t"+"业主电话"+"\t"+"代理人姓名"+"\t"+"代理人电话"+"\t"+"预算（万元）"+"\n"

count=0

for line in f1.readlines():
    ID = ""
    HOST_NAME = ""
    HOST_PHONE = ""
    AGENT_NAME=""
    AGENT_PHONE=""
    BUDGET=""
    BIG_OPEN=""
    DEADLINE=""
    lt=line.split('@@')

    # 提取编号
    hostid=regId.findall(lt[0])
    for i in hostid:
        ID=ID+i

    # 提取业主联系人
    if(lt[1]!=""):
        name=lt[1][-3:]
        hostname=regName.findall(name)
        for i in hostname:
            HOST_NAME=HOST_NAME+i
        if(len(HOST_NAME)<2 or HOST_NAME=="联系"):
            HOST_NAME=""
        if(HOST_NAME[-1:]=="联"or HOST_NAME[-1:]=="电"):
            HOST_NAME=HOST_NAME[-3:-1]
    # else:
    #     continue
    # print(NAME)

    # 提取业主电话号码
    hostphone = regPhone.findall(lt[2])
    if(len(hostphone)>0):
        for j in hostphone[0]:
            HOST_PHONE=HOST_PHONE+j
        # print(PHONE)
    # else:
    #     continue

    # 提取代理联系人
    if(lt[3]!=""):
        name=lt[3][-3:]
        agentname=regName.findall(name)
        for i in agentname:
            AGENT_NAME=AGENT_NAME+i
        if(AGENT_NAME[-1:]=="联"or AGENT_NAME[-1:]=="电"):
            AGENT_NAME=AGENT_NAME[-3:-1]
        if(len(AGENT_NAME)<2):
            AGENT_NAME=""

    # 提取代理电话号码
    agentphone = regPhone.findall(lt[4])
    if(len(agentphone)>0):
        for j in agentphone[0]:
            AGENT_PHONE=AGENT_PHONE+j
        # print(PHONE)

    # 提取预算
    budget = regBudget.findall(lt[5])
    if(len(budget)>0):
        for k in budget[0]:
            BUDGET=BUDGET+k

    str = str + lt[8].replace("\n","") + "\t" +  HOST_NAME + "\t" + HOST_PHONE + "\t" + AGENT_NAME + "\t" + AGENT_PHONE + "\t" + BUDGET  + "\n"

    count=count+1

f1.close()
fo=open(wfile,"w")
fo.write(str)
fo.close()

print("Finish...")
print("Total number of data is %d"%count)

# 838
