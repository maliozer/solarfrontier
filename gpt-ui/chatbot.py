# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import openai
from openai import OpenAI
import os

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index2.html')

@socketio.on('send_message')
def handle_message(data):
    user_message = data['message']
    gpt_response = generate_gpt_response(user_message)
    socketio.emit('receive_message', {'message': gpt_response})

def generate_gpt_response(user_message):
    # Use your OpenAI API key and choose the appropriate engine
    openai_api_key = ''
    client = OpenAI(api_key = os.getenv['YOURKEY'])
    prompt = f"User: {user_message}\nChatGPT:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with a block of text, and your task is to extract a list of keywords from it."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
    max_tokens=64
    )

    #debug
    print(response.choices[0].message.content)

    return response.choices[0].message.content

if __name__ == '__main__':
    socketio.run(app, debug=True)
