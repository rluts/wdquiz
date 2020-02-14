from flask import Flask, request, jsonify

from core.exceptions import FileTypeError, NotFoundError
from converters.images import Image
from quiz import Quiz


app = Flask(__name__)

ANONYMOUS_USER_ID = 1
SPA_ROOM_ID = 1
SPA_GAME_CATEGORY_ID = 1
BACKEND = 'api'


@app.route('/ask', methods=['POST'])
def ask():
    try:
        quiz = Quiz(
            initiator=ANONYMOUS_USER_ID,
            category_id=SPA_GAME_CATEGORY_ID,
            room_id=SPA_ROOM_ID,
            backend=BACKEND
        )
        img, answers = quiz.img_ask()
    except (FileTypeError, NotFoundError) as e:
        return e.msg, e.code
    try:
        image = str(Image(img, quiz.room_id)).split('/')[-1]
        return jsonify(url=image)
    except AttributeError:
        return "Image not found", 404


@app.route('/check', methods=['POST'])
def check():
    data = request.json
    result = data.get('answer')
    if result:
        if result in Quiz.get_answers(SPA_ROOM_ID):
            return jsonify(result='OK')
        else:
            return jsonify(result='FAIL')
