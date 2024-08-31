# Chat Application with Flask

This is a simple chat application built using Flask for the backend and HTML, CSS, and JavaScript for the frontend. The application allows users to chat with a model, save chat histories, and manage previous chats.

## Features

- **Chat with Model**: Users can send messages and receive responses from a model.
- **Save Chat**: Users can save their chat history with a custom name.
- **Load Chat**: Users can load previous chat histories.
- **Delete Chat**: Users can delete specific chat histories.
- **Delete History**: Users can clear the current chat history.
- **New Chat**: Users can start a new chat session.

## Setup


## File Structure

- `app.py`: Main Flask application.
- `custom_server.py`: Custom server handling chat logic.
- `templates/index.html`: Frontend HTML template.
- `static/`: Directory for static files (CSS, JS).
- `chat_histories/`: Directory where chat histories are saved.

## API Endpoints

- `POST /chat`: Send a message to the model.
- `POST /delete_history`: Clear the current chat history.
- `POST /save_chat`: Save the current chat history.
- `GET /load_chat`: Load a specific chat history.
- `GET /list_chats`: List all saved chat histories.
- `DELETE /delete_chat`: Delete a specific chat history.

## License

This project is licensed under the MIT License.