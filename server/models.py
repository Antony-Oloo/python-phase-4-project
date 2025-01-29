from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'  # Or your DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Association table for many-to-many relationship between User and Coupon
user_coupon = db.Table('user_coupon',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('coupon_id', db.Integer, db.ForeignKey('coupon.id'), primary_key=True),
    db.Column('date_issued', db.DateTime, default=datetime.utcnow)
)

# Model for Store
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    products = db.relationship('Product', backref='store', lazy=True)

    def __repr__(self):
        return f'<Store {self.name}>'

# Model for Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

# Model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    coupons = db.relationship('Coupon', secondary=user_coupon, backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<User {self.name}>'

# Model for Coupon
class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    discount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Coupon {self.code}>'

# Model for Company
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Company {self.name}>'

# Schemas for serialization
class StoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Store

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class CouponSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Coupon

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class CompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Company
