from flask import Flask, request, jsonify

app = Flask(__name__)

fake_financials = {
    "1": { 
        "account_balance": 5000.0,
        "transactions": [
            {"date": "2024-01-01", "description": "Purchase", "amount": -100.0},
            {"date": "2024-02-01", "description": "Deposit", "amount": 500.0},
            {"date": "2024-03-01", "description": "Withdrawal", "amount": -50.0},
        ]
    }
}

@app.route('/api/financials', methods=['GET'])
def get_financials():
    bank_number = request.args.get('bank_number')

    if bank_number is None:
        return jsonify({"error": "Bank number is required"}), 400

    user_data = fake_financials.get(bank_number)

    if user_data is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user_data)

if __name__ == '__main__':
    app.run(debug=True)
