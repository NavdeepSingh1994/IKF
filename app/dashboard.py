import streamlit as st
from app.incident_handler import get_active_incidents, add_incident
from app.maintenance import get_maintenance_tasks
from app.export import generate_pdf_report
from datetime import datetime

def main_dashboard():
    st.title("🛫 FlightOps Incident Dashboard")

    # --- Formular für neue Incidents ---
    st.header("➕ Neuen Incident erfassen")
    with st.form("incident_form"):
        system = st.text_input("System", placeholder="z. B. Radar Wien-Schwechat")
        priority = st.selectbox("Priorität", ["Kritisch", "Hoch", "Mittel", "Niedrig"])
        message = st.text_input("Beschreibung", placeholder="z. B. Kein Signal seit 03:24 UTC")
        submitted = st.form_submit_button("✅ Incident hinzufügen")

        if submitted:
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            add_incident(system, priority, f"{message} (erfasst: {timestamp})")
            st.success("📌 Neuer Incident wurde gespeichert.")

    # --- Filteroption ---
    st.header("📍 Aktive Incidents")
    filter_option = st.selectbox("🔎 Nur diese Priorität anzeigen:", ["Alle", "Kritisch", "Hoch", "Mittel", "Niedrig"])
    incidents = get_active_incidents()

    filtered_incidents = [
        inc for inc in incidents if filter_option == "Alle" or inc["priority"] == filter_option
    ]

    if not filtered_incidents:
        st.info("Keine Incidents mit dieser Priorität.")
    else:
        for idx, inc in enumerate(filtered_incidents):
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.error(f"{inc['system']} – {inc['priority']} – {inc['message']}")
            with col2:
                if st.button("🗑️", key=f"del_{idx}"):
                    from app.incident_handler import remove_incident
                    remove_incident(inc)
                    st.experimental_rerun()

    # --- Geplante Wartungen anzeigen ---
    st.header("🛠️ Geplante Wartungen")
    maint = get_maintenance_tasks()
    for m in maint:
        st.info(f"{m['system']} – {m['window']} – {m['note']}")

    # --- PDF-Export ---
    if st.button("📤 PDF-Report generieren"):
        generate_pdf_report(incidents, maint)
        st.success("✅ Report wurde generiert!")
