from flask import Flask, jsonify, request
from flask_cors import CORS
from DatabaseWrapper import DatabaseWrapper

app = Flask(__name__)
CORS(app)

db = DatabaseWrapper()

# --- ROTTE PER IL MENU (Client & Staff) ---
@app.route('/menu', methods=['GET'])
def get_menu():
    products = db.get_products()
    categories = db.get_categories()
    return jsonify({"products": products, "categories": categories})

# --- ROTTE PER GLI ORDINI (Client) ---
@app.route('/orders', methods=['POST'])
def place_order():
    data = request.json # { "table": "5", "user": "Daniele", "items": [{"id": 1, "qty": 2}, ...] }
    order_id = db.add_order(data['table'], data['user'])
    
    for item in data['items']:
        db.add_order_item(order_id, item['id'], item['qty'])
        
    return jsonify({"message": "Ordine inviato!", "order_id": order_id}), 201

# --- ROTTE PER LO STAFF ---
@app.route('/staff/orders', methods=['GET'])
def get_staff_orders():
    orders = db.get_orders_staff()
    return jsonify(orders)

@app.route('/staff/orders/<int:order_id>/status', methods=['PUT'])
def update_status(order_id):
    new_status = request.json.get('status')
    db.update_order_status(order_id, new_status)
    return jsonify({"message": "Stato aggiornato"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
