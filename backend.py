from flask import Flask, jsonify, request
import csv
import os
from flask_cors import CORS
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler
import logging


app = Flask(_name_)
CORS(app)

def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get request details
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        method = request.method
        path = request.path
        ip = request.remote_addr

        # For POST requests, get the body
        body = None
        if method == 'POST':
            body = request.get_json()

        # Create log entry
        log_entry = f"[{timestamp}] {method} {path} from {ip}"
        if body:
            log_entry += f" | Data: {body}"

        # Log to file
        with open('log.txt', 'a') as log_file:
            log_file.write(log_entry + '\n')

        # Execute the actual function
        response = f(*args, **kwargs)

        # Log the response
        status_code = response[1] if isinstance(response, tuple) else 200
        log_entry = f"[{timestamp}] Response: Status {status_code}"
        with open('log.txt', 'a') as log_file:
            log_file.write(log_entry + '\n\n')

        return response
    return decorated_function

class LiveLogger:
    @staticmethod
    def log_transaction(action, details):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action}: {details}\n"

        # Write to log file
        with open('log.txt', 'a') as log_file:
            log_file.write(log_entry)

        # You could also implement real-time notifications here
        # For example, using websockets or other real-time protocols
        print(log_entry.strip())  # Print to console for immediate feedback

def read_csv():
    with open('products.csv', 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(products):
    fieldnames = ['id', 'name', 'price', 'quantity']
    with open('products.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

@app.route('/products', methods=['GET'])
@log_request
def get_products():
    products = read_csv()
    LiveLogger.log_transaction(
        "Product Request",
        f"Retrieved {len(products)} products"
    )
    return jsonify(products)

@app.route('/purchase', methods=['POST'])
@log_request
def update_quantities():
    cart_items = request.json
    products = read_csv()

    # Log initial purchase attempt
    LiveLogger.log_transaction(
        "Purchase Attempt",
        f"Cart items: {cart_items}"
    )

    # Track changes for logging
    changes = []

    # Update quantities
    for product in products:
        product_id = product['id']
        if product_id in cart_items:
            old_quantity = int(product['quantity'])
            new_quantity = old_quantity - cart_items[product_id]

            if new_quantity < 0:
                error_msg = f"Insufficient quantity for product {product_id}"
                LiveLogger.log_transaction("Purchase Error", error_msg)
                return jsonify({'error': error_msg}), 400

            product['quantity'] = str(new_quantity)
            changes.append({
                'product_id': product_id,
                'old_quantity': old_quantity,
                'new_quantity': new_quantity
            })

    # Write updated quantities back to CSV
    write_csv(products)

    # Log successful purchase
    LiveLogger.log_transaction(
        "Purchase Successful",
        f"Changes: {changes}"
    )

    return jsonify({'message': 'Purchase successful', 'changes': changes})

@app.before_request
def setup_logging():
    # Create or clear the log file when the server starts
    with open('log.txt', 'w') as log_file:
        log_file.write(f"=== Server Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")

# Optional: Add error logging
@app.errorhandler(Exception)
def handle_error(error):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_entry = f"[{timestamp}] ERROR: {str(error)}\n"

    with open('log.txt', 'a') as log_file:
        log_file.write(error_entry)

    return jsonify({'error': str(error)}), 500

if _name_ == '_main_':
    # Create logs directory if it doesn't exist
    if not os.path.exists('log.txt'):
        open('log.txt', 'w').close()
    handler = RotatingFileHandler('log.txt', maxBytes=100000, backupCount=3)
    app.logger.addHandler(handler)
    app.run(debug=True)
