from converters.images import Image
from quiz import Quiz

if __name__ == '__main__':
    # quick example
    ROOM_ID = 8888
    quiz = Quiz(category_id=1, initiator=123, room_id=ROOM_ID, backend='api')
    img, answers, question_id, question = quiz.ask_image_type()
    image = str(Image(img, quiz.room_id, question_id))
    print(Quiz.get_answers(ROOM_ID))
    print(image)
