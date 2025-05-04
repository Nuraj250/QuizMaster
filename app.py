from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from database.db import db
from models.user import User
from models.quiz import Quiz
from models.question import Question
from services.openai_service import generate_questions
from services.auth_service import register_user, authenticate_user
from services.quiz_service import save_quiz_result
from services.leaderboard_service import get_leaderboard
from services.email_service import init_mail, send_challenge_email
from utils.utils import login_required, admin_required
from utils.timer import QuizTimer

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and email
db.init_app(app)
init_mail(app)

@app.before_first_request
def create_tables():
    db.create_all()

# ---- ROUTES ---- #

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))

        register_user(username, email, password)
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        category = request.form['category']
        session['quiz_category'] = category

        questions = generate_questions(category)
        session['quiz_questions'] = questions
        session['current_question'] = 0
        session['score'] = 0
        session['timer'] = QuizTimer().start()

        return redirect(url_for('quiz'))
    return render_template('dashboard.html')

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    questions = session.get('quiz_questions')
    if not questions:
        return redirect(url_for('dashboard'))

    current = session.get('current_question', 0)

    if request.method == 'POST':
        selected = request.form['option']
        correct = questions[current]['correct_option']

        if selected == correct:
            session['score'] += 1
        
        session['current_question'] += 1
        current += 1

        if current >= len(questions):
            duration = QuizTimer().stop() if session.get('timer') else 0
            save_quiz_result(
                user_id=session['user_id'],
                category=session['quiz_category'],
                score=session['score'],
                duration=duration
            )
            flash(f'Quiz completed! Your score: {session["score"]}/{len(questions)}')
            session.pop('quiz_questions', None)
            session.pop('current_question', None)
            session.pop('score', None)
            return redirect(url_for('dashboard'))

    question = questions[current]
    return render_template('quiz.html', question=question, number=current + 1)

@app.route('/leaderboard')
@login_required
def leaderboard():
    board = get_leaderboard()
    return render_template('leaderboard.html', leaderboard=board)

@app.route('/challenge', methods=['GET', 'POST'])
@login_required
def challenge():
    if request.method == 'POST':
        friend_email = request.form['email']
        sender_name = User.query.get(session['user_id']).username
        challenge_link = url_for('register', _external=True)
        send_challenge_email(friend_email, sender_name, challenge_link)

        flash('Challenge email sent successfully!')
        return redirect(url_for('dashboard'))
    return render_template('challenge_friend.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('home'))

# ---- Admin Routes ---- #

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    questions = Question.query.filter_by(approved=False).all()
    return render_template('admin.html', questions=questions)

@app.route('/approve_question/<int:question_id>')
@login_required
@admin_required
def approve_question(question_id):
    question = Question.query.get_or_404(question_id)
    question.approved = True
    db.session.commit()
    flash('Question approved.')
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_question/<int:question_id>')
@login_required
@admin_required
def reject_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question rejected and deleted.')
    return redirect(url_for('admin_dashboard'))

# ---- RUN SERVER ---- #

if __name__ == '__main__':
    app.run(debug=True)
