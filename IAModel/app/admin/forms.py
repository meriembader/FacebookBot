from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired


from ..models import Departement , Role

class DepartmentForm(FlaskForm):
    # form for admin to add or edit a departement
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    #form for admin to add or edit a role
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserAssignForm(FlaskForm):
    #form for admin to assign departments and roles to employees
    department = QuerySelectField(query_factory=lambda: Departement.query.all(), get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name")
    submit = SubmitField('Submit')
