# app.py
from flask import Flask, render_template, request, jsonify
import openai
from openai import OpenAI
from response import get_gpt_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message']
    gpt_response = generate_gpt_response(user_message)
    return gpt_response

def generate_gpt_response(user_message):
    get_gpt_response(user_message)

if __name__ == '__main__':
    app.run(debug=True)
