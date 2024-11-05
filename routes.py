from flask import render_template, request, redirect, url_for
from database import db, User, Answer
from questions import QUESTIONS


def register_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            user_name = request.form['name']
            user = User.query.filter_by(name=user_name).first()

            if user:
                return redirect(url_for('questions', user_id=user.id))
            else:
                user = User(name=user_name)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('questions', user_id=user.id))

        return render_template('home.html')

    @app.route('/questions/<int:user_id>', methods=['GET', 'POST'])
    def questions(user_id):
        user = User.query.get_or_404(user_id)

        if user.current_question >= len(QUESTIONS):
            return redirect(url_for('thanks', user_id=user.id))

        current_question_text = QUESTIONS[user.current_question]

        if request.method == 'POST':
            answer_text = request.form['answer']
            answer = Answer(
                question=current_question_text,
                answer=answer_text,
                user_id=user.id)
            db.session.add(answer)

            user.current_question += 1
            db.session.commit()

            return redirect(url_for('questions', user_id=user.id))

        return render_template(
            'questions.html',
            question=current_question_text,
            user=user)

    @app.route('/thanks/<int:user_id>')
    def thanks(user_id):
        user = User.query.get_or_404(user_id)
        return render_template('thanks.html', user=user)

    @app.route('/responses/<int:user_id>')
    def responses(user_id):
        user = User.query.get_or_404(user_id)
        answers = Answer.query.filter_by(user_id=user.id).all()
        return render_template('responses.html', user=user, answers=answers)
