from datetime import timezone
from enum import unique
from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


users_tests = db.Table('users_tests_result', 
              db.Column('uid',db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True),
              db.Column('tid',db.Integer, db.ForeignKey('tests.id'), nullable=False,  primary_key=True),
              db.Column('uscore', db.Integer),
              db.Column('usertestdate',db.DateTime(timezone=True),server_default=db.func.now()),
            )

class User(UserMixin, db.Model):
    #creation de tab user
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique= True)
    first_name = db.Column(db.String(60),index=True)
    last_name = db.Column(db.String(60),index=True)
    userlevel = db.Column(db.String(60),index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer,db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    is_admin =db.Column(db.Boolean, default=False)
    informations=db.relationship('Information', backref='user', lazy='dynamic')
    entretiens=db.relationship('Entretien', backref='user', lazy='dynamic')
    tests = db.relationship('Test', 
                            secondary = users_tests,
                            back_populates="users")
    @property
    def password(self):
        # password secured
        raise AttributeError('password is not readable attribute.')

    @password.setter
    def password(self, password):
        #set password to hashed password
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        #check if hashed password matches actual password
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

#set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
##############################################################################

class Departement(db.Model):
    #creation du tab department
    __tablename__='departments'
    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60),unique=True)
    description = db.Column(db.String(200))
    users= db.relationship('User',backref='department', lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

##############################################################################

class Role(db.Model):
    #creation du tab role
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description =  db.Column(db.String(200))
    users=db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role: {}>'.format(self.name)
###############################################################################

class Information(db.Model):
    #creation du table information
    __tablename__='informations' 
    id = db.Column(db.Integer, primary_key=True)
    inf_q = db.Column(db.String(300))
    inf_rep = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __repr__(self):
        return '<Information: {}>'.format(self.inf_q)

###############################################################################

class Test(db.Model):
    #creation du table test
    __tablename__='tests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200)) 
    description = db.Column(db.String(200))
    questions = db.relationship('Question',backref='test', lazy='dynamic')
    users = db.relationship('User', 
                            secondary = users_tests,
                            back_populates="tests")
    def __repr__(self):
        return '<Test :{}>'.format(self.title)

##############################################################################

class Question(db.Model):
    #creation du table question 
    __tablename__='questions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    questiontitle = db.Column(db.String(300))
    choixrep1 = db.Column(db.String(300))
    choixrep2 = db.Column(db.String(300))
    choixrep3 = db.Column(db.String(300))
    reptrue = db.Column(db.String(300))
    questionscore = db.Column(db.Integer)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
   
    def __repr__(self):
        return '<Question :{}>'.format(self.questiontitle)

##############################################################################
class Entretien(db.Model):
    #creation du table question 
    __tablename__='entretiens'
    id = db.Column(db.Integer, primary_key=True)
    entretientitle = db.Column(db.String(300))
    entretiendate = db.Column(db.DateTime())
    resultat= db.Column(db.String(300))
    questionscore = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
   
    def __repr__(self):
        return '<Entretien :{}>'.format(self.entretientitle)

###############################################################################


###############################################################################

