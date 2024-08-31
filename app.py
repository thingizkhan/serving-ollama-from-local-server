from flask import Flask, render_template, request, jsonify
import os
import json
import requests

app = Flask(__name__)

SERVER_URL = 'http://192.168.1.23:5000'  # Ensure this IP and port are correct and accessible
CHAT_HISTORY_DIR = 'chat_histories'

if not os.path.exists(CHAT_HISTORY_DIR):
    os.makedirs(CHAT_HISTORY_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("input")
    chat_history = request.json.get("history", [])
    if user_input:  # Only append if there's actual user input
        chat_history.append({'role': 'user', 'content': user_input})

    try:
        response = requests.post(f"{SERVER_URL}/chat", json={"input": user_input, "history": chat_history})
        response.raise_for_status()
        data = response.json()
        assistant_message = {'role': 'assistant', 'content': data['output']}
        chat_history.append(assistant_message)
        return jsonify({"output": data['output'], "history": chat_history})
    except requests.RequestException as e:
        return jsonify({"error": f"Error communicating with server: {str(e)}"}), 500

@app.route('/delete_history', methods=['POST'])
def delete_history():
    try:
        response = requests.post(f"{SERVER_URL}/delete_history")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Error communicating with server: {str(e)}"}), 500

@app.route('/save_chat', methods=['POST'])
def save_chat():
    chat_history = request.json.get("history")
    chat_name = request.json.get("name", "chat")
    chat_file = os.path.join(CHAT_HISTORY_DIR, f"{chat_name}.json")
    try:
        with open(chat_file, 'w') as f:
            json.dump(chat_history, f)
        return jsonify({"message": "Chat history saved successfully"})
    except Exception as e:
        return jsonify({"error": f"Error saving chat history: {str(e)}"}), 500

@app.route('/load_chat', methods=['GET'])
def load_chat():
    chat_name = request.args.get("name")
    chat_file = os.path.join(CHAT_HISTORY_DIR, f"{chat_name}.json")
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
        chats = [f.split(".json")[0] for f in os.listdir(CHAT_HISTORY_DIR) if f.endswith(".json")]
        return jsonify({"chats": chats})
    except Exception as e:
        return jsonify({"error": f"Error listing chat histories: {str(e)}"}), 500

@app.route('/delete_chat', methods=['DELETE'])
def delete_chat():
    chat_name = request.args.get("name")
    chat_file = os.path.join(CHAT_HISTORY_DIR, f"{chat_name}.json")
    if os.path.exists(chat_file):
        try:
            os.remove(chat_file)
            return jsonify({"message": "Chat deleted successfully"})
        except Exception as e:
            return jsonify({"error": f"Error deleting chat: {str(e)}"}), 500
    else:
        return jsonify({"error": "Chat not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
