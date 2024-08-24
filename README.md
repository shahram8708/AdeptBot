# AdeptBot

AdeptBot is a chat application built with Flask, which integrates with Google’s Gemini Generative AI model. It allows users to interact with an AI bot through text and image inputs. The application includes features for saving chat history, image previews, and audio playback of messages.

## Features

- **Chat with the AI Bot:** Send text and images to receive responses from the AI.
- **Image Upload:** Upload images that the AI can process and generate content based on them.
- **Text-to-Speech:** Play back text responses using speech synthesis.
- **Message Copying:** Copy messages to the clipboard.
- **Chat History:** Save and load chat history using local storage.
- **User Interface:** A responsive and user-friendly chat interface.

## Requirements

- Python 3.x
- Flask
- requests
- markdown
- google-generativeai

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shahram8708/adeptbot.git
   cd adeptbot
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Replace the `API_KEY` in `app.py` with your Google Generative AI API key:

   ```python
   API_KEY = "your_api_key_here"
   ```

2. Ensure you have the necessary credentials and access for the Google Generative AI API.

## Running the Application

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000` to use the chat application.

## Endpoints

### `GET /`

- Renders the main chat interface.

### `POST /generate_content`

- **Request:** JSON payload with text and image content.
- **Response:** Generated content from the AI based on the provided input.

### `POST /chat`

- **Request:** Form data with user input text.
- **Response:** AI’s response to the user input.

## Usage

1. **Send a Message:** Enter text in the input field and click "Send" to communicate with the bot.
2. **Upload an Image:** Click the image icon to upload an image. The bot will process the image and generate a response.
3. **Play Audio:** Click the play button to hear the bot’s response.
4. **Copy Message:** Use the copy button to copy the message to the clipboard.
5. **Delete Chat:** Click "Delete Chat" to clear the chat history.

## Troubleshooting

- Ensure your API key is correctly set and has the necessary permissions.
- Check for any network issues if the application fails to make API requests.
- Review the Flask server logs for detailed error messages if you encounter issues.
