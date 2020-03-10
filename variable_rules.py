from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/user/<username>')    #default string
def show_user_profile(username):
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')    #post_id type int
def show_post(post_id):
    return 'Post %d' % post_id

@app.route('/float/<float:float_number>')    #float_number type float
def show_float(float_number):
    return 'Float %f' % float_number 

@app.route('/path/<path:subpath>')    #subpath type path 
def show_subpath(subpath):
    return 'Subpath %s' % escape(subpath)
if __name__ == '__main__':
    app.run("127.0.0.1", 5000, debug=True)
