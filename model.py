from __init__ import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
 
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    incident = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    latitude = db.Column(db.String(10), nullable=False)
    longitude = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable = True)
    
    def __repr__(self):
        return f"Report('{self.address}', '{self.incident}','{self.date}', '{self.description}', '{self.latitude}', '{self.longitude}', '{self.username}')"
    

#db.drop_all()
db.create_all()