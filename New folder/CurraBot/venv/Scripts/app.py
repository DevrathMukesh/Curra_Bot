from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = float(data['queryResult']['parameters']['unit-currency']['amount'])
    target_currencies = data['queryResult']['parameters']['currency-name']
    print(target_currencies)

    response_text = ""
    for target_currency in target_currencies:
        cf = fetch_conversion_factor(source_currency, target_currency)
        if cf is not None:
            final_amount = amount * cf
            response_text += "{} {} is {} {}\n".format(amount, source_currency, final_amount, target_currency)
        else:
            response_text += f"Error: Unable to fetch conversion factor for {source_currency} to {target_currency}\n"

    response = {'fulfillmentText': response_text}
    return jsonify(response)


def fetch_conversion_factor(source, target):
    url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest"
    querystring = {"from": source, "to": target}
    headers = {
        "X-RapidAPI-Key": "e485732eefmsh37b836e2e48ec37p10a6b4jsn641e582e0d80",
        "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        if 'rates' in data:
            return data['rates'][target]
    return None


if __name__ == "__main__":
    app.run(debug=True)
