from flask import render_template,request,redirect,session
from app import app
import time   
from models import Admins   #models
from models import Shops   
from models import Msgs
from models import Users
from models import Shopflow

@app.route('/admin',methods=['GET'])
def admin():
	return render_template('admin/adminLogin.html')


@app.route('/adminLogin',methods=['POST'])
def adminLogin():
	if request.method == 'POST':
		u = Admins()
		email= request.form.get('email')
		pwd= request.form.get('pwd')
		u = Admins.objects(email=email,pwd=pwd).first()
		if u!=None:
			adminbean = {'id':str(u._id),'email':u.email,'role':u.role}
			# print(loginbean)
			session['adminbean'] = adminbean
			return redirect('/adminhome')  #重定向
		else:
			return ('<script>alert("账号/密码错误");location.href="/";</script>')


@app.route('/adminhome',methods=['GET'])
def adminhome():
	if 'adminbean' in session:  #如果拿不到session就报session过期
		adminbean = session['adminbean']
		return render_template('admin/adminhome.html',adminbean = adminbean)
	else:
		return ('<script>alert("账号信息过期，请重新登录");location.href="/";</script>')
	# return render_template('adminhome.html',adminbean = loginbean)

@app.route('/adminLogout',methods=['GET'])
def adminLogout():
	if 'adminbean' in session:
		del session['adminbean']
	return redirect('/')

#管理员界面
@app.route('/applyList',methods=['GET'])
def applyList():
	if 'adminbean' in session:
		adminbean = session['adminbean']
		#查询数据库 获得申请列表
		applist = Shops.objects(flag=0).all()  #查询所有
		# print(applist)
		return render_template('admin/applyList.html',applist = applist)
	else:
		return ('<script>alert("账号信息过期，请重新登录");location.href="/";</script>')

#管理员点击查看进入商家申请表格
@app.route('/shopinfo',methods=['GET'])
def shopinfo():
	if 'adminbean' in session:  
		adminbean = session['adminbean']
		#2.接收shopid
		shopid = request.args.get('shopid')
		#3.查库
		shopinfo = Shops.objects(_id=shopid).first()  #查询到的第一条
		# print(shopinfo)
		#4.渲染到页面
		return render_template('admin/shopinfo.html',shopinfo = shopinfo)
	else:
		return ('<script>alert("账号信息过期，请重新登录");location.href="/";</script>')

#驳回
@app.route('/refuseShopApply',methods=['POST'])
def refuseShopApply():
	if 'adminbean' in session: 
		adminbean = session['adminbean'] 
		uid = request.form.get('uid')	#get提交用args,post提交用form
		shopid = request.form.get('shopid')  #接收shopid，uid
		msg = request.form.get('msg')

		m = Msgs()
		# m['sendflag'] = 1
		m.sendflag = 0
		m.sendid = adminbean['id']
		m.sendname = '管理员'
		m.recflag = 1
		m.recid = uid
		m.msg = '您的商家申请被驳回,原因:'+msg
		m.createtime = time.time()
		m.save()
		u = Users.objects(_id = uid).update(set__role=0)
		s = Shops.objects(_id = shopid).update(set__flag=-1)
		return redirect('/applyList')
	else:
		return ('<script>alert("账号信息过期，请重新登录");location.href="/";</script>')

#审核通过  agreeShopApply
@app.route('/agreeShopApply',methods=['GET'])
def agreeShopApply():
	if 'adminbean' in session: 
		adminbean = session['adminbean']
		#接参
		shopid = request.args.get('shopid')
		uid = request.args.get('uid')
		#修改shops
		# Shopflow.objects().first().update(inc__flowid=1)
		# shopflow = Shopflow.objects().first()
		# s = Shops.objects(_id = shopid).update(set__flag=1,set__flowid=shopflow.flowid) 
		s = Shops.objects(_id = shopid).update(set__flag=1) 
		#修改users表
		u = Users.objects(_id = uid).update(set__role=3) 
		#插入msgs表
		m = Msgs()
		m.sendflag = 0
		m.sendid = adminbean['id']
		m.sendname = '管理员'
		m.recflag = 1
		m.recid = uid
		m.msg = '您的商家申请已通过审核'
		m.createtime = time.time()
		m.save()
		return redirect('/applyList')
	else:
		return ('<script>alert("账号信息过期，请重新登录");location.href="/";</script>') 