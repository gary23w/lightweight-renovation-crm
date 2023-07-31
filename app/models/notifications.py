from app import db

class Notifications(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(240), nullable=False)
    notification = db.Column(db.String(240), nullable=False)

    def __repr__(self):
        return '<Notifications {}>'.format(self.user)

    def serialize(self):
        return {
            'user': self.user,
            'title': self.title,
            'notification': self.notification,
        }
