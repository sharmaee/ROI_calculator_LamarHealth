import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.title('Lamar Health ROI Calculator')

# Get URL parameters for initial values
params = st.experimental_get_query_params()
avg_time_init = int(params.get("avg_time", [60])[0])
hourly_rate_init = int(params.get("hourly_rate", [22])[0])
prior_auth_vol_init = int(params.get("patient_vol", [17])[0])
platform_fee_init = int(params.get("platform_fee", [5000])[0])
price_per_auth_init = float(params.get("price_per_patient", [6.5])[0])

# Main columns for layout
slider_col, content_col = st.columns([1, 3])

with slider_col:
    #st.write("## Parameters")
    avg_time = st.slider('Average Time Per Patient Today (min)', min_value=0, max_value=100, value=avg_time_init)
    hourly_rate = st.slider('Hourly Salary (USD$)', min_value=0, max_value=60, value=hourly_rate_init)
    prior_auth_vol = st.slider('Patient Volume Per Week', min_value=0, max_value=50000, value=prior_auth_vol_init)
    platform_fee = st.slider('Platform Fee (USD$)', min_value=0, max_value=50000, value=platform_fee_init)
    price_per_auth = st.slider('Our Price Per Patient (USD$)', min_value=2.0, max_value=10.0, value=price_per_auth_init)
    efficiency = st.slider('Reduction in time spent (Efficiency)', min_value=0, max_value=100, value=90)
    number_of_years = st.slider('Years', min_value=0, max_value=5, value=3)



def calculate_roi_over_time(avg_time, hourly_rate, prior_auth_vol, platform_fee, price_per_auth, efficiency, number_of_years):
    years = np.arange(1, number_of_years + 1)
    total_savings = []
    percent_savings = []
    total_time_saved = []
    cost_per_year_total = []
    price_per_year_total = []

    for year in years:
        min_per_week = prior_auth_vol * avg_time
        cost_per_week = min_per_week / 60 * hourly_rate
        #price_per_week = prior_auth_vol*price_per_auth
        #decrease_cost_per_week = cost_per_week * (1-efficiency / 100)

        cost_per_year = cost_per_week * 52 * year
        #savings = cost_per_week * 52 * year - decrease_cost_per_week * 52 * year - price_per_week * 52 * year - platform_fee * year
       
        time_saved = min_per_week * 52 * year * (efficiency / 100)
        
        price_per_year = prior_auth_vol*price_per_auth * 52 * year + platform_fee * year
        savings = time_saved/60*hourly_rate - price_per_year
        percent = (savings / (cost_per_week * 52 * year)) * 100

        total_savings.append(savings)
        percent_savings.append(percent)
        total_time_saved.append(time_saved)
        cost_per_year_total.append(cost_per_year)
        price_per_year_total.append(price_per_year)

    return years, total_savings, percent_savings, total_time_saved, cost_per_year_total, price_per_year_total

years, total_savings, percent_savings, total_time_saved, cost_per_year_total, price_per_year_total = calculate_roi_over_time(avg_time, hourly_rate, prior_auth_vol, platform_fee, price_per_auth, efficiency, number_of_years)

data = {
    'Total Time Saved (minutes)': int(total_time_saved[-1]),
    'Cost Without Lamar Health (USD$)': int(cost_per_year_total[-1]),
    'Cost With Lamar Health (USD$)': int(int(cost_per_year_total[-1]) - int(total_savings[-1])),
    'Total Savings (USD$)': int(total_savings[-1]),
    'Lamar Health Price (USD$)': int(price_per_year_total[-1]),
    'Percent Savings': int(percent_savings[-1])
}

# Convert the dictionary to a Pandas DataFrame
df = pd.DataFrame([data])

# Create a container for the table within the content column
with content_col.container():
    st.table(df)

# Create a container for the graph within the content column
with content_col.container():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, total_savings, label='Total Savings', marker='o')
    #ax.plot(years, percent_savings, label='Percent Savings', marker='o')
    ax.plot(years, cost_per_year_total, label='Cost without Lamar Health', marker='o')
    ax.set_xlabel('Years')
    ax.set_ylabel('Total Dollars ($) Saved')
    ax.set_title('ROI Metrics Over Time')
    ax.legend()
    st.pyplot(fig)
