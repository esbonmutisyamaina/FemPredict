import streamlit as st
from datetime import datetime, timedelta


class CycleTracker:
    def __init__(self, period_start_date, cycle_length, period_duration):
        self.period_start_date = datetime.strptime(period_start_date, "%Y-%m-%d")
        self.cycle_length = cycle_length
        self.period_duration = period_duration

    def calculate_next_period(self):
        next_period_date = self.period_start_date + timedelta(days=self.cycle_length)
        return next_period_date.strftime('%d-%m-%Y')

    def calculate_safe_days(self):
        safe_days_start = self.period_start_date + timedelta(days=(self.period_duration))
        safe_days_end = safe_days_start + timedelta(days=3)
        return safe_days_start.strftime('%d-%m-%Y'), safe_days_end.strftime('%d-%m-%Y')

    def calculate_fertile_window(self):
        ovulation_date = self.period_start_date + timedelta(days=(self.cycle_length // 2))
        fertile_start = ovulation_date - timedelta(days=5)
        fertile_end = ovulation_date + timedelta(days=1)
        return fertile_start.strftime('%d-%m-%Y'), fertile_end.strftime('%d-%m-%Y'), ovulation_date.strftime('%d-%m-%Y')


class ShettlesGenderPrediction:
    def __init__(self, ovulation_date):
        self.ovulation_date = datetime.strptime(ovulation_date, "%d-%m-%Y")

    def predict_gender(self, intercourse_date):
        intercourse_date = datetime.strptime(intercourse_date, "%Y-%m-%d")
        days_difference = (self.ovulation_date - intercourse_date).days

        if 0 <= days_difference <= 1:
            return "You are more likely to conceive a boy." #75%
        elif 2 <= days_difference <= 5:
            return "You are more likely to conceive a girl." #80%
        else:
            return "Intercourse timing is outside the estimated fertile window."


# Streamlit app layout
st.title("Period Tracker & Pregnancy Gender Predictor (FEMPREDICT)")
st.write("SHETTLES METHOD")

# Initialize session state to store ovulation_date
if 'ovulation_date' not in st.session_state:
    st.session_state['ovulation_date'] = None

# Input fields for cycle tracking
period_start = st.date_input("Start Date of Last Period:")
cycle_length = st.number_input("Average Cycle Length (days):", min_value=20, max_value=45, value=28)
period_duration = st.number_input("Period Duration (days):", min_value=1, max_value=10, value=5)

# Button to calculate cycle and fertile window
if st.button("Calculate Cycle"):
    period_start_str = period_start.strftime("%Y-%m-%d")
    tracker = CycleTracker(period_start_str, cycle_length, period_duration)

    next_period = tracker.calculate_next_period()
    fertile_start, fertile_end, ovulation_date = tracker.calculate_fertile_window()

    # Calculate safe days
    safe_days_start, safe_days_end = tracker.calculate_safe_days()
    safe_days = f"{safe_days_start} to {safe_days_end}"

    # Save ovulation_date to session state
    st.session_state['ovulation_date'] = ovulation_date

    # Display results
    st.write(f"Safe Days: {safe_days}")
    st.write(f"Estimated Ovulation Date: {ovulation_date}")
    st.write(f"Fertile Window: {fertile_start} to {fertile_end}")
    st.write(f"Next Period: {next_period}")


# Input for gender prediction
intercourse_date = st.date_input("Date of Intercourse:")

# Button to predict gender
if st.button("Predict Gender"):
    if st.session_state['ovulation_date'] is not None:
        gender_predictor = ShettlesGenderPrediction(st.session_state['ovulation_date'])
        result = gender_predictor.predict_gender(intercourse_date.strftime("%Y-%m-%d"))
        st.write(result)
    else:
        st.warning("Please calculate your cycle first to get the ovulation date.")


hide_github_icon = """
<style>
[data-testid="stToolbar"] {visibility: hidden;}
</style>
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

# Closing remarks
st.markdown("---")  # This adds a horizontal line for separation
st.markdown("Based on biological data and mathematical estimations.")
st.markdown("Accuracy levels are 75% to 80%.")
st.markdown("### Made with ❤️ by Esbon Mutisya Maina")


