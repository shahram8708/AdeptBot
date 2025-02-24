from flask import Flask, render_template, request, jsonify
import base64
import requests
import logging
import markdown
import os

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

class HealthModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.chat_history = []

    def start_chat(self):
        self.chat_history = []

    def send_message(self, message):
        self.chat_history.append({'role': 'user', 'content': message})
        response = self.generate_response(message)
        self.chat_history.append({'role': 'bot', 'content': response})
        return response

    def generate_response(self, message):
        return ("To process your input, please ensure the model is connected and running on an NVIDIA GPU. If the issue persists even after proper GPU setup, make sure the trained model is correctly loaded. Load and run the trained model IRIS-MEDx-1.0 to receive accurate responses.")

model = HealthModel('IRIS-MEDx-1.0')
model.start_chat()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_content', methods=['POST'])
def generate_content():
    try:
        payload = request.json
        logging.debug("Request payload: %s", payload)

        if 'contents' not in payload or not payload['contents']:
            return jsonify({'error': 'Invalid request payload.'}), 400

        text_input = payload['contents'][0]['parts'][0]['text']
        image_base64 = payload['contents'][0]['parts'][1]['inlineData']['data']
        image_data = base64.b64decode(image_base64)

        response_text = model.generate_response(text_input)
        html_content = markdown.markdown(response_text)

        model.send_message(text_input)
        model.send_message(response_text)

        return jsonify({'generated_content': html_content})

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return jsonify({'error': 'Internal Server Error.'}), 500

@app.route('/chat', methods=['POST'])
def chat_response():
    try:
        user_input = request.form['user_input']
        logging.debug("User input: %s", user_input)

        if user_input.lower() != 'exit':
            bot_response = model.send_message(user_input)
            bot_response_html = markdown.markdown(bot_response)
        else:
            bot_response_html = markdown.markdown("Chat ended. Please refresh the page to start a new chat.")

        return jsonify(user_input=user_input, bot_response=bot_response_html)

    except Exception as e:
        logging.error("An error occurred in chat: %s", str(e))
        return jsonify({'error': 'Internal Server Error.'}), 500

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
    return response

if __name__ == '__main__':
    app.run(debug=True)
