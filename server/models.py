from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from datetime import datetime
from config import db  # Import db directly from config.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    discount_value = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Usage(db.Model):
    __tablename__ = 'usages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    used_at = db.Column(db.DateTime, default=datetime.utcnow)  # Extra attribute
    amount_saved = db.Column(db.Float, nullable=True)
