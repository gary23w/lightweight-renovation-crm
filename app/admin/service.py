from flask import current_app
from app import db
from app.models.job import Jobs
from app.admin.email.engine import send_email

def get_jobs_scheduler():
    admins = current_app.config['USERS']
    jobs = Jobs.query.all()
    for admin in admins:
        if admin['admin']:
            send_email(admin['email'], 'update', data=jobs)