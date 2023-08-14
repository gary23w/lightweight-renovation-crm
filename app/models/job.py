from app import db

class Jobs(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    contract_number = db.Column(db.String(64), nullable=False)
    salesman = db.Column(db.String(64), nullable=False)
    customer = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(240), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    selling_price = db.Column(db.String(120), nullable=False)
    cost = db.Column(db.String(120), nullable=False)
    installer = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.String(240), nullable=False)

    def __repr__(self):
        return '<Jobs {}>'.format(self.customer)

    def serialize(self):
        return {
            'contract_number': self.contract_number,
            'salesman': self.salesman,
            'customer': self.customer,
            'address': self.address,
            'city': self.city,
            'phone': self.phone,
            'description': self.description,
            'date': self.date,
            'email': self.email,
            'selling_price': self.selling_price,
            'cost': self.cost,
            'installer': self.installer,
            'status': self.status,
            'notes': self.notes
        }
