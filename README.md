# I.R.I.S (Intelligent Responsive Integrated System) - AI Health Assistant

## Overview
Welcome to **I.R.I.S (Intelligent Responsive Integrated System)** — Your AI Health Assistant. This platform offers a seamless way to upload health reports and receive AI-driven suggestions for better health insights.

## Features
- **Upload Reports**: Easily upload images (like X-rays) or PDF health reports.
- **Ask Questions**: Type your health-related queries to get personalized advice.
- **Instant Feedback**: Receive AI-generated insights on your uploaded reports.
- **Secure & Private**: Your data remains confidential and secure.

## Requirements
- Python 3.7+
- NVIDIA GPU (for optimal model performance)

## Dependencies
Install the required packages using pip:

```bash
pip install Flask requests markdown
```

## Project Structure
```
├── app.py                # Main Flask application
├── templates/
│   └── index.html        # Frontend HTML template
└── README.md             # Project documentation
```

## Usage

### Running the Application
1. **Ensure NVIDIA GPU is properly configured**.
2. **Start the Flask server:**
   ```bash
   python app.py
   ```
3. **Access the app:**
   Open your browser and go to `http://127.0.0.1:5000/`

### API Endpoints

#### 1. `GET /`
- **Description:** Renders the main interface.
- **Response:** HTML page.

#### 2. `POST /generate_content`
- **Description:** Processes text and image inputs and returns a generated response.
- **Request Body (JSON):**
  ```json
  {
    "contents": [
      {
        "parts": [
          { "text": "Describe the image" },
          { "inlineData": { "data": "<base64_encoded_image>" } }
        ]
      }
    ]
  }
  ```
- **Response:**
  ```json
  {
    "generated_content": "<markdown_rendered_html>"
  }
  ```
- **Errors:**
  - `400 Bad Request` if payload is invalid.
  - `500 Internal Server Error` on server issues.

#### 3. `POST /chat`
- **Description:** Handles chat messages.
- **Form Data:**
  - `user_input`: User message.
- **Response:**
  ```json
  {
    "user_input": "<user_message>",
    "bot_response": "<markdown_rendered_response>"
  }
  ```
- **Special Command:**
  - Sending `exit` ends the chat.

### CORS
- All endpoints support CORS for cross-origin requests.

## Logging
- **Level:** DEBUG
- **Logs:**
  - Incoming requests.
  - Payload data.
  - Errors and exceptions.

## Error Handling
- Consistent JSON responses for errors.
- Proper logging of issues for easier debugging.

## Notes
- Ensure the **IRIS-MEDx-1.0** model is correctly loaded and running on an NVIDIA GPU for optimal responses.
- The app uses Markdown to format model responses.
