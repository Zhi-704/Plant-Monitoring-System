"""Functions for generating Altair Charts."""

import pandas as pd
import altair as alt


def get_bar_chart_of_latest_temperature_per_plant(live_reading_data: pd.DataFrame) -> alt.Chart:
    """Returns an Altair bar chart of the latest temperature of each plant."""

    latest_readings = live_reading_data.sort_values(
        'timestamp').drop_duplicates('name', keep='last')

    return alt.Chart(latest_readings).mark_bar(color="DarkGreen").encode(
        x=alt.X('name:N', title='Plant Name'),
        y=alt.Y('temperature:Q', title='Temperature (°C)'),
        color=alt.Color('temperature:Q', scale=alt.Scale(scheme='oranges')
                        )).properties(
        title='Latest Temperature Readings for Each Plant', width=1200, height=400,
    ).interactive()


def get_bar_chart_of_latest_soil_moisture_per_plant(live_reading_data: pd.DataFrame) -> alt.Chart:
    """Returns an Altair bar chart of the latest soil moisture of each plant."""

    latest_readings = live_reading_data.sort_values(
        'timestamp').drop_duplicates('name', keep='last')

    return alt.Chart(latest_readings).mark_bar(color='green').encode(
        x=alt.X('name:N', title='Plant Name'),
        y=alt.Y('soil_moisture:Q', title='Soil Moisture (%)'),
        color=alt.Color('soil_moisture:Q', scale=alt.Scale(scheme='blues'))
    ).properties(
        title='Latest Soil Moisture Readings for Each Plant',
        width=1200,
        height=400
    ).interactive()
