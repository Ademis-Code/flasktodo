from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import UserMixin, login_user, logout_user
from webapp.forms.auth_form import LoginForm
from webapp import app, login_manager, limiter
from flask_limiter.util import get_remote_address


USER = {
    'username': 'admin',
    'password': 'admin1234'
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username == USER['username']:
        return User(username)
    return None


def key_by_ip_user():
    user = request.form.get('username') or 'anon'
    return f"{get_remote_address()}:{user}"


@limiter.limit("10 per 10 minutes", key_func=key_by_ip_user)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == USER['username'] and password == USER['password']:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Please check your email or password', 'danger')
            return render_template('auth_templates/login.html', form=form, error="Invalid username or password")
    return render_template('auth_templates/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))