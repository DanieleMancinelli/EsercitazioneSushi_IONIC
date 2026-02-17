from flask import Flask, jsonify, request
from flask_cors import CORS
from DatabaseWrapper import DatabaseWrapper

app = Flask(__name__)
CORS(app)

db = DatabaseWrapper()

@app.route('/menu', methods=['GET'])
def get_menu():
    try:
        products = db.get_all_products()
        categories = db.get_all_categories()
        return jsonify({"products": products, "categories": categories})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders', methods=['POST'])
def place_order():
    try:
        data = request.json
        order_id = db.add_order(data['table'], data['user'])
        for item in data['items']:
            db.add_order_item(order_id, item['id'], item['qty'])
        return jsonify({"message": "Ordine inviato!", "order_id": order_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/status', methods=['GET'])
def get_order_status():
    try:
        table = request.args.get('table')
        user = request.args.get('user')
        orders = db.fetch_query("SELECT id, status, created_at FROM orders WHERE table_number = %s AND user_name = %s ORDER BY created_at DESC", (table, user))
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/staff/orders', methods=['GET'])
def get_staff_orders():
    return jsonify(db.get_orders_staff())

@app.route('/staff/orders/<int:order_id>/status', methods=['PUT'])
def update_status(order_id):
    new_status = request.json.get('status')
    db.update_order_status(order_id, new_status)
    return jsonify({"message": "OK"})

@app.route('/staff/products', methods=['POST'])
def add_product():
    d = request.json
    db.add_product(d['name'], d['image_url'], d['price'], d['category_id'])
    return jsonify({"msg": "ok"})

@app.route('/staff/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    d = request.json
    db.update_product(pid, d['name'], d['image_url'], d['price'], d['category_id'])
    return jsonify({"msg": "ok"})

@app.route('/staff/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    db.delete_product(pid)
    return jsonify({"msg": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)