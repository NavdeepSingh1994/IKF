import streamlit as st
from datetime import datetime
from app.incident_handler import get_active_incidents, add_incident, remove_incident
from app.maintenance import get_maintenance_tasks
from app.export import generate_pdf_report
import time
from app.gpt_helper import answer_question


def main_dashboard():
    st.title("🛫 FlightOps Incident Dashboard")

    # --- Rollensteuerung ---
    role = st.radio("🔐 Rolle auswählen:", ["👨 Operator", "🧑‍✈️ Einsatzleitung"])

    if role == "🧑‍✈️ Einsatzleitung":
        selected_form = st.radio("📋 Was möchtest du erfassen?", ["🧨 Incident", "🛠️ Wartung"])

        if selected_form == "🧨 Incident":
            st.subheader("➕ Neuen Incident erfassen")
            with st.form("incident_form"):
                system = st.text_input("System", placeholder="z. B. Radar Wien-Schwechat")
                priority = st.selectbox("Priorität", ["Kritisch", "Hoch", "Mittel", "Niedrig"])
                message = st.text_input("Beschreibung", placeholder="z. B. Kein Signal seit 03:24 UTC")
                submitted = st.form_submit_button("✅ Incident hinzufügen")

                if submitted:
                    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                    full_message = f"{message} (erstellt: {timestamp})"
                    add_incident(system, priority, full_message)
                    st.success("📌 Neuer Incident wurde gespeichert.")
                    st.rerun()

        elif selected_form == "🛠️ Wartung":
            st.subheader("🛠️ Neue Wartung planen")
            with st.form("maintenance_form"):
                system = st.text_input("System (Wartung)", placeholder="z. B. Voice Comm Salzburg")
                window = st.text_input("Wartungsfenster", placeholder="z. B. 04.07.2025 – 04:00–05:00")
                note = st.text_input("Beschreibung", placeholder="z. B. Austausch Audiomatrix")
                submitted = st.form_submit_button("✅ Wartung hinzufügen")

                if submitted:
                    from app.maintenance import add_maintenance
                    add_maintenance(system, window, note)
                    st.success("🛠️ Wartung hinzugefügt.")
                    st.rerun()

    # --- FlightGPT Chatbot ---
    with st.expander("💬 Frag FlightGPT: Dein Incident-Co-Pilot"):
        user_question = st.text_input("Deine Frage", placeholder="z. B. Was bedeutet Priorität 'Hoch'?")

        if user_question:
            with st.spinner("✈️ FlightGPT denkt nach..."):
                response = answer_question(user_question)
            st.success(response)

    # --- Filter für Prioritäten ---
    st.header("📍 Aktive Incidents")
    filter_option = st.selectbox("🔎 Nur diese Priorität anzeigen:", ["Alle", "Kritisch", "Hoch", "Mittel", "Niedrig"])
    incidents = get_active_incidents()
    filtered_incidents = [
        inc for inc in incidents if filter_option == "Alle" or inc["priority"] == filter_option
    ]

    if not filtered_incidents:
        st.info("Keine Incidents mit dieser Priorität.")
    else:
        priority_colors = {
            "Kritisch": "#e63946",  # Rot
            "Hoch": "#f77f00",  # Orange
            "Mittel": "#f1c40f",  # Gelb
            "Niedrig": "##3498db"  # Blau
        }

        for idx, inc in enumerate(filtered_incidents):
            color = priority_colors.get(inc["priority"], "#cccccc")
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.markdown(
                    f"<div style='background-color:{color}; padding:10px; border-radius:8px; color:white;'>"
                    f"<b>{inc['system']}</b> – <i>{inc['priority']}</i> – {inc['message']}</div>",
                    unsafe_allow_html=True
                )
            with col2:
                if role == "🧑‍✈️ Einsatzleitung":
                    if st.button("🗑️", key=f"del_{idx}"):
                        remove_incident(inc)
                        st.rerun()


    # --- Geplante Wartungen ---
    st.header("🛠️ Geplante Wartungen")
    maint = get_maintenance_tasks()
    for m in maint:
        st.markdown(
            f"<div style='background-color:#00bcd4; padding:10px; border-radius:8px; color:white;'>"
            f"<b>{m['system']}</b> – {m['window']} – {m['note']}</div>",
            unsafe_allow_html=True
        )

    # --- PDF Report ---
    if st.button("📤 PDF-Report generieren"):
        generate_pdf_report(incidents, maint)
        st.success("✅ Report wurde generiert!")
