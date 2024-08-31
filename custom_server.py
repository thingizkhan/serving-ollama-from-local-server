from flask import Flask, request, jsonify
from ollama import chat
import os

app = Flask(__name__)
chat_history = []

@app.route('/chat', methods=['POST'])
def chat_route():
    user_input = request.json.get("input")
    chat_history.extend(request.json.get("history", []))  # Load the history from the request
    chat_history.append({'role': 'user', 'content': user_input})
    try:
        response = chat('qwen2:7b', messages=chat_history)
        assistant_message = response['message']
        chat_history.append(assistant_message)
        return jsonify({"output": assistant_message['content'], "history": chat_history})
    except Exception as e:
        return jsonify({"error": f"Error generating response: {str(e)}"}), 500

@app.route('/delete_history', methods=['POST'])
def delete_history():
    global chat_history
    chat_history = []
    return jsonify({"message": "History deleted"})

@app.route('/delete_chat', methods=['DELETE'])
def delete_chat():
    chat_name = request.args.get("name")
    chat_file = os.path.join('chat_histories', f"{chat_name}.json")
    if os.path.exists(chat_file):
        try:
            os.remove(chat_file)
            return jsonify({"message": "Chat deleted successfully"})
        except Exception as e:
            return jsonify({"error": f"Error deleting chat: {str(e)}"}), 500
    else:
        return jsonify({"error": "Chat not found"}), 404

@app.route('/save_chat', methods=['POST'])
def save_chat():
    chat_history = request.json.get("history")
    chat_name = request.json.get("name", "chat")
    chat_file = os.path.join('chat_histories', f"{chat_name}.json")
    try:
        with open(chat_file, 'w') as f:
            json.dump(chat_history, f)
        return jsonify({"message": "Chat history saved successfully"})
    except Exception as e:
        return jsonify({"error": f"Error saving chat history: {str(e)}"}), 500

@app.route('/load_chat', methods=['GET'])
def load_chat():
    chat_name = request.args.get("name")
    chat_file = os.path.join('chat_histories', f"{chat_name}.json")
    if os.path.exists(chat_file):
        try:
            with open(chat_file, 'r') as f:
                chat_history = json.load(f)
            return jsonify({"history": chat_history})
        except Exception as e:
            return jsonify({"error": f"Error loading chat history: {str(e)}"}), 500
    else:
        return jsonify({"history": []})

@app.route('/list_chats', methods=['GET'])
def list_chats():
    try:
        chats = [f.split(".json")[0] for f in os.listdir('chat_histories') if f.endswith(".json")]
        return jsonify({"chats": chats})
    except Exception as e:
        return jsonify({"error": f"Error listing chat histories: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

