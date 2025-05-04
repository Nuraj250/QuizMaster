from models.quiz import Quiz
from models.user import User

def get_leaderboard(limit=10):
    leaderboard = (
        Quiz.query
        .join(User)
        .add_columns(User.username, Quiz.score, Quiz.duration, Quiz.category)
        .order_by(Quiz.score.desc(), Quiz.duration)
        .limit(limit)
        .all()
    )
    return leaderboard