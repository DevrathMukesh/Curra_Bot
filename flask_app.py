from flask import Flask, request, jsonify
from utils import fetch_conversion_factor

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = float(data['queryResult']['parameters']['unit-currency']['amount'])
    target_currency = data['queryResult']['parameters']['currency-name']
    print(source_currency)
    cf = fetch_conversion_factor(source_currency, target_currency)
    if cf is not None:
        final_amount = amount * cf
        response_text = f"{amount} {source_currency} is {final_amount} {target_currency}"
    else:
        response_text = f"Error: Unable to fetch conversion factor for {source_currency} to {target_currency}"

    response = {'fulfillmentText': response_text}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
