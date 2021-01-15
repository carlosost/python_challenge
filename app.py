from flask.app import Flask
from flask.templating import render_template
from flask_socketio import SocketIO, emit, send
import threading
from stock import check_stock_quote

app = Flask(__name__)
app.secret_key = 'jobisty_secret_key'
io = SocketIO(app)

messages = []

@app.route("/")
def home():
    return render_template("chat.html")

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

    "012 4/stock="