from flask import Flask, render_template, request, jsonify
import base64
import requests
import logging
import markdown
import os
import google.generativeai as genai

app = Flask(__name__)

API_KEY = "AIzaSyBPgXeivnFmtX6-PSu3XudU0-EraotrYf4"
genai.configure(api_key=API_KEY)

logging.basicConfig(level=logging.DEBUG)

model = genai.GenerativeModel('gemini-1.5-flash')
chat_session = model.start_chat(history=[])

@app.route('/')
def index():
    return render_template('index.html')

def replace_words(text, replacements):
    for old_word, new_word in replacements.items():
        text = text.replace(old_word, new_word)
    return text

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

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        logging.debug("Response JSON: %s", response_json)

        generated_content = response_json.get('candidates')[0]['content']['parts'][0]['text']

        replacements = {'Google': 'Neural Networker Team', 'Gemini': 'I.R.I.S', 'Gemini 1.5 Flash model': 'I.R.I.S model', 'Sundar Pichai': 'Shah Ram', 'Alphabet': 'AI/ML Developer', '2015': '2024', 'Larry Page and Sergey Brin': 'Shah Ram'}
        generated_content = replace_words(generated_content, replacements)

        if generated_content:
            html_content = markdown.markdown(generated_content)
            chat_session.send_message(text_input)
            chat_session.send_message(generated_content)
            return jsonify({'generated_content': html_content})
        else:
            return jsonify({'error': 'Failed to generate content.'}), 500

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return jsonify({'error': 'Internal Server Error.'}), 500

@app.route('/chat', methods=['POST'])
def chat_response():
    try:
        user_input = request.form['user_input']
        logging.debug("User input: %s", user_input)

        if user_input.lower() != 'exit':
            response = chat_session.send_message(user_input)
            bot_response = response.text

            replacements = {'Google': 'Neural Networker Team', 'Gemini': 'I.R.I.S', 'Gemini 1.5 Flash model': 'I.R.I.S model', 'Sundar Pichai': 'Shah Ram', 'Alphabet': 'AI/ML Developer', '2015': '2024', 'Larry Page and Sergey Brin': 'Shah Ram'}
            bot_response = replace_words(bot_response, replacements)

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
