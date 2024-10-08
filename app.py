from flask import Flask, render_template, request, redirect, url_for, session
import random 

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define questions
def import_question():
    folder = "../CA_Acupuncture_Exam/講義/"
    # file = "Q&A-1 中醫基礎 p01"
    file = "Q&A-6 針灸 IIa p01"
    # file = "Q&A-9 方劑 p01"
    ###
    foler_file_name = folder + file + ".txt"
    with open(foler_file_name, "r", encoding='utf-8') as f: 
            data = f.readlines()
    q = []
    s1 = []
    s2 = []
    s3 = []
    s4 = []
    a = []
    for i in range (0,len(data)):
        # print(i%3)
        # print(data[i])
        if i%7 == 0:
            q.append(data[i].replace('\n', ''))
        if i%7 == 1:
            s1.append(data[i].replace('\n', ''))
        if i%7 == 2:
            s2.append(data[i].replace('\n', ''))
        if i%7 == 3:
            s3.append(data[i].replace('\n', ''))
        if i%7 == 4:
            s4.append(data[i].replace('\n', ''))
        if i%7 == 5:
            a.append(data[i].replace('\n', ''))

    c = list(zip(q,s1,s2,s3,s4,a))
    random.shuffle(c)
    q,s1,s2,s3,s4,a = zip(*c)

    questions = []

    for i in range(0,len(q)):
        if a[i] == '1':
            ans = s1[i]
        elif a[i] == '2':
            ans = s2[i]
        elif a[i] == '3':
            ans = s3[i]
        elif a[i] == '4':
            ans = s4[i]

        dic = {
        'question': q[i],
        'options': [s1[i],s2[i],s3[i],s4[i]],
        'answer': ans
        }
        questions.append(dic)
    return questions

questions = import_question()

# questions = [
#     {
#         'question': '在陽性物質的基礎上所產生陰證 , 應屬於何種病證?',
#         'options': ['氣虛', '血瘀'],
#         'answer': '氣虛'
#     },
#     {
#         'question': '依據五行理論的特性 , 五臟中何者屬於陽?',
#         'options': ['肺, 腎','肝, 心'],
#         'answer': '肝, 心'
#     }
# ]

@app.route('/')
def index():
    session['current_question'] = 0
    session['score'] = 0
    session['answered_questions'] = []  # Keep track of answered questions
    session['incorrect_questions'] = []
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    current_question = session.get('current_question', 0)

    if request.method == 'POST':
        if 'option' in request.form:
            selected_option = request.form['option']
            if selected_option == questions[current_question]['answer']:
                if current_question not in session['answered_questions']:
                    try:
                        if session['is_answered'] == False:
                            session['score'] += 1
                    except:
                        session['score'] += 1
                    # session['answered_questions'].append(current_question)  # Mark question as answered correctly
                session['correct_answer'] = True
            else:
                session['incorrect_questions'].append({
                        'question': questions[current_question]['question'],
                        'correct_answer': questions[current_question]['answer']
                    })
                session['correct_answer'] = False
            session['answered_questions'].append(current_question)
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
    total_score = round((score / total_questions) * 100, 2) if total_questions > 0 else 0
    incorrect_questions = session.get('incorrect_questions', [])
    return render_template('result.html', score= score, total_questions = total_questions, total_score=total_score, total=100, incorrect_questions=incorrect_questions)  # Show out of 100

if __name__ == '__main__':
    app.run(debug=True)