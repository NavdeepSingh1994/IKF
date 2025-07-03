def get_maintenance_tasks():
    return [
        {
            "system": "Radar Innsbruck",
            "window": "04.07.2025 – 02:00–03:00",
            "note": "Firmwareupdate geplant"
        },
        {
            "system": "Voice Comm Salzburg",
            "window": "04.07.2025 – 04:00–05:00",
            "note": "Austausch Audiomatrix"
        }
    ]
import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "maintenance.json"

def get_maintenance_tasks():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)["maintenance"]
    except:
        return []

def add_maintenance(system, window, note):
    try:
        path = DATA_PATH
        if not path.exists():
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"maintenance": []}, f)

        with open(path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data["maintenance"].append({
                "system": system,
                "window": window,
                "note": note
            })
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()
    except Exception as e:
        print(f"Fehler beim Hinzufügen der Wartung: {e}")
