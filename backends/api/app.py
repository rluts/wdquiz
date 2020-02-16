from flask import Flask, request, jsonify
from flask_cors import CORS

from core.exceptions import FileTypeError, NotFoundError
from converters.images import Image
from db import session
from db.models import QuestionType
from quiz import Quiz


app = Flask(__name__)
CORS(app)

ANONYMOUS_USER_ID = 1
SPA_ROOM_ID = 1
SPA_GAME_CATEGORY_ID = 2
BACKEND = 'api'


@app.route('/ask', methods=['POST', 'OPTIONS'])
def ask():
    quiz = Quiz(
        initiator=ANONYMOUS_USER_ID,
        category_id=SPA_GAME_CATEGORY_ID,
        room_id=SPA_ROOM_ID,
        backend=BACKEND
    )
    img, answers, question_id, question = quiz.ask_image_type()

    try:
        image = Image(img, quiz.room_id, question_id, convert_svg=False)
        image = str(image).split('/')[-1]
        return jsonify(url=f'/media/{image}', question_id=question_id, question=question)
    except (FileTypeError, NotFoundError) as e:
        return e.msg, e.code
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
