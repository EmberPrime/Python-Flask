from flask import render_template,request,session,redirect
from app import app
import os
import time
import math
from flask_uploads import UploadSet, configure_uploads, IMAGES,patch_request_class,secure_filename #上传图片
from models import Shops
from models import Dishclass
from models import Dishs

# UPLOAD_FOLDER=os.getcwd()+r'\static\photos\idcards'
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF'])

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#添加菜品 管理分类  菜单管理页面
@app.route('/menumanger',methods=['GET'])
def menumanger():
	if 'loginbean' in session: 
		loginbean = session['loginbean']
		myshops = Shops.objects(uid=loginbean['id'],flag=1).first() #多个商店为all
		dishs = Dishclass.objects(uid=loginbean['id'],shopid=myshops._id).all()

		sort = Dishclass.objects(uid=loginbean['id'],_id=myshops._id).all()
		return render_template('home/Menumanger.html',loginbean=loginbean,shopid=myshops._id,dishs=dishs)
	else:
		return ('<script>alert("账号过期请重新登录");location.href="/";</script>')

#添加菜的种类
@app.route('/addSort',methods=['POST'])
def addSort():
		
	if 'loginbean' in session:
		loginbean = session['loginbean']
		ds = Dishclass() 
		ds.shopid = request.form.get('shopid')
		ds.uid = loginbean['id']
		ds.category = request.form.get('dishclass')
		ds.save()
		return redirect('/menumanger')
	else:
		return ('<script>alert("账号过期请重新登录");location.href="/";</script>')

#删除菜的种类
# @app.route('/deldishclass',methods=['GET'])
# def deldishclass():
# 	if 'loginbean' in session: 
# 		loginbean = session['loginbean']
# 		# dishs = Dishclass.objects(uid=loginbean['id']).all()
# 		return ('<script>alert("该功能暂未开放");location.href="/menumanger";</script>')
# 	else:
# 		return ('<script>alert("账号过期请重新登录");location.href="/";</script>')

#修改菜的种类 名
@app.route('/updateSort',methods=['POST'])
def updateSort():
	if 'loginbean' in session: 
		loginbean = session['loginbean']
		sortid= request.form.get('sortid')
		newSortname= request.form.get('newSortname')
		if newSortname!='':
			dish = Dishclass.objects(_id=sortid).update(set__category=newSortname)
		return redirect('/menumanger')
		# return ('<script>alert("修改成功");location.href="/menumanger";</script>')
	else:
		return ('<script>alert("账号过期请重新登录");location.href="/";</script>')

#向种类中添加菜
@app.route('/addtoSort',methods=['POST'])
def addtoSort():
	if 'loginbean' in session: 
		loginbean = session['loginbean']
		ds = Dishs()
		if request.method == 'POST':
			d = request.files['dishphoto']
			app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+ '/static/photos/dishImg/' # 文件储存地址
			photos = UploadSet('photos', IMAGES) #创建UploadSet 拿到UploadSet对象 并设置文件类型为image
			configure_uploads(app, photos) #使用configure_uploads()方法注册并完成相应的配置
			if d and allowed_file(d.filename):  # 判断是否是允许上传的文件类型
				filename = photos.save(request.files['dishphoto'])
				dishphoto = '/static/photos/dishImg/' + filename #路径字符串
				ds.dishphoto = dishphoto
			ds.dishname = request.form.get('dishname')
			ds.price = float(request.form.get('price'))
			ds.sortid = request.form.get('sortid')
			ds.shopid = request.form.get('shopid')			
			ds.uid = loginbean['id']		
			ds.save()
		# return render_template('dish/dishmanager.html',loginbean = loginbean,dishs=dishs)
		return ('<script>alert("添加成功");location.href="/menumanger";</script>')
	else:
		return ('<script>alert("账号过期请重新登录");location.href="/";</script>')

#完整的菜单页面  左边栏的  当前菜单
@app.route('/menu',methods=['GET'])
def menu():
	if 'loginbean' in session: 
		loginbean = session['loginbean']
		sortid = request.args.get('sortid')
		shop = Shops.objects(uid=loginbean['id'],flag=1).first() #查找店面
		dish = Dishs.objects(uid=loginbean['id'],sortid=sortid).all() #查找这类菜下有几个菜
		return render_template('dish/allmenu.html',loginbean=loginbean,dish=dish)
	else:
		return ('<script>alert("账号过期请重新登录");location.href="/";</script>')
