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

    app.config['VERSION'] = config_data['version']
    app.config['NAME'] = config_data['name']
    app.config['SHORT_NAME'] = config_data['short_name']
    app.config['LOGO'] = config_data['logo']
    app.config['BACKGROUND_IMAGE'] = config_data['background_image_login']
    app.config['LOGIN_STYLES'] = config_data['login_design']
    app.config['WEBSITE'] = config_data['website']
    app.config['PWA'] = config_data['enable_pwa']
    app.config['SUPPORT_EMAIL'] = config_data['support_email']
    app.config['INFO_EMAIL'] = config_data['info_email']
    app.config['SUPPORT_PHONE'] = config_data['office_phone']
    app.config['EMAIL_HYPERLINK'] = config_data['email_hyperlink']
    app.config['USERS'] = config_data['users']
    app.config['SIB_API_KEY'] = config_data['sib_api_key']
    app.config['SERVICES'] = config_data['services']
    phone_list = {}
    salesman_options = ""
    leader_board_users = []
    for user in config_data['users']:
        phone_list[user['username']] = user['phone']
        username = user['username'][0].upper() + user['username'][1:]
        salesman_options += "<option value=\"" + username + "\">" + username + "</option>"
        opts = {"username": username, "call_sign": user['call_sign']}
        leader_board_users.append(opts)
    app.config['LEADER_BOARD_USERS'] = leader_board_users
    app.config['PHONE_LIST'] = phone_list
    app.config['SALESMAN_OPTIONS'] = salesman_options

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/')
    return app
