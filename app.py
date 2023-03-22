from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

""" keeps track of the user's responses"""





@app.route('/', methods = ["GET", "POST"])
def question():

    session["responses"] = []
    
    return render_template(
        'questions.html',
         title = satisfaction_survey.title,
         instructions = satisfaction_survey.instructions
    )
    


@app.route('/question/<int:id>', methods = ["GET","POST"])
def firstQuestion(id = id):
    ses = session["responses"]
    if(id > len(ses) or id < len(ses)):
        flash(" INVALID QUESTION ")
        id = len(session["responses"])
        return redirect(f"/question/{id}")
    else:
        return render_template(
            'question-one.html',
            question = satisfaction_survey.questions[id].question,
            choices = satisfaction_survey.questions[id].choices,
        )


@app.route('/answer', methods=["GET","POST"])
def nextQuestion():
    ses = session["responses"]
    session["responses"].append(request.form.get("choice"))
    session["responses"] = ses
    count = len(session["responses"]) 
    if(len(session["responses"]) != len(satisfaction_survey.questions)):
        return redirect(f"question/{count}")
    else:
        return redirect('/thanks')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


    
