from flask import Flask, send_from_directory, send_file, request, render_template, redirect, url_for
import os
import json
from flask_pymongo import PyMongo
import flask_login
import time
from flask_socketio import SocketIO, emit

#初始化 
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config["MONGO_URI"] = "mongodb://localhost:27017/water"
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
mongo = PyMongo(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

class User(flask_login.UserMixin):
    pass
@login_manager.user_loader
def user_loader(id):
    if mongo.db.user.count({"id": id}) == 0:
        return

    user = User()
    user.id = id
    return user


@login_manager.request_loader
def request_loader(request):
    id = request.form.get('id')
    if mongo.db.user.count({"id": id}) == 0:
        return
    if(request.form['password'] == mongo.db.user.find({"id": id})[0]['password']):
        user = User()
        user.id = id
        return user
    return
#傳送訊息api
@app.route("/message", methods=['POST'])
def upload():
    try:
        test = request.json
        id = flask_login.current_user.id
        msg = test['Message']
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data = {"id":id,"msg":msg,"date":date}
        socketio.emit('status_response', data)
        return {"response": "ok"}
    except:
        return {"response": "error"},422

# 回傳給前端
@app.route("/index")
@flask_login.login_required
def home():
    return render_template('chat.html', async_mode=socketio.async_mode, id=flask_login.current_user.id)

#登入首頁
@app.route('/', methods=['GET', 'POST'])
def index():
    if (flask_login.current_user.is_active):
        user = User()
        user.id = flask_login.current_user.id
        flask_login.login_user(user)
        return redirect(url_for("home"))
    else:
        if request.method == 'POST':
            id = request.form.get('id')
            password = request.form.get('password')
            try:
                if mongo.db.user.find({"id": id})[0]['password'] == password:
                    user = User()
                    user.id = id
                    flask_login.login_user(user)
                    return redirect(url_for("home"))
                else:
                    return render_template("login.html", error="帳號或密碼錯誤")
            except:
                return render_template("login.html", error="帳號或密碼錯誤")
        return render_template("login.html")

#登出
@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("index"))
#註冊
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        id = request.form.get('id')
        name = request.form.get('name')
        password = request.form.get('password')
        block = {'id': id, 'name': name, 'password': password}
        if mongo.db.user.count({"id": id}) >= 1:
            return render_template("register.html", error="帳號已使用")
        else:
            mongo.db.user.insert_one(block)
            return render_template("register.html", error="註冊成功")

if __name__ == '__main__':
    socketio.run(app, debug=True)

