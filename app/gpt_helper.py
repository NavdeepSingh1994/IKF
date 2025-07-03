import openai
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DATA_PATH = Path(__file__).parent.parent / "data" / "example_incidents.json"

def load_incident_context():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data["incidents"], indent=2, ensure_ascii=False)
    except Exception as e:
        return f"[Fehler beim Laden der Incident-Daten: {e}]"

def answer_question(prompt: str) -> str:
    try:
        incident_context = load_incident_context()
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "Du bist ein technischer Co-Pilot im Bereich Flugsicherung und Incident Management. "
                    "Antworten basieren auf folgenden Incident-Daten:\n" + incident_context
                )},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Fehler bei der Anfrage an GPT-4: {e}"
