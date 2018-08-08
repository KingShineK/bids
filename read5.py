#-*- coding:utf-8 -*-
import re
import os
from tqdm import tqdm

path=r'E:\hongxing'
wfile=r'E:\hongxing1\0808_1.txt'
os.chdir(path)

if(os.path.exists(wfile)):
    os.remove(wfile)

ch1="编号"#16个字符
ch21="联系人："#7个字符
ch21_1="联系人姓名："
ch22="联系人:"#7个字符
ch2_reg=re.compile(r'(\u8054\u7CFB\u4EBA[:：])|(\u6709\u610F\u8005\u53EF\u4E0E)')#联系人：、有意者可与
ch3="电话"#17个字符
# ch3_reg=re.compile(r'\u8054\u7CFB\u4EBA[\u4e00-\u9fa5]*[：]\u7535\u8BDD[：]\d+')
ch4="代理机构："
ch4_1="代理单位："
ch4_2="代理机构名称："
# ch5="万元"
# ch5="预算"
ch5_reg=re.compile(r'\u9884\u7B97([\u4e00-\u9fa5][^(\u7F16\u53F7)])*[:：]|\u9020\u4EF7\u7EA6\d+\u4E07\u5143|\u603B\u6295\u8D44|\u9884\u7B97\u4EF7[：]\d+') # 直接查找“预算：”字段，中间可包含其他汉字但是不能为“编号”或搜索造价为、总投资、工程预算
ch6="开标时间" #25个字符
ch7="截止时间"
ch8_reg=re.compile(r'\u62DB\u6807\u516C\u544A\u65E5\u671F') #“招标公告日期”后截40个字符

count=0
str=""
for filename in tqdm(os.listdir()):
    file = open(filename,'r')
    for line in file.readlines():
        str31 = ""
        str32 = ""
        str41 = ""
        str42 = ""
        str5 = ""
        str6 = ""
        str7 = ""
        #查找编号字段
        str1 = line[line.find(ch1):line.find(ch1) + 30]
        #查找联系人、联系方式字段
        str2 = line[int(len(line)*1/5):]
        #查找预算字段
        ch5=ch5_reg.search(line)
        if(ch5 is not None):
            str5 = line[ch5.span()[0]:ch5.span()[0] + 15]

        #查找联系人
        #ch2=ch2_reg.search(str2)
        #if (ch2 is not None):
         #   str31 = line[ch2.span()[0]:ch2.span()[0] + 7]

        #查找开标时间
        str6 = line[line.find(ch6):line.find(ch6) + 30]
        #查找截止时间
        str7 = line[line.find(ch7):line.find(ch7) + 30]
        #将“招标公告日期”加入上述时间
        ch8 = ch8_reg.search(line)
        if (ch8 is not None):
            strgg = line[ch8.span()[0]:ch8.span()[0] + 40]
            strgg_list=strgg.split("\u81F3") # “至”
            if (len(strgg_list) > 1):
                str6=str6+strgg_list[0]
                str7=str7+strgg_list[1]
            else:
                pass

        ####  查找业主、代理机构信息
        # 查找“代理机构”字段
        if str2.find(ch4)!=-1:
            agent=str2.find(ch4)
        elif(str2.find(ch4_1)!=-1):
            agent=str2.find(ch4_1)
        elif (str2.find(ch4_2) != -1):
            agent = str2.find(ch4_2)
        else:
            agent=len(str2);
        #str3存储业主信息，str4存储代理机构信息
        str3=str2[:agent]
        str4=str2[agent:]
        # 查找业主姓名、电话
        if(str3.find(ch22)!=-1):
            str31 = str3[str3.find(ch22):str3.find(ch22) + 7]  # 截取业主信息
            str32 = str3[str3.find(ch22) + 7:str3.find(ch22) + 30]  # 查找联系人，从其后信息查找电话
        elif(str3.find(ch21) != -1):
            str31 = str3[str3.find(ch21):str3.find(ch21) + 7]  # 截取业主信息
            str32 = str3[str3.find(ch21) + 7:str3.find(ch21) + 30]  # 查找联系人，从其后信息查找电话
        elif (str3.find(ch21_1) != -1):
            str31 = str3[str3.find(ch21_1):str3.find(ch21_1) + 9]  # 截取业主信息
            str32 = str3[str3.find(ch21_1) + 9:str3.find(ch21_1) + 30]  # 查找联系人，从其后信息查找电话
        else:
            str31=""
            str32=""
        # 查找代理机构姓名、电话
        if agent!=len(str2):
            if (str4.find(ch22) != -1):
                str41 = str4[str4.find(ch22):str4.find(ch22) + 7]  # 截取代理信息
                str42 = str4[str4.find(ch22) + 7:str4.find(ch22) + 30]
            elif(str4.find(ch21) != -1):
                str41 = str4[str4.find(ch21):str4.find(ch21) + 7]  # 截取代理信息
                str42 = str4[str4.find(ch21) + 7:str4.find(ch21) + 30]
            elif (str4.find(ch21_1) != -1):
                str41 = str4[str4.find(ch21_1):str4.find(ch21_1) + 9]  # 截取代理信息
                str42 = str4[str4.find(ch21_1) + 9:str4.find(ch21_1) + 30]
            else:
                str41 = ""
                str42 = ""

        str = str+str1+ "@@" + str31 + "@@" + str32 + "@@"+str41+"@@"+str42+"@@"+str5+"@@"+str6+"@@"+str7+"@@"+filename+"\n"

    file.close()

fo = open(wfile, "w")
fo.write(str)
fo.close()

print("Finish...")
# print("Total number of file is %d"%count)

# 858