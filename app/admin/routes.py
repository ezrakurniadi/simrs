from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.admin import bp
from app.admin.forms import RoleForm, UserRoleForm, UserForm
from app.auth.models import Role, User, db
from app.utils import roles_required

@bp.route('/admin', methods=['GET'])
@roles_required('Admin')
def dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/admin/users', methods=['GET'])
@roles_required('Admin')
def list_users():
    users = User.query.all()
    return render_template('admin/users/list.html', users=users)

@bp.route('/admin/users/<id>', methods=['GET'])
@roles_required('Admin')
def view_user(id):
    user = User.query.get_or_404(id)
    return render_template('admin/users/view.html', user=user)

@bp.route('/admin/users/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        # Check if user with this username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        
        if existing_user:
            if existing_user.username == form.username.data:
                flash('A user with this username already exists.', 'error')
            if existing_user.email == form.email.data:
                flash('A user with this email already exists.', 'error')
            return render_template('admin/users/new.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            created_by=current_user.id,
            updated_by=current_user.id
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.', 'success')
        return redirect(url_for('admin.list_users'))
    
    return render_template('admin/users/new.html', form=form)

@bp.route('/admin/users/<id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        # Check if another user with this username or email already exists
        existing_user = User.query.filter(
            ((User.username == form.username.data) & (User.id != id)) |
            ((User.email == form.email.data) & (User.id != id))
        ).first()
        
        if existing_user:
            if existing_user.username == form.username.data:
                flash('A user with this username already exists.', 'error')
            if existing_user.email == form.email.data:
                flash('A user with this email already exists.', 'error')
            return render_template('admin/users/edit.html', form=form, user=user)
        
        # Update user details
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.updated_by = current_user.id
        
        # Only update password if a new one was provided
        if form.password.data:
            user.set_password(form.password.data)
        
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.view_user', id=user.id))
    
    return render_template('admin/users/edit.html', form=form, user=user)

@bp.route('/admin/roles', methods=['GET'])
@roles_required('Admin')
def list_roles():
    roles = Role.query.all()
    return render_template('admin/roles/list.html', roles=roles)

@bp.route('/admin/roles/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_role():
    form = RoleForm()
    if form.validate_on_submit():
        # Check if role with this name already exists
        existing_role = Role.query.filter_by(name=form.name.data).first()
        if existing_role:
            flash('A role with this name already exists.')
            return render_template('admin/roles/new.html', form=form)
        
        role = Role(
            name=form.name.data,
            description=form.description.data,
            created_by=current_user.id,
            updated_by=current_user.id
        )
        
        db.session.add(role)
        db.session.commit()
        flash('Role created successfully.')
        return redirect(url_for('admin.list_roles'))
    
    return render_template('admin/roles/new.html', form=form)

@bp.route('/admin/roles/<id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_role(id):
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    
    if form.validate_on_submit():
        # Check if another role with this name already exists
        existing_role = Role.query.filter(Role.name == form.name.data, Role.id != id).first()
        if existing_role:
            flash('A role with this name already exists.')
            return render_template('admin/roles/edit.html', form=form, role=role)
        
        role.name = form.name.data
        role.description = form.description.data
        role.updated_by = current_user.id
        
        db.session.commit()
        flash('Role updated successfully.')
        return redirect(url_for('admin.list_roles'))
    
    return render_template('admin/roles/edit.html', form=form, role=role)

@bp.route('/admin/roles/<id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_role(id):
    role = Role.query.get_or_404(id)
    
    # Check if role is assigned to any users
    if role.users:
        flash('Cannot delete role because it is assigned to one or more users.')
        return redirect(url_for('admin.list_roles'))
    
    db.session.delete(role)
    db.session.commit()
    flash('Role deleted successfully.')
    return redirect(url_for('admin.list_roles'))

@bp.route('/admin/users/<user_id>/remove-role/<role_id>', methods=['POST'])
@roles_required('Admin')
def remove_role(user_id, role_id):
    user = User.query.get_or_404(user_id)
    role = Role.query.get_or_404(role_id)
    
    # Check if user has this role
    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        flash(f'Role "{role.name}" removed from user "{user.username}" successfully.', 'success')
    else:
        flash(f'User does not have the role "{role.name}".', 'warning')
    
    return redirect(url_for('admin.view_user', id=user.id))

@bp.route('/admin/users/<user_id>/assign-role', methods=['GET', 'POST'])
@roles_required('Admin')
def assign_role(user_id):
    user = User.query.get_or_404(user_id)
    form = UserRoleForm()
    
    # Populate the role choices
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]
    
    if form.validate_on_submit():
        role = Role.query.get(form.role_id.data)
        if role:
            # Check if user already has this role
            if role in user.roles:
                flash(f'User already has the role "{role.name}".', 'warning')
            else:
                user.roles.append(role)
                db.session.commit()
                flash(f'Role "{role.name}" assigned to user "{user.username}" successfully.', 'success')
            return redirect(url_for('admin.view_user', id=user.id))
        else:
            flash('Invalid role selected.', 'error')
    
    return render_template('admin/users/assign_role.html', form=form, user=user)