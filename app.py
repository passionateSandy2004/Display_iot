from flask import Flask, jsonify, request
from flask_cors import CORS  # Add CORS support
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initial dummy data
data = {
    "total_value": "$12,350.00",
    "cash_balance": "$1,200.00",
    "unrealized_pl": "+$450.00",
    "symbols": ["AAPL", "TSLA", "GOOGL"],
    "pl": ["+$25.00", "-$30.00", "+$50.00"],
    "total_values": ["$1,502.50", "$3,625.50", "$4,901.00"],
    "quantities": ["10", "5", "2"],
    "prices": ["150.25", "725.10", "2,450.50"]
}

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    # Format the data as expected by the Arduino code
    portfolio = {
        "total_value": data["total_value"],
        "cash_balance": data["cash_balance"],
        "unrealized_pl": data["unrealized_pl"],
        "positions": []
    }
    
    # Create position objects
    for i in range(len(data["symbols"])):
        position = {
            "symbol": data["symbols"][i],
            "quantity": data["quantities"][i],
            "price": f"${data['prices'][i]}",
            "pl": data["pl"][i],
            "total_value": data["total_values"][i]
        }
        portfolio["positions"].append(position)
    
    return jsonify(portfolio)

@app.route('/total_value', methods=['GET', 'POST'])
def total_value():
    if request.method == 'POST':
        data['total_value'] = request.json.get('value', data['total_value'])
    return jsonify({'total_value': data['total_value']})

@app.route('/cash_balance', methods=['GET', 'POST'])
def cash_balance():
    if request.method == 'POST':
        data['cash_balance'] = request.json.get('value', data['cash_balance'])
    return jsonify({'cash_balance': data['cash_balance']})

@app.route('/unrealized_pl', methods=['GET', 'POST'])
def unrealized_pl():
    if request.method == 'POST':
        data['unrealized_pl'] = request.json.get('value', data['unrealized_pl'])
    return jsonify({'unrealized_pl': data['unrealized_pl']})

@app.route('/symbols', methods=['GET', 'POST'])
def symbols():
    if request.method == 'POST':
        data['symbols'] = request.json.get('value', data['symbols'])
    return jsonify({'symbols': data['symbols']})

@app.route('/pl', methods=['GET', 'POST'])
def pl():
    if request.method == 'POST':
        data['pl'] = request.json.get('value', data['pl'])
    return jsonify({'pl': data['pl']})

@app.route('/total_values', methods=['GET', 'POST'])
def total_values():
    if request.method == 'POST':
        data['total_values'] = request.json.get('value', data['total_values'])
    return jsonify({'total_values': data['total_values']})

@app.route('/quantities', methods=['GET', 'POST'])
def quantities():
    if request.method == 'POST':
        data['quantities'] = request.json.get('value', data['quantities'])
    return jsonify({'quantities': data['quantities']})

@app.route('/prices', methods=['GET', 'POST'])
def prices():
    if request.method == 'POST':
        data['prices'] = request.json.get('value', data['prices'])
    return jsonify({'prices': data['prices']})

# Create ASGI application
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(asgi_app, host="0.0.0.0", port=5000)
