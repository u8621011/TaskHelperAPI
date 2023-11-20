from flask import Flask, Response, request, jsonify
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://chat.openai.com", "https://chat.openai.com"]}})  # 允許 chatgpt 的 CORS 請求


# 保存 todo 的地方，當 python 案例重啟後就會消失。
_TODOS = {}

@app.route("/todos/<string:username>", methods=['POST'])
def add_todo(username):
    data = request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(data["todo"])
    return 'OK', 200

@app.route("/todos/<string:username>", methods=['GET'])
def get_todos(username):
    return jsonify(_TODOS.get(username, []))

# ChatGPT 目前並不支援 DELETE。使用 HTTP DELETE 會失敗，改用 POST 來 workaround
#@app.route("/todos/<string:username>", methods=['DELETE'])
#def delete_todo(username):
@app.route("/todos/cancel/<string:username>", methods=['POST'])
def cancel_todo(username):
    data = request.get_json(force=True)
    todo_idx = data["todo_idx"]
    # fail silently, it's a simple plugin
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return 'OK', 200


@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'