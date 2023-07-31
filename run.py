import os
from app import create_app
from flask_apscheduler import APScheduler
from app.admin.service import get_jobs_scheduler

scheduler = APScheduler()
app = create_app()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='send_status_update', seconds=43200, misfire_grace_time=900)
def send_status_update():
    with app.app_context():
        get_jobs_scheduler()

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    app.run(host='0.0.0.0', port=port)