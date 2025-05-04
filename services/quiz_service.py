from models.quiz import Quiz
from database.db import db

def save_quiz_result(user_id, category, score, duration):
    quiz = Quiz(user_id=user_id, category=category, score=score, duration=duration)
    db.session.add(quiz)
    db.session.commit()
    return quiz