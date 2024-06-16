"""Creates dashboard with streamlit"""

from os import environ as ENV
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import utils
import charts

AWS_ACCESS_KEY = ENV["ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = ENV["SECRET_ACCESS_KEY"]


if __name__ == "__main__":

    destination_path = "./data"

    load_dotenv()

    conn = utils.get_connection()

    live_data = utils.get_live_data(conn)
    live_data['timestamp'] = pd.to_datetime(live_data['timestamp'])

    archived_data = utils.get_archived_data(
        str(AWS_ACCESS_KEY), str(AWS_SECRET_ACCESS_KEY))

    archived_data['timestamp'] = pd.to_datetime(archived_data['timestamp'])

    st.title("🌴 LMNH Plant Health Tracker 🪷")

    st.altair_chart(
        charts.get_bar_chart_of_latest_temperature_per_plant(live_data))

    st.altair_chart(
        charts.get_bar_chart_of_latest_soil_moisture_per_plant(live_data)
    )

    st.subheader("Archived Data")
    st.dataframe(archived_data)
