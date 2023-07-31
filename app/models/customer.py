from app import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    contract_number = db.Column(db.String(64), nullable=False)
    salesman = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(240), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Customer {}>'.format(self.name)

    def serialize(self):
        return {
            'contract_number': self.contract_number,
            'salesman': self.salesman,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'phone': self.phone,
            'description': self.description,
            'date': self.date,
            'email': self.email
        }
