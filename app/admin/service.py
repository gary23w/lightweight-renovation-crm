from flask import current_app
from app import db
from app.models.job import Jobs
from app.admin.email.engine import email_builder_factory, EmailSender

def get_jobs_scheduler():
    admins = current_app.config['USERS']
    jobs = Jobs.query.all()
    for admin in admins:
        if admin['admin']:
            builder = email_builder_factory('update')
            email_sender = EmailSender(builder)
            email_sender.send_email(admin['email'], 'update', data=jobs)