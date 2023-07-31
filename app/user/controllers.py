from flask import current_app, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, login_user, UserMixin
from werkzeug.security import check_password_hash
from app import db, login_manager
from app.models.user import User
import base64
import requests
import hmac

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def serve_login_page(error=None):
    logo = current_app.config['LOGO']
    background_image = current_app.config['BACKGROUND_IMAGE']
    login_design = current_app.config['LOGIN_STYLES']

    page_data = {
        'error': error,
        'logo': logo,
        'background_image': f'background-image: url("{background_image}");',
        'button_background': login_design['button_background'],
        'button_background_hover': login_design['button_background_hover'],
        'card_background': login_design['card_color_background'],
        'card_border': login_design['card_border_color'],
        'login_text': login_design['button_text'],
    }

    return render_template('index.gary', **page_data)

def handle_login_request():
    username = request.form.get('u')
    password = request.form.get('p')

    user_data = find_user_in_config(username)

    if user_data and hmac.compare_digest(password, user_data['password']):
        user = User(username)
        login_user(user)
        return redirect(url_for('admin.admin_route'))

    return serve_login_page("Invalid username or password.")

def find_user_in_config(username):
    users_config = current_app.config['USERS']
    
    for user in users_config:
        if user['username'] == username:
            current_app.config['EMAIL'] = user['email']
            return user

    return None
