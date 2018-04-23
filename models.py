from flask import Flask
from flask_mongoengine import MongoEngine

app=Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
	'db': 'finger',
	'host':'localhost',
	'port':27017
}
#创建mongo原型
mdb = MongoEngine()
mdb.init_app(app)

# print(dir(mdb))  输出所有的类型

#类名定义 collection
class Users(mdb.Document):
	_id = mdb.ObjectIdField()
	nickname = mdb.StringField()
	pwd = mdb.StringField()
	email = mdb.StringField()
	tel = mdb.StringField()
	updtime = mdb.FloatField()
	createtime = mdb.FloatField()
	msgnum = mdb.IntField()
	bgimg = mdb.StringField()  #上传背景图片路径
	headImg = mdb.StringField()  #头像路径
	role = mdb.IntField()  #1普通用户2 店铺审核 3 商家  -1表示禁止 0再次申请

class Admins(mdb.Document):
	_id = mdb.ObjectIdField()
	# nickname = mdb.StringField()
	email = mdb.StringField()
	pwd = mdb.StringField()
	role = mdb.IntField()

class Shops(mdb.Document):  
	_id = mdb.ObjectIdField()
	uid = mdb.ObjectIdField()
	shopname = mdb.StringField()
	address = mdb.StringField()
	lng	= mdb.FloatField() 
	lat = mdb.FloatField()
	tel = mdb.StringField()
	idcard = mdb.StringField()			#身份证照片地址
	ownercard = mdb.StringField()		#手持身份证照片地址
	blicense = mdb.StringField()		#营业执照照片地址
	hlicense = mdb.StringField()		#卫生许可证照片地址
	updtime = mdb.FloatField()
	createtime = mdb.FloatField()
	flag = 	mdb.IntField()		#-2表强制终止,-1表驳回,0表审核中,1表审核通过
	flowid = mdb.LongField(default=0)  #店铺流水id

#商家流水id表
class Shopflow(mdb.Document): 
	_id = mdb.ObjectIdField()
	flowid = mdb.LongField() 

class Msgs(mdb.Document):
	_id = mdb.ObjectIdField()
	sendflag = 	mdb.IntField()	#0表管理员,1表普通用户
	sendid = mdb.ObjectIdField()
	sendname = mdb.StringField()
	recflag = mdb.IntField()		#0表管理员,1表普通用户
	recid = mdb.ObjectIdField()
	recname = mdb.StringField()
	msg = mdb.StringField()
	createtime = mdb.FloatField()

#菜的类别 比如凉菜热菜啥的
class Dishclass(mdb.Document):
	_id = mdb.ObjectIdField()
	uid = mdb.ObjectIdField()
	shopid = mdb.ObjectIdField()
	category = mdb.StringField()

#向种类添加菜名
class Dishs(mdb.Document):
	_id = mdb.ObjectIdField()
	uid = mdb.ObjectIdField()
	shopid = mdb.ObjectIdField()
	sortid = mdb.ObjectIdField() #菜的种类id
	dishname = mdb.StringField()
	dishphoto = mdb.StringField()
	price = mdb.FloatField()
	# curprice = mdb.FloatField()
	flag = 	mdb.IntField()  








