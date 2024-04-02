from flask import Flask, request, jsonify
import requests
from werkzeug.local import LocalProxy, LocalStack

app = Flask(__name__)
local_session_stack = LocalStack()
session = LocalProxy(lambda: local_session_stack.top)

@app.before_request
def before_request():
    local_session_stack.push(requests.Session())

@app.after_request
def after_request(response):
    local_session_stack.pop()
    return response

@app.route('/', methods=['POST'])
def index():
    try:
        # Extract data from request
        data = request.get_json()
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = float(data['queryResult']['parameters']['unit-currency']['amount'])
        target_currencies = data['queryResult']['parameters']['currency-name']

        # Initialize response text
        response_text = ""

        for target_currency in target_currencies:
            # Attempt to fetch conversion factor
            cf = fetch_conversion_factor(source_currency, target_currency)
            if cf is not None:
                final_amount = amount * cf
                response_text += "{} {} is {} {}\n".format(amount, source_currency, final_amount, target_currency)
            else:
                response_text += f"Error: Unable to fetch conversion factor for {source_currency} to {target_currency}\n"

        # Create and return JSON response
        response = {'fulfillmentText': response_text}
        return jsonify(response)

    except (KeyError, ValueError) as e:
        # Handle potential errors during data extraction or conversion
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'fulfillmentText': error_message}), 500  # Internal Server Error

    except requests.exceptions.RequestException as e:
        # Handle errors related to API requests (e.g., network issues, timeouts)
        error_message = f"Error fetching conversion rates: {str(e)}"
        return jsonify({'fulfillmentText': error_message}), 500  # Internal Server Error

def fetch_conversion_factor(source, target):
    url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest"
    querystring = {"from": source, "to": target}
    headers = {
        "X-RapidAPI-Key": "e485732eefmsh37b836e2e48ec37p10a6b4jsn641e582e0d80",  # Replace with your actual key
        "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
    }

    try:
        response = session.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if 'rates' in data:
                return data['rates'][target]
        return None
    except requests.exceptions.RequestException as e:
        # Handle potential errors during API requests
        print(f"Error fetching conversion factor: {str(e)}")  # Log the error
        return None

if __name__ == "__main__":
    app.run(debug=True)
