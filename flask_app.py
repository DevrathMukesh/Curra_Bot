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
    print(target_currency)
    print(amount)

    response_text = ""
    cf = fetch_conversion_factor(source_currency, target_currency)
    print(cf)
    if cf is not None:
        final_amount = amount * cf
        response_text += "{} {} is {} {}\n".format(amount, source_currency, final_amount, target_currency)
    else:
        response_text += f"Error: Unable to fetch conversion factor for {source_currency} to {target_currency}\n"

    response = {'fulfillmentText': response_text}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
