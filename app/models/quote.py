from app import db

class Quote(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(120), nullable=False)
    job_description = db.Column(db.String(240), nullable=False)
    quote_amount = db.Column(db.Float, nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_address = db.Column(db.String(120), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    your_email = db.Column(db.String(120), nullable=False)
    your_phone = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(2000), nullable=True) 

    def __repr__(self):
        return '<Quote {}>'.format(self.job_title)

    def serialize(self):
        return {
            'job_title': self.job_title,
            'job_description': self.job_description,
            'quote_amount': self.quote_amount,
            'customer_name': self.customer_name,
            'customer_address': self.customer_address,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'your_email': self.your_email,
            'your_phone': self.your_phone,
            'notes': self.notes
        }
