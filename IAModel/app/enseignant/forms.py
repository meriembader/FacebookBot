from flask_wtf import FlaskForm

from wtforms import StringField,  SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Question, Test

class QuestionForm(FlaskForm):
    questiontitle = StringField('Questiontitle', validators=[DataRequired()])
    choixrep1 = StringField('Choixrep1', validators=[DataRequired()])
    choixrep2 = StringField('Choixrep2', validators=[DataRequired()])
    choixrep3 = StringField('Choixrep3', validators=[DataRequired()])
    reptrue = StringField('Reptrue', validators=[DataRequired()])
    questionscore =StringField('Questionscore', validators=[DataRequired()])
    submit = SubmitField('Submit')

