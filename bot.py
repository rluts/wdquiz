from converters.images import Image
from quiz.quiz import Quiz

if __name__ == '__main__':
    quiz = Quiz(category_id=1, initiator=123, room_id=8888, backend='api')
    img, answers = quiz.img_ask()
    image = str(Image(img, quiz.room_id))
    print(Quiz.get_answers(8888))
    print(image)
