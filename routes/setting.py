from flask import render_template,request,redirect,session
from flask_uploads import UploadSet, configure_uploads, IMAGES,patch_request_class,secure_filename #上传图片
from app import app
import os
import time
from models import Users   #models

# UPLOAD_FOLDER=os.getcwd()+r'\static\photos\idcards'
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#跳转到设置页面
@app.route('/setting',methods=['GET'])
def setting():
	if 'loginbean' in session:  
		loginbean = session['loginbean']
		return render_template('home/setting.html',loginbean = loginbean)
	else:
		return ('<script>alert("请先登录");location.href="/";</script>')

#更换背景
@app.route('/changeBG',methods=['GET'])
def changeBG():
	if 'loginbean' in session:  
		loginbean = session['loginbean']
		bg = request.args.get('bg')	 #获取用户选择编号
		changebg = Users.objects(_id = loginbean['id']).update(set__bgnum=bg) #修改 changebg无实意
		usersbg = Users.objects(_id = loginbean['id']).first()  #查库 得到结果集
		loginbean['bgnum']  = bg
	# return render_template('index.html')
	return ('<script>alert("提交成功");location.href="/";</script>')

#更换昵称
@app.route('/changeNickname',methods=['GET'])
def changeNickname():
	if 'loginbean' in session:  
		loginbean = session['loginbean']
		reNickname = request.args.get('Nickname') #这个Nickname是指的input表单的name,不能与<form>表单相同
		changenick = Users.objects(_id = loginbean['id']).update(set__nickname=reNickname)  
		#插库后 记得修改loginbean
		loginbean['nickname'] = reNickname
		session['loginbean'] = loginbean

	return ('<script>alert("提交成功");location.href="/setting";</script>')

#更换背景
@app.route('/changebgimg',methods=['POST'])
def changebgimg():
	if 'loginbean' in session: 
		loginbean = session['loginbean']
		try:
			if request.method == 'POST':
				q = request.files['bgimg']
				if q and allowed_file(q.filename):  # 判断是否是允许上传的文件类型
					app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+ '/static/photos/bgImg/' # 文件储存地址
					photos = UploadSet('photos', IMAGES) #创建UploadSet 拿到UploadSet对象 并设置文件类型为image
					configure_uploads(app, photos) #使用configure_uploads()方法注册并完成相应的配置
					filename = photos.save(request.files['bgimg'])
					bgimg = '/static/photos/bgImg/' + filename #路径字符串
				h = Users.objects(_id = loginbean['id']).update(set__bgimg=bgimg) #更改路径
				loginbean['bgimg'] = bgimg
				session['loginbean'] = loginbean
			return ('<script>alert("提交成功");location.href="/setting";</script>')
		except Exception as err:
			estr = str(err)
			if estr.find('before')>0:
				return ('<script>alert("图片不能为空");location.href="/setting";</script>')
	else:
		return ('<script>alert("账号信息过期，请重新登录");location.href="/";</script>')


# 更换头像测试
@app.route('/changeHeadImg',methods=['POST'])
def changeHeadImg():
	if 'loginbean' in session: 
		loginbean = session['loginbean']
		try:
			if request.method == 'POST':
				f = request.files['headImg']
				if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
					app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+ '/static/photos/headImg/' # 文件储存地址
					photos = UploadSet('photos', IMAGES) #创建UploadSet 拿到UploadSet对象 并设置文件类型为image
					configure_uploads(app, photos) #使用configure_uploads()方法注册并完成相应的配置

					filename = photos.save(request.files['headImg'])
					headImg = '/static/photos/headImg/' + filename #路径字符串
				h = Users.objects(_id = loginbean['id']).update(set__headImg=headImg) #更改路径
				loginbean['headImg'] = headImg
				session['loginbean'] = loginbean
			return ('<script>alert("提交成功");location.href="/setting";</script>')
		except Exception as err:
			estr = str(err)
			if estr.find('before')>0:
				return ('<script>alert("图片不能为空");location.href="/setting";</script>')
	else:
		return ('<script>alert("账号信息过期，请重新登录");location.href="/";</script>')