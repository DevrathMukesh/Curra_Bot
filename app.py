import streamlit as st
import requests

@st.cache
def fetch_conversion_factor(source, target):
    url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest"
    querystring = {"from": source, "to": target}
    headers = {
        "X-RapidAPI-Key": "e485732eefmsh37b836e2e48ec37p10a6b4jsn641e582e0d80",  # Replace with your actual key
        "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if 'rates' in data:
                return data['rates'][target]
        return None
    except requests.exceptions.RequestException as e:
        # Handle potential errors during API requests
        print(f"Error fetching conversion factor: {str(e)}")  # Log the error
        return None

def main():
    st.title("Currency Conversion")

    source_currency = st.text_input("Source Currency")
    amount = st.number_input("Amount", value=1.0)
    target_currencies = st.text_input("Target Currencies (comma-separated)").split(",")

    if st.button("Convert"):
        response_text = ""
        for target_currency in target_currencies:
            cf = fetch_conversion_factor(source_currency.strip(), target_currency.strip())
            if cf is not None:
                final_amount = amount * cf
                response_text += "{} {} is {} {}\n".format(amount, source_currency, final_amount, target_currency)
            else:
                response_text += f"Error: Unable to fetch conversion factor for {source_currency} to {target_currency}\n"
        
        st.text_area("Conversion Results", response_text)

if __name__ == "__main__":
    main()
