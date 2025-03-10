from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Global balance and auto_pay variables
balance = 250
auto_pay_enabled = True
auto_pay_amount = 500

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # This allows access to columns by name
    return conn

# Home route (renders login page)
@app.route('/')
def home():
    return render_template('index.html')

# Login route (checks username and password from the database)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Connect to the database
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify({'balance': balance, 'auto_pay_enabled': auto_pay_enabled, 'auto_pay_amount': auto_pay_amount})

@app.route('/recharge', methods=['POST'])
def recharge():
    global balance
    data = request.json
    amount = data.get('amount')
    if amount and amount > 0:
        balance += amount
        return jsonify({'message': f'Recharged ₹{amount}', 'new_balance': balance})
    return jsonify({'message': 'Invalid amount'}), 400

@app.route('/deduct', methods=['POST'])
def deduct():
    global balance
    data = request.json
    amount = data.get('amount')
    if amount and amount > 0 and balance >= amount:
        balance -= amount
        check_auto_pay()
        return jsonify({'message': f'Deducted ₹{amount}', 'new_balance': balance})
    return jsonify({'message': 'Insufficient balance or invalid amount'}), 400

def check_auto_pay():
    global balance
    if auto_pay_enabled and balance < 100:
        balance += auto_pay_amount
        return f'Auto-pay activated: Added ₹{auto_pay_amount} to your account. New balance: ₹{balance}'
    return 'No auto-pay triggered.'

@app.route('/toggle-autopay', methods=['POST'])
def toggle_auto_pay():
    global auto_pay_enabled
    data = request.json
    auto_pay_enabled = data.get('enabled', auto_pay_enabled)
    return jsonify({'auto_pay_enabled': auto_pay_enabled})

@app.route('/set-autopay-amount', methods=['POST'])
def set_auto_pay_amount():
    global auto_pay_amount
    data = request.json
    amount = data.get('amount')
    if amount and amount > 0:
        auto_pay_amount = amount
        return jsonify({'message': f'Auto-pay amount set to ₹{amount}'})
    return jsonify({'message': 'Invalid amount'}), 400

if __name__ == '__main__':
    app.run(debug=True)