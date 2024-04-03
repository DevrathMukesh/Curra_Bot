import streamlit as st
from utils import fetch_conversion_factor

def main():
    st.title("Currency Conversion")

    source_currency = st.text_input("Enter source currency:")
    amount = st.number_input("Enter amount:")
    target_currency = st.text_input("Enter target currency:")

    if st.button("Convert"):
        cf = fetch_conversion_factor(source_currency, target_currency)
        if cf is not None:
            final_amount = amount * cf
            st.write(f"{amount} {source_currency} is {final_amount} {target_currency}")
        else:
            st.error(f"Error: Unable to fetch conversion factor for {source_currency} to {target_currency}")

if __name__ == "__main__":
    main()
