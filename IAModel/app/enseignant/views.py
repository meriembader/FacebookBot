from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.admin.forms import DepartmentForm

from . import enseignant
from app.enseignant.forms import QuestionForm
from .. import db

from ..models import Question

def check_enseignant():
    #prevent non-enseignant from accessing the page
    if not current_user.role.name == "Enseignant":
        abort(403)

@enseignant.route('/questions', methods = ['GET', 'POST'])
@login_required
def list_questions():
    #list all questions
    check_enseignant()
    questions= Question.query.all()
    return render_template('enseignant/questions/questions.html', questions=questions, title="Questions")

@enseignant.route('/questions/add',methods=['GET','POST'])
@login_required
def add_question():
    #add a question to the database
    check_enseignant()
    add_question= True

    form=QuestionForm()

    if form.validate_on_submit():
        question= Question(questiontitle=form.questiontitle.data,
                            choixrep1=form.choixrep1.data,
                            choixrep2=form.choixrep2.data,
                            choixrep3=form.choixrep3.data,
                            reptrue=form.reptrue.data,
                            questionscore=form.questionscore.data)
        try:
            db.session.add(question)
            db.session.commit()
            flash('you have successfully added a new questions')
        except :
            flash('Erroe: question name already exists.')

        #redirect to question page 
        return redirect(url_for('enseignant.list_questions'))
    #load question template
    return render_template('enseignant/questions/question.html', action="Add", add_question=add_question, form=form, title="Add Question")

@enseignant.route('/questions/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_question(id):
    #edit a question
    check_enseignant()
    add_question=True
    question= Question.query.get_or_404(id)
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        question.questiontitle=form.questiontitle.data
        question.choixrep1= form.choixrep1.data
        question.choixrep2= form.choixrep2.data
        question.choixrep3= form.choixrep3.data
        question.reptrue= form.reptrue.data
        question.questionscore = form.questionscore.data
 
        db.session.commit()
        flash('you hava successfully edited the question.')

        #redirect to the question page 
        return redirect(url_for('enseignant.list_questions'))
    form.questionscore.data =question.questionscore
    form.reptrue.data = question.reptrue
    form.choixrep3.data = question.choixrep3
    form.choixrep2.data = question.choixrep2
    form.choixrep1.data = question.choixrep1
    form.questiontitle.data = question.questiontitle

    return render_template ('enseignant/questions/question.html', action="Edit",
                            add_question=add_question, form=form,
                            question=question, title="Edit Question")

@enseignant.route('/questions/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_question(id):
    #delete a departement from the database
    check_enseignant()
    question= Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    flash('you have successfully deleted the questions')

    #redirect to the departments page 
    return redirect(url_for('enseignant.list_questions'))