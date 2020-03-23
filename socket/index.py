from flask import Flask, request, abort, render_template, jsonify
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/message", methods=['POST'])
def upload():
    try:
        test = request.json
        id = test['ID']
        msg = test['Message']
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data = {"id":id,"msg":msg,"date":date}
        socketio.emit('status_response', data)
        return jsonify(
            {"response": "ok"}
        )
    except:
        pass

    # 回傳給前端
@app.route("/")
def home():
    return render_template('index.html', async_mode=socketio.async_mode)


if __name__ == "__main__":
    socketio.run(app, debug=True)
