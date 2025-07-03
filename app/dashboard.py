import streamlit as st
from app.incident_handler import get_active_incidents
from app.maintenance import get_maintenance_tasks
from app.export import generate_pdf_report


def main_dashboard():
    st.title("🛫 FlightOps Incident Dashboard")

    st.header("📍 Aktive Incidents")
    incidents = get_active_incidents()
    for inc in incidents:
        st.error(f"{inc['system']} – {inc['priority']} – {inc['message']}")

    st.header("🛠️ Geplante Wartungen")
    maint = get_maintenance_tasks()
    for m in maint:
        st.info(f"{m['system']} – {m['window']} – {m['note']}")

    if st.button("📤 PDF-Report generieren"):
        generate_pdf_report(incidents, maint)
        st.success("✅ Report wurde generiert!")
