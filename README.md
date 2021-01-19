# python_challenge
Simple browser-based chat application using Python

## Description
This project is designed to test your knowledge of back-end web technologies, specifically in
Python and assess your ability to create back-end products with attention to details, standards,
and reusability.

## Assignment
The goal of this exercise is to create a simple browser-based chat application using Python.
This application should allow several users to talk in a chatroom and also to get stock quotes
from an API using a specific command.

## Mandatory Features
* Allow registered users to log in and talk with other users in a chatroom.
* Allow users to post messages as commands into the chatroom with the following format 
/stock=stock_code
* Create a decoupled bot that will call an API using the stock_code as a parameter
(https://stooq.com/q/l/?s=aapl.us&f=sd2t2ohlcv&h&e=csv, here aapl.us is the stock_code)
* The bot should parse the received CSV file and then it should send a message back into
the chatroom using a message broker like RabbitMQ. The message will be a stock quote
using the following format: “APPL.US quote is $93.42 per share”. The post owner will be the bot.
* Have the chat messages ordered by their timestamps and show only the last 50 messages.
* Unit test the functionality you prefer.

## Bonus (Optional)
* Have more than one chatroom.
* Handle messages that are not understood or any exceptions raised within the bot.

## How-To Use
```sh
git clone https://github.com/carlosost/python_challenge.git
cd python_challenge
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```
* Open a browser and type http://127.0.0.1:5000/
* Click on "Sign Up" or "Login" and use one of the pre registered users bellow:
    * email: user1@email.com pass: user1
    * email: user2@email.com pass: user2