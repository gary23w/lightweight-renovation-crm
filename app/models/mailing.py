from app import db

class Mailing(db.Model):
    __tablename__ = 'mailing'

    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)


    def __repr__(self):
        return '<Mailing {}>'.format(self.name)

    def serialize(self):
        return {
            'customer': self.customer,
            'email': self.email,
        }
