from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app import limiter, get_remote_address
from . import bp
from .controllers import handle_login_request, serve_login_page

@bp.route('/', methods=['GET', 'POST'])
@limiter.limit("50/hour", key_func=get_remote_address)
def home_route():
    if request.method == 'POST':
        return handle_login_request()
    return serve_login_page()


