import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "example_incidents.json"

def get_active_incidents():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("incidents", [])
    except Exception as e:
        print(f"Fehler beim Laden der Incidents: {e}")
        return []
def add_incident(system, priority, message):
    try:
        with open(DATA_PATH, "r+", encoding="utf-8") as file:
            data = json.load(file)
            if "incidents" not in data:
                data["incidents"] = []
            data["incidents"].append({
                "system": system,
                "priority": priority,
                "message": message
            })
            file.seek(0)
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.truncate()
    except Exception as e:
        print(f"Fehler beim Hinzufügen des Incidents: {e}")

def remove_incident(incident_to_remove):
    try:
        with open(DATA_PATH, "r+", encoding="utf-8") as file:
            data = json.load(file)
            data["incidents"] = [
                inc for inc in data.get("incidents", [])
                if not (
                    inc["system"] == incident_to_remove["system"] and
                    inc["priority"] == incident_to_remove["priority"] and
                    inc["message"] == incident_to_remove["message"]
                )
            ]
            file.seek(0)
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.truncate()
    except Exception as e:
        print(f"Fehler beim Entfernen des Incidents: {e}")
