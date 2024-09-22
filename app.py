from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 定义题目
questions = [
    {
        'question': '在陽性物質的基礎上所產生陰證 , 應屬於何種病證?',
        'options': ['氣虛', '血瘀'],
        'answer': '氣虛'
    },
    {
        'question': '依據五行理論的特性 , 五臟中何者屬於陽?',
        'options': ['肝, 心', ' 肺, 腎'],
        'answer': '肝, 心'
    }
]

@app.route('/')
def index():
    session['current_question'] = 0
    session['score'] = 0
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    current_question = session.get('current_question', 0)

    if request.method == 'POST':
        if 'option' in request.form:
            selected_option = request.form['option']
            if selected_option == questions[current_question]['answer']:
                session['score'] += 1
                session['correct_answer'] = True
            else:
                session['correct_answer'] = False

            session['is_answered'] = True
            return redirect(url_for('question'))

    is_answered = session.get('is_answered', False)
    correct_answer = session.get('correct_answer', None)

    if current_question < len(questions):
        return render_template(
            'question.html',
            question=questions[current_question],
            question_index=current_question + 1,
            total_questions=len(questions),
            is_answered=is_answered,
            correct_answer=correct_answer
        )
    else:
        return redirect(url_for('result'))

@app.route('/next', methods=['POST'])
def next_question():
    session['current_question'] += 1
    session['is_answered'] = False
    session['correct_answer'] = None
    return redirect(url_for('question'))

@app.route('/previous', methods=['POST'])
def previous_question():
    session['current_question'] -= 1
    session['is_answered'] = False
    session['correct_answer'] = None
    return redirect(url_for('question'))

@app.route('/result')
def result():
    score = session.get('score', 0)
    total_questions = len(questions)
    return render_template('result.html', score=score, total=total_questions)

if __name__ == '__main__':
    app.run(debug=True)