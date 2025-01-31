from flask import Flask, request, jsonify
from models import db, User, Store, Product, Company, Coupon
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime, date

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# ------------- HOME ROUTE -------------
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"})

# ------------- USER ROUTES -------------
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# ------------- STORE ROUTES -------------
@app.route('/stores', methods=['GET'])
def get_stores():
    stores = Store.query.all()
    return jsonify([store.to_dict() for store in stores])

@app.route('/stores', methods=['POST'])
def add_store():
    data = request.json
    new_store = Store(name=data['name'], location=data['location'])
    db.session.add(new_store)
    db.session.commit()
    return jsonify(new_store.to_dict()), 201

# ------------- PRODUCT ROUTES -------------
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'], store_id=data['store_id'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

# ------------- COMPANY ROUTES -------------
@app.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    return jsonify([company.to_dict() for company in companies])

@app.route('/companies', methods=['POST'])
def add_company():
    data = request.json
    new_company = Company(name=data['name'], industry=data['industry'])
    db.session.add(new_company)
    db.session.commit()
    return jsonify(new_company.to_dict()), 201

# ------------- COUPON ROUTES -------------
@app.route('/coupons', methods=['GET'])
def get_coupons():
    coupons = Coupon.query.all()
    return jsonify([coupon.to_dict() for coupon in coupons])

@app.route('/coupons/<int:coupon_id>', methods=['GET'])
def get_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    return jsonify(coupon.to_dict())

@app.route('/coupons', methods=['POST'])
def add_coupon():
    data = request.json
    try:
        expiry_date = datetime.strptime(data['expiry'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid expiry date format. Use YYYY-MM-DD."}), 400

    new_coupon = Coupon(
        code=data['code'],
        discount=data['discount'],
        expiry=expiry_date,
        description=data.get('description', ''),
        store_id=data['store_id']
    )
    db.session.add(new_coupon)
    db.session.commit()
    return jsonify(new_coupon.to_dict()), 201

@app.route('/coupons/<int:id>', methods=['PUT'])
def update_coupon(id):
    data = request.json
    coupon = Coupon.query.get_or_404(id)

    try:
        coupon.expiry = date.fromisoformat(data.get('expiry', coupon.expiry.isoformat()))
    except ValueError:
        return jsonify({"error": "Invalid expiry date format."}), 400

    coupon.code = data.get('code', coupon.code)
    coupon.discount = data.get('discount', coupon.discount)
    coupon.description = data.get('description', coupon.description)
    coupon.store_id = data.get('store_id', coupon.store_id)

    db.session.commit()
    return jsonify(coupon.to_dict()), 200

@app.route('/coupons/<int:id>', methods=['DELETE'])
def delete_coupon(id):
    coupon = Coupon.query.get_or_404(id)

    db.session.delete(coupon)
    db.session.commit()
    return jsonify({"message": "Coupon deleted successfully"}), 200

# ------------- RUN THE APP -------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
