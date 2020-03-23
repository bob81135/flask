from flask import Flask, send_from_directory, send_file, request, render_template, redirect, url_for
import time
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity
import json
from flask_pymongo import PyMongo
#初始化 
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/water"
app.config['JWT_SECRET_KEY'] = 'super-secret'  
jwt = JWTManager(app)
mongo = PyMongo(app)

@app.route("/user", methods=['GET'])
@jwt_required
def get_user():
    current_user = get_jwt_identity()
    return {"logged_in_as": current_user}, 200

#登入首頁
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        test = request.json
        id = test['id']
        password = test['password']
        try:
            if mongo.db.user.find({"id": id})[0]['password'] == password:
                access_token = create_access_token(identity=id)
                
                return {"access_token": access_token},200
            else:
                return render_template("login.html", error="帳號或密碼錯誤")
        except:
            return render_template("login.html", error="帳號或密碼錯誤")
    return render_template("login.html")

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
    app.run("127.0.0.1", 5000, debug=True)

