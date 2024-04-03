import requests


def fetch_conversion_factor(source, target):
    url = "https://api.currencyfreaks.com/v2.0/rates/latest"
    querystring = {"apikey": "3cbfcef7ed864220a3cbe9ab333f398d"}

    response = requests.get(url, params=querystring)

    if response.status_code == 200:
        data = response.json()
        if 'rates' in data:
            ex_s = float(data['rates'][source.upper()])  # Convert to uppercase
            ex_t = float(data['rates'][target.upper()])  # Convert to uppercase
            return ex_t / ex_s  # Return the conversion factor
    else:
        print("Error:", response.text)  # Print the error response
        return None


if __name__ == "__main__":
    main()

# # Example usage:
# conversion_factor = fetch_conversion_factor("INR", "USD")
# if conversion_factor is not None:
#     amount = 1
#     final_amount = amount * conversion_factor
#     print("Final Amount:", final_amount)
# else:
#     print("Failed to fetch conversion factor.")
#
