import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sidebar inputs
st.sidebar.title("Lamar Health ROI Calculator")
patients_per_month = st.sidebar.number_input("Number of Patients per Month", value=200)
hourly_salary = st.sidebar.number_input("Hourly Salary ($)", value=22)
years = st.sidebar.number_input("Time Horizon (Years)", value=3)

# Module toggles and formulas
enable_fax = st.sidebar.checkbox("Include Fax Processing", value=True)
st.sidebar.caption("**Fax Processing Formula:**\nBefore: 15 min × patients/month × hourly wage\nAfter: $fax price + 1 min × patients/month × hourly wage")
fax_price = st.sidebar.number_input("Lamar Fax Processing Price ($)", value=2)

enable_benefit = st.sidebar.checkbox("Include Benefit Check", value=True)
st.sidebar.caption("**Benefit Check Formula:**\nBefore: 30 min × patients/month × hourly wage\nAfter: $benefit check price + 1 min × patients/month × hourly wage")
benefit_price = st.sidebar.number_input("Lamar Benefit Check Price ($)", value=6)

enable_auth = st.sidebar.checkbox("Include Prior Authorization", value=True)
st.sidebar.caption("**Prior Authorization Formula:**\nBefore: 30 min × patients/month × hourly wage\nAfter: $prior auth price + 1 min × patients/month × hourly wage")
auth_price = st.sidebar.number_input("Lamar Prior Authorization Price ($)", value=6)

# Constants
months = years * 12
minutes_to_hours = 1 / 60

# Time per task (in minutes)
fax_time = 15
benefit_time = 30
auth_time = 30
post_lamar_time = 1  # 1 minute of staff time per patient per module

# Cost before Lamar
cost_before_fax = fax_time * minutes_to_hours * patients_per_month * hourly_salary * months if enable_fax else 0
cost_before_benefit = benefit_time * minutes_to_hours * patients_per_month * hourly_salary * months if enable_benefit else 0
cost_before_auth = auth_time * minutes_to_hours * patients_per_month * hourly_salary * months if enable_auth else 0
cost_before_total = cost_before_fax + cost_before_benefit + cost_before_auth

# Cost after Lamar (module price + 1 min of staff time)
cost_after_fax = (fax_price + post_lamar_time * minutes_to_hours * hourly_salary) * patients_per_month * months if enable_fax else 0
cost_after_benefit = (benefit_price + post_lamar_time * minutes_to_hours * hourly_salary) * patients_per_month * months if enable_benefit else 0
cost_after_auth = (auth_price + post_lamar_time * minutes_to_hours * hourly_salary) * patients_per_month * months if enable_auth else 0
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
costs_after = [((fax_price + post_lamar_time * minutes_to_hours * hourly_salary) * patients_per_month * enable_fax +
                (benefit_price + post_lamar_time * minutes_to_hours * hourly_salary) * patients_per_month * enable_benefit +
                (auth_price + post_lamar_time * minutes_to_hours * hourly_salary) * patients_per_month * enable_auth) * m for m in months_range]

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

# Revenue Recapture
st.header("Revenue Recapture")
denial_rates = [x / 100 for x in range(0, 21)]  # 0% to 20%
patients_per_year = patients_per_month * 12
revenue_per_patient = 80000  # Assumed chronic patient annual revenue
revenue_recaptured = [patients_per_year * revenue_per_patient * rate for rate in denial_rates]

revenue_data = pd.DataFrame({
    'Denial Rate Improvement (%)': [r * 100 for r in denial_rates],
    'Revenue Recaptured ($)': revenue_recaptured
})

# Plot revenue recapture
fig2, ax2 = plt.subplots()
ax2.plot(revenue_data['Denial Rate Improvement (%)'], revenue_data['Revenue Recaptured ($)'])
ax2.set_xlabel('Denial Rate Improvement (%)')
ax2.set_ylabel('Revenue Recaptured ($)')
ax2.set_title('Revenue Recapture vs. Denial Rate Improvement')
st.pyplot(fig2)

# Explanation of revenue recapture calculation
st.caption("""
**Calculation Logic:**
Revenue Recaptured = Number of Patients per Year × $80,000 (estimated chronic care revenue per patient) × Denial Rate Improvement (%)

This assumes each patient contributes $80,000 annually and that improvement in denial rates results in direct revenue recovery.
""") × Denial Rate Improvement (%)

This assumes each patient contributes $80,000 annually and that improvement in denial rates results in direct revenue recovery.")
