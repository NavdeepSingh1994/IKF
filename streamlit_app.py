import streamlit as st
from app.dashboard import main_dashboard

st.set_page_config(page_title="FlightOps Incident Dashboard", layout="wide")
main_dashboard()
