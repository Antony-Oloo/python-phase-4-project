#!/usr/bin/env python3
from flask import Flask, request, jsonify
from models import db, app, Store, Product, Coupon, User, Company, StoreSchema, ProductSchema, CouponSchema, UserSchema, CompanySchema
from flask_cors import CORS

# Enable CORS
CORS(app)

@app.route('/stores', methods=['GET'])
def get_stores():
    stores = Store.query.all()
    store_schema = StoreSchema(many=True)
    return store_schema.jsonify(stores)

@app.route('/store', methods=['POST'])
def add_store():
    name = request.json.get('name')
    location = request.json.get('location')

    new_store = Store(name=name, location=location)
    db.session.add(new_store)
    db.session.commit()

    store_schema = StoreSchema()
    return store_schema.jsonify(new_store), 201

@app.route('/store/<int:id>', methods=['PATCH'])
def update_store(id):
    store = Store.query.get_or_404(id)

    store.name = request.json.get('name', store.name)
    store.location = request.json.get('location', store.location)

    db.session.commit()

    store_schema = StoreSchema()
    return store_schema.jsonify(store)

@app.route('/store/<int:id>', methods=['DELETE'])
def delete_store(id):
    store = Store.query.get_or_404(id)

    db.session.delete(store)
    db.session.commit()

    return '', 204

# Product routes
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    return product_schema.jsonify(products)

@app.route('/product', methods=['POST'])
def add_product():
    name = request.json.get('name')
    price = request.json.get('price')
    store_id = request.json.get('store_id')

    new_product = Product(name=name, price=price, store_id=store_id)
    db.session.add(new_product)
    db.session.commit()

    product_schema = ProductSchema()
    return product_schema.jsonify(new_product), 201

@app.route('/product/<int:id>', methods=['PATCH'])
def update_product(id):
    product = Product.query.get_or_404(id)

    product.name = request.json.get('name', product.name)
    product.price = request.json.get('price', product.price)
    product.store_id = request.json.get('store_id', product.store_id)

    db.session.commit()

    product_schema = ProductSchema()
    return product_schema.jsonify(product)

@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return '', 204

# Coupon routes
@app.route('/coupons', methods=['GET'])
def get_coupons():
    coupons = Coupon.query.all()
    coupon_schema = CouponSchema(many=True)
    return coupon_schema.jsonify(coupons)

@app.route('/coupon', methods=['POST'])
def add_coupon():
    code = request.json.get('code')
    discount = request.json.get('discount')

    new_coupon = Coupon(code=code, discount=discount)
    db.session.add(new_coupon)
    db.session.commit()

    coupon_schema = CouponSchema()
    return coupon_schema.jsonify(new_coupon), 201

@app.route('/coupon/<int:id>', methods=['PATCH'])
def update_coupon(id):
    coupon = Coupon.query.get_or_404(id)

    coupon.code = request.json.get('code', coupon.code)
    coupon.discount = request.json.get('discount', coupon.discount)

    db.session.commit()

    coupon_schema = CouponSchema()
    return coupon_schema.jsonify(coupon)

@app.route('/coupon/<int:id>', methods=['DELETE'])
def delete_coupon(id):
    coupon = Coupon.query.get_or_404(id)

    db.session.delete(coupon)
    db.session.commit()

    return '', 204

# User routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.jsonify(users)

@app.route('/user', methods=['POST'])
def add_user():
    name = request.json.get('name')
    email = request.json.get('email')

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    user_schema = UserSchema()
    return user_schema.jsonify(new_user), 201

@app.route('/user/<int:id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get_or_404(id)

    user.name = request.json.get('name', user.name)
    user.email = request.json.get('email', user.email)

    db.session.commit()

    user_schema = UserSchema()
    return user_schema.jsonify(user)

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return '', 204

# Company routes
@app.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    company_schema = CompanySchema(many=True)
    return company_schema.jsonify(companies)

@app.route('/company', methods=['POST'])
def add_company():
    name = request.json.get('name')
    location = request.json.get('location')

    new_company = Company(name=name, location=location)
    db.session.add(new_company)
    db.session.commit()

    company_schema = CompanySchema()
    return company_schema.jsonify(new_company), 201

@app.route('/company/<int:id>', methods=['PATCH'])
def update_company(id):
    company = Company.query.get_or_404(id)

    company.name = request.json.get('name', company.name)
    company.location = request.json.get('location', company.location)

    db.session.commit()

    company_schema = CompanySchema()
    return company_schema.jsonify(company)

@app.route('/company/<int:id>', methods=['DELETE'])
def delete_company(id):
    company = Company.query.get_or_404(id)

    db.session.delete(company)
    db.session.commit()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
