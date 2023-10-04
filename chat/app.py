import json
import logging as log
import os
from threading import Lock

from flask import render_template, request, Blueprint, jsonify

from .preload import *
from .tts import *

loop = asyncio.get_event_loop()

log.basicConfig(level=log.INFO)

chat_bp = Blueprint(name="chat", import_name=__name__, url_prefix='/')

# 每建立一次会话，就缓存一个用户id
user_token = {}

lock = Lock()

@chat_bp.route('/')
def home():
    return render_template('index.html')


@chat_bp.route('/get_response', methods=['POST'])
def get_bot_response():
    try:
        if lock.acquire():
            global user_token
            user_id = request.json.get('id')
            user_input = request.json.get('user_input')
            if user_token.get(user_id) is None:
                user_token.setdefault(user_id, [])
            history = user_token.get(user_id)
            response, history = model.chat(tokenizer, query=user_input, history=history, top_p=0.8, temperature=0.9,
                                           max_length=2048)
            q, a = history[-1]
            xml_ = f"""
                <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
                <voice name="zh-CN-XiaoxiaoNeural">
                    <prosody rate="0%" pitch="0%">
                    {a}
                    </prosody>
                </voice>
            </speak>
                """
            id = uuid.uuid1().hex
            filename = id + '.wav'
            gen_file = os.path.join('static', 'output', filename)
            gen_wav(xml_, gen_file)
            write_to_json(a, filename)
            user_token[user_id] = history
            return a
        else:
            return '忙碌中...'
    except (Exception) as e:
        log.info(e)
    finally:
        lock.release()


def gen_wav(t:str, path):
    loop.run_until_complete(mainSeq(t, path))

@chat_bp.route('/reset')
def reset():
    global user_token
    user_token.clear()
    return "重置成功！"


@chat_bp.route('/static/output/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        file_path = os.path.join('static/output', filename)
        os.remove(file_path)
        remove_from_json(filename)
        return jsonify({'message': 'File deleted successfully'})
    except OSError as e:
        return jsonify({'message': 'Error deleting file: ' + str(e)}), 500


def write_to_json(text_input, filename):
    data = {}
    json_file = os.path.join('static/json', 'barkwebui.json')
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log.info(e)

    file_id = os.path.splitext(filename)[0]


    data = {file_id: {
        'textInput': text_input,
        'outputFile': filename
    }}

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)


def remove_from_json(filename):
    data = {}
    json_file = os.path.join('static/json', 'barkwebui.json')
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    file_id = os.path.splitext(filename)[0]


    if file_id in data:
        del data[file_id]

    if not data:
        os.remove(json_file)
    else:
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
