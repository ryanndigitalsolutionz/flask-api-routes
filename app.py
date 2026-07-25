from flask import Flask, jsonify, request
from ext import fetch_external_product

app = Flask(__name__)

inventory = [
    {"id": 1, "name": "Almond Milk", "price": 5.79, "stock": 75},
    {"id": 2, "name": "Dark Chocolate", "price": 4.19, "stock": 50}
]


@app.route("/", methods=["GET"])
def home():
    """Health check / API status endpoint."""
    return jsonify({
        "status": "online",
        "message": "Welcome to the Inventory System API"
    }), 200


@app.route("/inventory/summary", methods=["GET"])
def get_inventory_summary():
    """Helper route to calculate total stocks."""
    total_items = len(inventory)
    total_quantity = sum(item["quantity"] for item in inventory)
    total_value = sum(item["price"] * item["quantity"] for item in inventory)
    
    return jsonify({
        "total_unique_items": total_items,
        "total_stock_count": total_quantity,
        "total_inventory_value": round(total_value, 2)
    }), 200


@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_single_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": f"Item with ID {item_id} not found"}), 404
    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json() or {}
    
    new_item = {
        "id": len(inventory) + 1,
        "name": data.get("name"),
        "price": float(data.get("price", 0.0)),
        "stock": int(data.get("stock", 0))
    }
    
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": f"Item with ID {item_id} not found"}), 404

    data = request.get_json() or {}

    # Update only fields provided in payload
    if "name" in data:
        item["name"] = data["name"]
    if "barcode" in data:
        item["barcode"] = data["barcode"]
    if "price" in data:
        item["price"] = float(data["price"])
    if "quantity" in data:
        item["quantity"] = int(data["quantity"])
    if "category" in data:
        item["category"] = data["category"]

    return jsonify(item), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global inventory
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": f"Item with ID {item_id} not found"}), 404

    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": f"Item {item_id} successfully deleted"}), 200


@app.route("/inventory/fetch-external/<identifier>", methods=["POST"])
def add_from_external(identifier):
    product_data = fetch_external_product(identifier)
    if not product_data:
        return jsonify({"error": "Product not found on external API"}), 404
    
    product_data["id"] = len(inventory) + 1
    inventory.append(product_data)
    return jsonify(product_data), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)

