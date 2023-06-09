from forms import UserLoginForm, UserSignInForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            # username = form.username.data
            email = form.email.data
            password = form.password.data
            # print(email, password)

            user = User(email= email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('signup.html', form=form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserSignInForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print("Form email:", email)
            print("Form password", password)

            logged_user = User.query.filter(User.email == email).first()
            # if logged_user:
            #     print("User found in database")
            #     print("User email:", logged_user.email)
            #     print("User hashed password:", logged_user.password)
            # else: 
            #     print("USer not found in database")

            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successful', 'auth-sucess')
                return redirect(url_for('site.profile'))
            else:
                flash('You have failed in your attempt to access this content.', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('signin.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))