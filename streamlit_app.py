import os
import requests
import pandas as pd
import streamlit as st

# Use Docker service name if running in Docker, otherwise localhost
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv("data/car-details.csv")


def get_unique_options(df: pd.DataFrame):
    return {
        "company": sorted(df["company"].dropna().unique().tolist()),
        "owner": sorted(df["owner"].dropna().unique().tolist()),
        "fuel": sorted(df["fuel"].dropna().unique().tolist()),
        "seller_type": sorted(df["seller_type"].dropna().unique().tolist()),
        "transmission": sorted(df["transmission"].dropna().unique().tolist()),
        "year": sorted(df["year"].dropna().unique().tolist()),
        "seats": sorted(df["seats"].dropna().unique().tolist()),
    }


def login(username: str, password: str) -> str | None:
    try:
        resp = requests.post(f"{API_BASE_URL}/login", json={"username": username, "password": password}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("access_token")
    except Exception as exc:  # noqa: BLE001
        st.error(f"Login failed: {exc}")
        return None


def predict(token: str, api_key: str, payload: dict) -> float | None:
    headers = {
        "token": token,
        "api_key": api_key,
    }
    try:
        resp = requests.post(f"{API_BASE_URL}/predict", json=payload, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        return data.get("predicted_price")
    except Exception as exc:  # noqa: BLE001
        st.error(f"Prediction failed: {exc}")
        return None


def main():
    st.title("Car Price Prediction")
    st.markdown("A simple Streamlit frontend for your FastAPI ML model.")

    df = load_data()
    options = get_unique_options(df)

    with st.expander("Authentication", expanded=True):
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", value="admin", type="password")
        api_key = st.text_input("API Key", value="demo-key")

        if "token" not in st.session_state:
            st.session_state.token = None

        if st.button("Login"):
            token = login(username, password)
            if token:
                st.session_state.token = token
                st.success("Logged in successfully.")

    st.markdown("---")
    st.header("Car Features")

    col1, col2 = st.columns(2)

    with col1:
        company = st.selectbox("Company", options["company"])
        owner = st.selectbox("Owner", options["owner"])
        fuel = st.selectbox("Fuel", options["fuel"])
        seller_type = st.selectbox("Seller Type", options["seller_type"])
        transmission = st.selectbox("Transmission", options["transmission"])

    with col2:
        year = st.selectbox("Year", options["year"])
        seats = st.selectbox("Seats", options["seats"])

        km_driven = st.number_input("Kilometers Driven", min_value=0.0, value=float(df["km_driven"].median()))
        mileage_mpg = st.number_input("Mileage (mpg)", min_value=0.0, value=float(df["mileage_mpg"].dropna().median()))
        engine_cc = st.number_input("Engine (cc)", min_value=0.0, value=float(df["engine_cc"].dropna().median()))
        max_power_bhp = st.number_input(
            "Max Power (bhp)", min_value=0.0, value=float(df["max_power_bhp"].dropna().median())
        )
        torque = st.number_input("Torque (Nm)", min_value=0.0, value=float(df["torque_nm"].dropna().median()))

    if st.button("Predict Price"):
        if not st.session_state.get("token"):
            st.error("Please login first.")
            return

        payload = {
            "company": company,
            "year": int(year),
            "owner": owner,
            "fuel": fuel,
            "seller_type": seller_type,
            "transmission": transmission,
            "km_driven": float(km_driven),
            "mileage_mpg": float(mileage_mpg),
            "engine_cc": float(engine_cc),
            "max_power_bhp": float(max_power_bhp),
            "torque": float(torque),
            "seats": float(seats),
        }

        price = predict(st.session_state.token, api_key, payload)
        if price is not None:
            st.success(f"Predicted Price: ₹{price:,.0f}")


if __name__ == "__main__":
    main()

