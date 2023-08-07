from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_executor import Executor
import json
import os

db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(default_limits=["50 per hour"], key_func=get_remote_address)
executor = Executor()

keys_mapping = {
    'VERSION': 'version',
    'NAME': 'name',
    'SHORT_NAME': 'short_name',
    'LOGO': 'logo',
    'BACKGROUND_IMAGE': 'background_image_login',
    'LOGIN_STYLES': 'login_design',
    'WEBSITE': 'website',
    'PWA': 'enable_pwa',
    'SUPPORT_EMAIL': 'support_email',
    'INFO_EMAIL': 'info_email',
    'SUPPORT_PHONE': 'office_phone',
    'EMAIL_HYPERLINK': 'email_hyperlink',
    'USERS': 'users',
    'SIB_API_KEY': 'sib_api_key',
    'SERVICES': 'services',
}

def load_config(config_path):
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as config_file:
                config_data = json.load(config_file)
                return config_data
        except json.JSONDecodeError:
            print(f"Error: Config file '{config_path}' is not a valid JSON file.")
        except Exception as e:
            print(f"An error occurred while opening the config file: {e}")
    else:
        print(f"Error: Config file '{config_path}' does not exist.")
    return None

config_data = load_config('app/config.json')

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='tpl', static_folder='static')
    app.config.from_object(config_class)    
    CORS(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.home_route'
    db.init_app(app)
    limiter.init_app(app)
    executor.init_app(app)

    for app_key, config_key in keys_mapping.items():
        app.config[app_key] = config_data[config_key]

    phone_list = {}
    salesman_options = []
    leader_board_users = []
    for user in config_data['users']:
        phone_list[user['username']] = user['phone']
        username = user['username'][0].upper() + user['username'][1:]
        salesman_options.append(f'<option value="{username}">{username}</option>')
        leader_board_users.append({"username": username, "call_sign": user['call_sign']})

    app.config['LEADER_BOARD_USERS'] = leader_board_users
    app.config['PHONE_LIST'] = phone_list
    app.config['SALESMAN_OPTIONS'] = "".join(salesman_options)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/')
    return app
