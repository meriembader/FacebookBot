import flask
from flask.scaffold import F


from flask import Blueprint

auth = Blueprint('auth',__name__)
 
from . import views
