from app import app
import routes.index
import routes.user
import routes.home
import routes.admin
import routes.setting
import routes.dish


# app = Flask(__name__)

if __name__ == '__main__':
	app.run(debug = True)



# 指明端口
# if __name__ == '__main__':
# 	app.run(host = '0.0.0.0',port=5000,debug = True)

# 有了 debug = True 就能热启动

