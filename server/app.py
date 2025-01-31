from flask import Flask, request, jsonify
from models import db, User, Store, Product, Company, Coupon
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# ------------- Coupon Routes -------------
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

@app.route('/coupons/<int:coupon_id>', methods=['PATCH'])
def update_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    data = request.json

    coupon.code = data.get('code', coupon.code)
    coupon.discount = data.get('discount', coupon.discount)
    if 'expiry' in data:
        try:
            coupon.expiry = datetime.strptime(data['expiry'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid expiry date format. Use YYYY-MM-DD."}), 400
    coupon.description = data.get('description', coupon.description)
    coupon.store_id = data.get('store_id', coupon.store_id)
    db.session.commit()
    return jsonify(coupon.to_dict())

@app.route('/coupons/<int:coupon_id>', methods=['DELETE'])
def delete_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    db.session.delete(coupon)
    db.session.commit()
    return jsonify({"message": "Coupon deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
