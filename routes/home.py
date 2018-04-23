from flask import render_template,request,session,redirect
from app import app
import os
import time
import math
from flask_uploads import UploadSet, configure_uploads, IMAGES,patch_request_class,secure_filename #上传图片
from models import Shops
from models import Msgs
from models import Users


# UPLOAD_FOLDER=os.getcwd()+r'\static\photos\idcards'
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF'])

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+ '/static/photos/idcards/' # 文件储存地址
photos = UploadSet('photos', IMAGES) #创建UploadSet 拿到UploadSet对象 并设置文件类型为image
configure_uploads(app, photos) #使用configure_uploads()方法注册并完成相应的配置

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/home',methods=['GET'])
def home():
	if 'loginbean' in session:  #如果拿不到session就报session过期
		loginbean = session['loginbean']
		return render_template('home/home.html',loginbean = loginbean)
	else:
		return ('<script>alert("账号信息过期，请重新登录");location.href="/";</script>')

@app.route('/shopapply',methods=['GET'])
def shopapply():
	if 'loginbean' in session:  #如果拿不到session就报session过期
		loginbean = session['loginbean']
		shopRs = Shops.objects(uid = loginbean['id'],flag=-1).first()
		return render_template('home/shopapply.html',loginbean = loginbean)
	else:
		return ('<script>alert("账号信息过期，请重新登录");location.href="/";</script>')

#提交申请信息
@app.route('/subapply',methods=['POST'])
def subapply():
	if 'loginbean' in session: 
		loginbean = session['loginbean']
		if request.method == 'POST':
			shop = Shops()
			shop['uid'] = loginbean['id']
			shop['shopname'] = request.form.get('shopname')
			shop['address'] = request.form.get('address')
			shop['lng'] = float(request.form.get('lng'))
			shop['lat'] = float(request.form.get('lat'))
			shop['tel'] = request.form.get('tel')
			print(shop['lng'])
			print(shop['lat'])

			fArr = ('idcard','ownercard','blicense','hlicense')
			for item in fArr:
				f = request.files[item]
				if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
					filename = photos.save(request.files[item])
					shop[item] = '/static/photos/idcards/' + filename

			updtime = time.time()
			shop.updtime = updtime
			shop.createtime = updtime
			shop.flag = 0
			
			shop.save()
			#----修改users表中role=2(审核中)---------
			u = Users.objects(_id = shop.uid).update(set__role=2)
			loginbean['role'] = 2
			session['loginbean'] = loginbean
		# return redirect('/home')
		return ('<script>alert("提交成功");location.href="/home";</script>')
	else:
		return ('<script>alert("账号信息过期，请重新登录");location.href="/";</script>')

# myMsg
@app.route('/myMsg',methods=['GET'])
def myMsg():
	if 'loginbean' in session: 
		loginbean = session['loginbean']
		msglist = Msgs.objects(recid=loginbean['id'],recflag=1).order_by('-createtime').all()
		for item in msglist:
			date = time.localtime(math.floor(item.createtime))
			item.createtime = str(date.tm_year)+'年'+str(date.tm_mon)+'月'+str(date.tm_mday)+'日 '+str(date.tm_hour)+":"+str(date.tm_min)
	return render_template('home/msgs.html',loginbean = loginbean,msglist=msglist)

