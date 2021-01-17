from flask import Flask
from flask import Blueprint, render_template
from flask_login import LoginManager, login_required, current_user
from flask_socketio import SocketIO, emit, send
from flask_sqlalchemy import SQLAlchemy

import threading

from stock import check_stock_quote
from auth import auth as auth_blueprint
from models import db, User

# create application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jobsitysecretkey'
app.register_blueprint(auth_blueprint)

# bind database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)

# create and bind login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# create and bind socket io
io = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
@login_required
def chat_window():
    return render_template('chat.html', name=current_user.name)

# store message history (50 last)
messages = []

@io.on('sendMessage')
def send_message_handler(msg):

    name = msg['name']
    text = msg['message']
    try:
        command_start = text.index("/stock=")
    except ValueError:
        if len(messages) == 50:
            messages.pop(0)
        messages.append(msg)
        emit('getMessage', msg, broadcast=True)
    else:
        code_start = command_start + 7
        if code_start == len(text):
            # ex: "hello bot /stock="
            bot_msg = "You forgot to inform a stock code."
        elif text[code_start] == " ":
            # ex: "hello bot /stock= " <-- blank after command
            # ex: "hello bot /stock= thank you" <-- blank after command
            bot_msg = "The command stock was incorrectly used."
        else:
            bot_msg = "Wait a moment. I am processing your stock quote request."
            code_end = text.find(" ", code_start)
            if code_end > 0:
                # ex: "hello bot /stock=aapl.us " <-- blank after code
                # ex: "hello bot /stock=aapl.us thank you" <-- blank after code
                code = text[code_start:code_end]
            else:
                # ex: "hello bot /stock=aapl.us" <-- code at the end
                code = text[code_start:]

            class AsyncStock(threading.Thread):
                def run(self):
                    rabbitmq_msg = check_stock_quote(code)
                    print(rabbitmq_msg)

            async_check_stock = AsyncStock()
            async_check_stock.start()

        emit('getMessage', {'name':name, 'message':bot_msg}, broadcast=True)

@io.on('message')
def message_handler(msg):
    send(messages)

if __name__ == "__main__":
    io.run(app, debug=True)