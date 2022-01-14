from flask import Blueprint

enseignant = Blueprint('enseignant',__name__)

from . import views
