from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))

    products = db.relationship('Product', backref='lab', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Prepared")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)
