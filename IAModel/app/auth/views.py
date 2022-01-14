from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user


from . import auth
from app.auth.forms import LoginForm , RegistrationForm

from .. import db
from ..models import User 
from app import models

@auth.route('/register', methods=['GET', 'POST'])
def register():
    #handle requests to the /register route 
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    userlevel=form.userlevel.data,
                    password=form.password.data)

        #add employee to the database
        db.session.add(user)
        db.session.commit()
        flash('you have successfully registered! you may now login')
        #redirect to the login page
        return redirect(url_for('auth.login'))
    #load registration template 
    return  render_template('auth/register.html', form=form ,title='Register')

@auth.route('/login',methods= ['GET','POST'])
def login():
    #handle requests to the /login route log an employee in through the login form
    form = LoginForm()
    if form.validate_on_submit():
        #check whether employee exists in the database and whether
        #the password entered matches the password in the database 
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            #log user in
            login_user(user)

            #redirect to the dashboard page after login
            #return redirect(url_for('home.dashboard'))
            if user.is_admin:
                return  redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        #when login details are incorrect 
        else:
            flash('Invalid email or password')
    #load login template auth/login.html
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    #handel requests to the /logout route log an user out through the logout link
    logout_user()
    flash('you have successfully been logged out ')
    #redirect to the login page
    return redirect(url_for('auth.login'))
    