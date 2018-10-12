#-*- coding:utf-8 -*-
## 2018-10-9
## 优化了提取联系人
import re
from flask import Flask,jsonify,request,abort,json

app=Flask(__name__)

@app.route('/')
def index():
	return 'Hello,world!'

@app.errorhandler(404)
def not_found(error):
	return jsonify({'error':'Not found'}),404

@app.route('/read')
def read(id,data):

	ch2 = ['联系人：', '联系人:', '联系人姓名：','采购人：','联系人1：','采购经办人：','项目负责人：']
	ch3 = ['联系人']
	name = ['李','王','张','刘','陈','杨','赵','黄','周','吴','徐','孙','胡','朱','高','林','何','郭','马','罗','梁','宋','郑','谢','韩','唐','冯','于','董','萧','程','曹','袁','邓','许','傅','沈','曾','彭','吕','苏','卢','蒋','蔡','贾','丁','魏','薛','叶','阎','余','潘','杜','戴','夏','钟','汪','田','任','姜','范','方','石','姚','谭','廖','邹','熊','金','陆','郝','孔','白','崔','康','毛','邱','秦','江','史','顾','侯','邵','孟','龙','万','段','漕','钱','汤','尹','黎','易','常','武','乔','贺','赖','龚','文']

	ch4 = ['代理机构：', '代理单位：', '代理机构名称：','招标代理：','代理机构','代理公司']

	ch5 = ['预算：', '预算:','预算金额：', '预算金额:','预算总额：','预算总额:','预算总价：','预算总价:','预算价：','工程概算：','造价：','工程合同估算价：','工程估算价（万元）：', '项目投资：','投标报价上限为','预算金额（元）','投资额','预算总金额','造价约','最高限价：','投标报价上限为','工程合同估算价：','采购预算金额','预算金额为￥','采购项目预算','工程总投资约', '总投资','￥']

	ch6 = "开标时间"
	ch7 = "截止时间"
	# 开标时间、截至时间补充信息
	ch8 = ['招标公告日期']
	line = data
	str31 = ""
	str32 = ""
	str41 = ""
	str42 = ""
	str5 = ""
	str6 = ""
	str7 = ""
	# agent：“代理机构”位置
	agent = len(line)
	# 查找预算所在内容
	for i in ch5:
		if (line.find(i) != -1):
			str5 = line[line.find(i):line.find(i) + 20]
			break

	# 查找“代理机构”字段
	for i in ch4:
		if (line.find(i) != -1):
			agent = line.find(i)
			break

	# str3存储业主信息，str4存储代理机构信息
	str3 = line[:agent]
	str4 = line[agent:]

	# 查找业主姓名、电话
	k=0
	for i in ch2:
		if (str3.find(i) != -1):
			str31 = str3[str3.find(i): str3.find(i) + 7]  # 业主姓名所在信息
			str32 = str3[str3.find(i) + 7: str3.find(i) + 30]  # 业主电话所在信息
			k=k+1
			break

	if(k == 0):
		for i in name:
			tem=ch3[0]+i
			if (str3.find(tem)!=-1):
				str31 = str3[str3.find(tem): str3.find(tem) + 6]  # 业主姓名所在信息
				str32 = str3[str3.find(tem) +6: str3.find(i) + 25]  # 业主电话所在信息
				break

	# 查找代理机构姓名、电话
	k=0
	for i in ch2:
		if (str4.find(i) != -1):
			str41 = str4[str4.find(i):str4.find(i) + 7]  # 代理姓名所在信息
			str42 = str4[str4.find(i) + 7:str4.find(i) + 30]  # 代理电话所在信息
			k=k+1
			break
	if (k == 0):
		for i in name:
			tem = ch3[0] + i
			if (str4.find(tem) != -1):
				str41 = str4[str4.find(tem): str4.find(tem) + 6]  # 业主姓名所在信息
				str42 = str4[str4.find(tem) + 6: str4.find(i) + 25]  # 业主电话所在信息
				break

	# 查找开标时间
	str6 = line[line.find(ch6):line.find(ch6) + 30]
	# 查找截止时间
	str7 = line[line.find(ch7):line.find(ch7) + 30]
	# 将“招标公告日期”加入上述时间
	for i in ch8:
		if (line.find(i) != -1):
			strgg = line[line.find(i):line.find(i) + 40]
			strgg_list = strgg.split("\u81F3")  # “至”
			if (len(strgg_list) > 1):
				str6 = str6 + strgg_list[0]
				str7 = str7 + strgg_list[1]
			break

	str = id+ "@@"+str31 + "@@" + str32 + "@@" + str41 + "@@" + str42 + "@@" + str5 + "@@" + str6 + "@@" + str7

	return str

