from flask import Flask, render_template, request
from chatbot import chatbotextention
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbotextention(userText))


if __name__ == "__main__":
    app.run()

#to run flask app
#set FLASK_app=app.py
#flask run
