#!/usr/bin/env python3

# Remote library imports
from flask import request, jsonify
from flask_restful import Resource
from config import app, db, api
from models import User, Store, Coupon, Usage
from datetime import datetime

# Index route
@app.route('/')
def index():
    return '<h1>Coupon App Backend</h1>'

# USER RESOURCE
class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])

    def post(self):
        data = request.get_json()
        name, email, password = data.get("name"), data.get("email"), data.get("password")

        if not all([name, email, password]):
            return {"error": "All fields are required!"}, 400

        if User.query.filter_by(email=email).first():
            return {"error": "Email already exists!"}, 400

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully!"}, 201

    def delete(self):
        data = request.get_json()
        user_id = data.get("id")
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found!"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully!"}, 200

api.add_resource(UserResource, '/users')

# STORE RESOURCE
class StoreResource(Resource):
    def get(self):
        stores = Store.query.all()
        return jsonify([{"id": store.id, "name": store.name, "location": store.location} for store in stores])

    def post(self):
        data = request.get_json()
        name, location = data.get("name"), data.get("location")

        if not name:
            return {"error": "Store name is required!"}, 400

        new_store = Store(name=name, location=location)
        db.session.add(new_store)
        db.session.commit()
        return {"message": "Store created successfully!"}, 201

    def delete(self):
        data = request.get_json()
        store_id = data.get("id")
        store = Store.query.get(store_id)

        if not store:
            return {"error": "Store not found!"}, 404

        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted successfully!"}, 200

api.add_resource(StoreResource, '/stores')

# COUPON RESOURCE
class CouponResource(Resource):
    def get(self):
        coupons = Coupon.query.all()
        return jsonify([
            {
                "id": coupon.id,
                "code": coupon.code,
                "discount_value": coupon.discount_value,
                "expiry_date": coupon.expiry_date.strftime('%Y-%m-%d'),
                "store_id": coupon.store_id
            }
            for coupon in coupons
        ])

    def post(self):
        data = request.get_json()
        code, discount_value, expiry_date, store_id = (
            data.get("code"),
            data.get("discount_value"),
            data.get("expiry_date"),
            data.get("store_id"),
        )

        if not all([code, discount_value, expiry_date, store_id]):
            return {"error": "All fields are required!"}, 400

        new_coupon = Coupon(
            code=code,
            discount_value=discount_value,
            expiry_date=datetime.strptime(expiry_date, "%Y-%m-%d"),
            store_id=store_id
        )
        db.session.add(new_coupon)
        db.session.commit()
        return {"message": "Coupon created successfully!"}, 201

    def delete(self):
        data = request.get_json()
        coupon_id = data.get("id")
        coupon = Coupon.query.get(coupon_id)

        if not coupon:
            return {"error": "Coupon not found!"}, 404

        db.session.delete(coupon)
        db.session.commit()
        return {"message": "Coupon deleted successfully!"}, 200

api.add_resource(CouponResource, '/coupons')

# USAGE RESOURCE
class UsageResource(Resource):
    def get(self):
        usages = Usage.query.all()
        return jsonify([
            {
                "id": usage.id,
                "user_id": usage.user_id,
                "coupon_id": usage.coupon_id,
                "used_at": usage.used_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for usage in usages
        ])

    def post(self):
        data = request.get_json()
        user_id, coupon_id = data.get("user_id"), data.get("coupon_id")

        if not all([user_id, coupon_id]):
            return {"error": "Both user_id and coupon_id are required!"}, 400

        new_usage = Usage(user_id=user_id, coupon_id=coupon_id)
        db.session.add(new_usage)
        db.session.commit()
        return {"message": "Coupon usage recorded successfully!"}, 201

api.add_resource(UsageResource, '/usage')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