@app.route('/bids',methods=['POST'])
def bids():
	# if not request.json or not 'data' in request.json:
	# 	# abort(400)
	# print(request.data.decode("utf-8"))
	# print(request.data[0])
	# request.setCharacterEncoding("UTF-8")

	# id=request.json['id']
	# data=request.json['data']

	# param = json.dumps(request.data.decode("utf-8"),ensure_ascii=False) --json转str
	# str转json
	param=json.loads(request.data.decode("utf-8"))
	# print(type(param),param)

	id=param['id']
	data=param['data']

	ID="http://www.qianlima.com/zb/detail/20180830_"+id+".html"

	f1=read(id,data)
	# regId = re.compile(r'[A-Za-z-]*\d+')
	regName = re.compile(r'[\u4e00-\u9fa5]+')
	regPhone = re.compile(r'(\d{3}-\d{8}|\d{4}-\d{7,8})|(\d{11})|(\d{7,8})')  # 3位区号+8位/4位区号+7位或8位/11位手机号/8位固话
	regBudget = re.compile(r'\d+[.,]*\d*')
	budget_Y=['万元','亿元','元']
	# 存储各字段数据的字典
	bid={}

	f2=f1.split('\n')
	for line in f2:
		HOST_NAME = ""
		HOST_PHONE = ""
		AGENT_NAME = ""
		AGENT_PHONE = ""
		BUDGET = ""
		BIG_OPEN = ""
		DEADLINE = ""
		lt = line.split('@@')

		# 提取业主联系人
		if (lt[1] != ""):
			name = lt[1][-3:]
			hostname = regName.findall(name)
			for i in hostname:
				HOST_NAME = HOST_NAME + i
			if (len(HOST_NAME) < 2 or HOST_NAME == "联系"):
				HOST_NAME = ""
			if (HOST_NAME[-1:] == "联" or HOST_NAME[-1:] == "电"):
				HOST_NAME = HOST_NAME[-3:-1]

		# 提取业主电话号码
		hostphone = regPhone.findall(lt[2])
		if (len(hostphone) > 0):
			for j in hostphone[0]:
				HOST_PHONE = HOST_PHONE + j

		# 提取代理联系人
		if (lt[3] != ""):
			name = lt[3][-3:]
			agentname = regName.findall(name)
			for i in agentname:
				AGENT_NAME = AGENT_NAME + i
			if (len(HOST_NAME) < 2 or HOST_NAME == "联系"):
				HOST_NAME = ""
			if (AGENT_NAME[-1:] == "联" or AGENT_NAME[-1:] == "电"):
				AGENT_NAME = AGENT_NAME[-3:-1]

		# 提取代理电话号码
		agentphone = regPhone.findall(lt[4])
		if (len(agentphone) > 0):
			for j in agentphone[0]:
				AGENT_PHONE = AGENT_PHONE + j
			# print(PHONE)

		# 提取预算
		budget = regBudget.findall(lt[5])
		if (len(budget) > 0):
			for k in budget[0]:
				BUDGET = BUDGET + k
		for i in budget_Y:
			if (lt[5].find(i) != -1):
				BUDGET=BUDGET+i
				break

		bid={'id':ID,'hostname':HOST_NAME,'hostphone':HOST_PHONE,'agentname':AGENT_NAME,'agentphone':AGENT_PHONE,'budget':BUDGET}

	# return jsonify({'id':bid['id'],'budget':bid['budget']})
	return jsonify(bid)

if __name__=='__main__':
	# app.run(debug=True)
    host="127.0.0.1"
    # host="192.168.20.145"
    # host="39.106.184.74"
    port="5000"
    app.run(host=host,port=port)