import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sidebar inputs
st.sidebar.title("Lamar Health ROI Calculator")
patients_per_month = st.sidebar.number_input("Number of Patients per Month", value=200)
hourly_salary = st.sidebar.number_input("Hourly Salary ($)", value=22)
years = st.sidebar.number_input("Time Horizon (Years)", value=3)

# Module toggles
enable_fax = st.sidebar.checkbox("Include Fax Processing", value=True)
enable_benefit = st.sidebar.checkbox("Include Benefit Check", value=True)
enable_auth = st.sidebar.checkbox("Include Prior Authorization", value=True)

fax_price = st.sidebar.number_input("Lamar Fax Processing Price ($)", value=2)
st.sidebar.caption("**Fax Processing Formula:** 15 min × patients/month × hourly wage (before) or fax price (after)")
benefit_price = st.sidebar.number_input("Lamar Benefit Check Price ($)", value=6)
st.sidebar.caption("**Benefit Check Formula:** 30 min × patients/month × hourly wage (before) or benefit check price (after)")
auth_price = st.sidebar.number_input("Lamar Prior Authorization Price ($)", value=6)
st.sidebar.caption("**Prior Authorization Formula:** 30 min × patients/month × hourly wage (before) or prior auth price (after)")

# Constants
months = years * 12
minutes_to_hours = 1 / 60

# Time per task (in minutes)
fax_time = 15
benefit_time = 30
auth_time = 30

# Cost before Lamar
cost_before_fax = fax_time * minutes_to_hours * patients_per_month * hourly_salary * months if enable_fax else 0
cost_before_benefit = benefit_time * minutes_to_hours * patients_per_month * hourly_salary * months if enable_benefit else 0
cost_before_auth = auth_time * minutes_to_hours * patients_per_month * hourly_salary * months if enable_auth else 0
cost_before_total = cost_before_fax + cost_before_benefit + cost_before_auth

# Cost after Lamar
cost_after_fax = fax_time * minutes_to_hours * patients_per_month * fax_price * months if enable_fax else 0
cost_after_benefit = benefit_time * minutes_to_hours * patients_per_month * benefit_price * months if enable_benefit else 0
cost_after_auth = auth_time * minutes_to_hours * patients_per_month * auth_price * months if enable_auth else 0
cost_after_total = cost_after_fax + cost_after_benefit + cost_after_auth

# Savings
savings = cost_before_total - cost_after_total
time_saved_hours = savings / hourly_salary if hourly_salary != 0 else 0
roi_percent = (savings / cost_before_total) * 100 if cost_before_total != 0 else 0

# Summary
st.title("Lamar Health ROI Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Time Saved (Hours)", f"{time_saved_hours:,.2f}")
col2.metric("Cost Savings ($)", f"${savings:,.2f}")
col3.metric("ROI (%)", f"{roi_percent:.2f}%")

# Time graph data
months_range = list(range(1, months + 1))
costs_before = [((fax_time * enable_fax + benefit_time * enable_benefit + auth_time * enable_auth) * minutes_to_hours * patients_per_month * hourly_salary) * m for m in months_range]
costs_after = [((fax_time * fax_price * enable_fax + benefit_time * benefit_price * enable_benefit + auth_time * auth_price * enable_auth) * minutes_to_hours * patients_per_month) * m for m in months_range]

# Create DataFrame for plotting
data = pd.DataFrame({
    'Month': months_range,
    'Cost Before Lamar': costs_before,
    'Cost After Lamar': costs_after
})

# Plot the data
fig, ax = plt.subplots()
ax.plot(data['Month'], data['Cost Before Lamar'], label='Cost Before Lamar')
ax.plot(data['Month'], data['Cost After Lamar'], label='Cost After Lamar')
ax.set_xlabel('Month')
ax.set_ylabel('Cost ($)')
ax.set_title('Cost Over Time')
ax.legend()
st.pyplot(fig)

st.write("Lamar Health offers automation solutions across three modules: Fax Processing, Benefit Check, and Prior Authorization. Customize the inputs on the left to see how much you can save.")
