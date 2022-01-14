from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from app.admin.forms import DepartmentForm, RoleForm , UserAssignForm
from .. import db

from ..models import Departement , Role, User

def check_admin():
    #prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)
#Departement Views

@admin.route('/departments', methods=['GET','POST'])
@login_required
def list_departments():
    #list all departments
    check_admin()
    departments = Departement.query.all()
    return render_template('admin/departments/departments.html', departments=departments, title="Departments")

@admin.route('/departments/add', methods=['GET','POST'])
@login_required
def add_department():
    #add a departement to the database
    check_admin()
    add_department = True
    
    form=DepartmentForm()
    if form.validate_on_submit():
        department = Departement(name=form.name.data,
                                 description=form.description.data)

        try:
            #add  department to the database
            db.session.add(department)
            db.session.commit()
            flash('you have successfully added a new department.')
        except :
            flash('Error: department name already exists.')
        
        #redirect to departements page 
        return redirect(url_for('admin.list_departments'))
    #load department template
    return render_template('admin/departments/department.html', action="Add", add_department=add_department, form=form, title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_department(id):
    #edit a departement
    check_admin()
    add_department = False
    department= Departement.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name=form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('you have successfully edited the department.')
        
        #redirect to the departments page
        return redirect(url_for('admin.list_departments'))
    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit", 
                            add_department=add_department, form=form,
                            department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_department(id):
    #delete a department from the database
    check_admin()
    department =Departement.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('you have successfully deleted the department.')
    
    #redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title = "Delete department")


#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    #list all roles
    roles = Role.query.all()
    return render_template('admin/roles/roles.html', roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET','POST'])
@login_required
def add_role():
    #add a role to the database
    check_admin()
    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            #add role to database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            flash('Error: role name already exists.')
    
        #redirect to roles page 
        return redirect(url_for('admin.list_roles'))
    # load role template 
    return render_template('admin/roles/role.html', add_role=add_role, form=form ,  title='add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_role(id):
    #edit a role 
    check_admin()
    add_role = False

    role= Role.query.get_or_404(id)
    form= RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.descrioption = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('you have successfully edited the role.')
        #redirect to the roles page 
        return redirect(url_for('admin.list_roles'))
    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role = add_role, form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_role(id):
    #Delete a role from the database
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('you have successfully deleted the role.')

    #redirect to the roles page
    return redirect(url_for('admin.list_roles'))
    
    return render_template(title="Delete Role")       

#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################


@admin.route('/users')
@login_required
def list_users():
    #list all users
    check_admin()
    users = User.query.all()
    return render_template('admin/users/users.html', users=users, title="Users")


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    #assign a departement and role to an user simple 
    check_admin()

    user = User.query.get_or_404(id)
    #prevent admin from being assigned a department or role
    if user.is_admin:
        abort(403)
        
    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.department = form.department.data
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('you have successfully assigned a department and role')

        #redirect to the roles page 
        return redirect(url_for('admin.list_users'))
    return render_template('admin/users/user.html', user=user, form=form,
                            title = 'Assign User')
       