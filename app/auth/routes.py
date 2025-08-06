from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.auth.models import User, Role, db
from urllib.parse import urlparse
import logging

@bp.route('/')
def home():
    return render_template('auth/home.html')

@bp.route('/dashboard')
def dashboard_redirect():
    """Redirect authenticated users to their role-specific dashboard, or to home if not authenticated."""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    
    # Import here to avoid circular imports
    from app.helpers import get_user_dashboard_url
    return redirect(get_user_dashboard_url(current_user))

@bp.route('/login', methods=['GET', 'POST'])
@bp.route('/login/<role>', methods=['GET', 'POST'])
def login(role=None):
    logging.info(f"Login request - Method: {request.method}, Role: {role}, Authenticated: {current_user.is_authenticated}")
    if current_user.is_authenticated:
        logging.info("User already authenticated, redirecting to patients index")
        return redirect(url_for('patients.index'))
    
    form = LoginForm()
    logging.info(f"Login form method: {request.method}")
    logging.info(f"Form validate on submit: {form.validate_on_submit()}")
    if form.validate_on_submit():
        logging.info(f"Login attempt for username: {form.username.data}")
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            logging.info("User not found")
            flash('Invalid username or password')
            return redirect(url_for('auth.login', role=role))
        if not user.check_password(form.password.data):
            logging.info("Password check failed")
            flash('Invalid username or password')
            return redirect(url_for('auth.login', role=role))
        
        logging.info("Login successful")
        login_user(user)
        next_page = request.args.get('next')
        logging.info(f"Next page: {next_page}")
        if not next_page or urlparse(next_page).netloc == '':
            # Redirect to role-specific dashboard
            from app.helpers import get_user_dashboard_url
            next_page = get_user_dashboard_url(user)
        logging.info(f"Redirecting to: {next_page}")
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form, role=role)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('patients.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        
        # Assign default role (Receptionist)
        role = Role.query.filter_by(name='Receptionist').first()
        if role:
            user.roles.append(role)
        
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Import the form here to avoid circular imports
    from app.admin.forms import UserForm
    form = UserForm(obj=current_user)
    
    # Remove username and email from form validation since they shouldn't be changed here
    del form.username
    del form.email
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Update user details
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            
            # Only update password if a new one was provided
            if form.password.data:
                current_user.set_password(form.password.data)
            
            db.session.commit()
            flash('Profile updated successfully.', 'success')
            return redirect(url_for('auth.profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'error')
            print(f"Error updating profile: {str(e)}")
    
    # Pre-populate form with current user data for GET requests
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    
    return render_template('auth/profile.html', title='User Profile', form=form)