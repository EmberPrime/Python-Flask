from flask import render_template,request,redirect,session
from app import app
import os
import time
from models import Users   #models

# 注册
@app.route('/zhuce',methods=['POST'])
def zhuce():
	if request.method == 'POST':
		u = Users()
		list = ['nickname','email','pwd','tel']
		for item in list:
			u[item] = request.form.get(item)
		u.role = 1
		u.msgnum = 0
		updtime = time.time()
		u.headImg = '/static/photos/headImg/basic.jpg'
		u.bgimg = '/static/img/bg4.jpg'
		u.updtime = updtime
		u.createtime = updtime

		try:
			u.save()
			return ('<script>alert("注册成功");location.href="/";</script>')
		except Exception as err:
			estr = str(err)
			if estr.find('emailuiq')>0:
				return ('<script>alert("邮箱已被注册");location.href="/";</script>')
			elif estr.find('teluiq')>0:
				return ('<script>alert("手机号码已被注册");location.href="/";</script>')
			else:
				return '数据库异常'	

# 登录
@app.route('/login',methods=['POST'])
def login():
	if request.method == 'POST':
		u = Users()
		email= request.form.get('email')
		pwd= request.form.get('pwd')
		u = Users.objects(email=email,pwd=pwd).first()
		if u!=None:
			loginbean = {'id':str(u._id),'nickname':u.nickname,'tel':u.tel,'role':u.role,'msgnum':u.msgnum,'headImg':u.headImg,'bgimg':u.bgimg}
			session['loginbean'] = loginbean
			return redirect('/')  #重定向
		else:
			return ('<script>alert("账号/密码错误");location.href="/";</script>')

#注销
@app.route('/logout',methods=['GET'])
def logout():
	if 'loginbean' in session:
		del session['loginbean']
	return redirect('/')

		