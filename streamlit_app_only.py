import streamlit as st
import requests

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
            ex_s=data['rates'][source]
            ex_t=data['rates'][target]
            ex_c=ex_s/ex_t
            # print(ex_c)
            return ex_c
    return None

def main():
    st.title("Currency Converter")

    source_currency = st.text_input("Enter source currency:")
    amount = st.number_input("Enter amount:", value=1.0)
    target_currencies = st.text_input("Enter target currencies separated by comma (e.g., USD, EUR):")

    if source_currency and amount and target_currencies:
        target_currencies = [currency.strip() for currency in target_currencies.split(",")]
        response_text = ""
        for target_currency in target_currencies:
            cf = fetch_conversion_factor(source_currency, target_currency)
            if cf is not None:
                
                final_amount = amount * cf
                response_text += "{} {} is {} {}\n".format(amount,target_currency , final_amount, source_currency)
            else:
                response_text += f"Error: Unable to fetch conversion factor for {source_currency} to {target_currency}\n"
        
        st.text_area("Conversion Results:", value=response_text)

if __name__ == "__main__":
    main()
