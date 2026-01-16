import os
import json
from typing import Dict, Any
from google.genai import Client, types
from dotenv import load_dotenv


load_dotenv()

client = Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)
SYSTEM_PROMPT = """
انت مساعد ذكي بتشرح رحلات مواصلات للناس بطريقة بسيطة ولطيفة.

المدخل JSON فيه:
- origin
- destination
- journeys: قائمة من البدائل

كل Journey فيها:
- summary: (وقت إجمالي بالدقايق، تكلفة تقريبية، مسافة مشي، عدد تحويلات، modes)
- legs: قائمة خطوات الرحلة

كل Leg نوعه واحد من:
- walk: مشي (مسافة/وقت)
- trip: مواصلة (mode + route_short_name + من محطة/إلى محطة + وقت + fare)
- transfer: تحويل/مشي بين وسيلتين (وقت/مسافة)

المطلوب:
- اكتب بالعامية المصرية
- اشرح كل رحلة في فقرة منفصلة
- اذكر: الوقت الإجمالي، المشي، التكلفة/السعر لو موجود
- اشرح الخطوات بالترتيب (legs)  
- لو مفيش رحلات قول: "مع الأسف مفيش رحلات مناسبة دلوقتي."
"""

def format_server_journeys_for_user_llm(
    journeys: list,
    origin: str,
    dest: str
) -> str:
    try:
        if not journeys:
            return "مع الأسف مفيش رحلات مناسبة دلوقتي."

        clean_journeys = []
        for j in journeys:
            summary = j.get("summary") or {}
            legs = j.get("legs") or []

            clean_legs = []
            for leg in legs:
                t = leg.get("type")
                if t == "walk":
                    clean_legs.append(
                        {
                            "type": "walk",
                            "distance_meters": int(leg.get("distance_meters", 0)),
                            "duration_minutes": int(leg.get("duration_minutes", 0)),
                        }
                    )
                elif t == "trip":
                    clean_legs.append(
                        {
                            "type": "trip",
                            "mode": leg.get("mode", ""),
                            "route_short_name": leg.get("route_short_name", ""),
                            "headsign": leg.get("headsign", ""),
                            "from": (leg.get("from") or {}).get("name", ""),
                            "to": (leg.get("to") or {}).get("name", ""),
                            "duration_minutes": int(leg.get("duration_minutes", 0)),
                            "fare": float(leg.get("fare", 0.0)),
                        }
                    )
                elif t == "transfer":
                    clean_legs.append(
                        {
                            "type": "transfer",
                            "from_trip_name": leg.get("from_trip_name", ""),
                            "to_trip_name": leg.get("to_trip_name", ""),
                            "walking_distance_meters": int(leg.get("walking_distance_meters", 0)),
                            "duration_minutes": int(leg.get("duration_minutes", 0)),
                        }
                    )

            clean_journeys.append(
                {
                    "id": j.get("id"),
                    "summary": {
                        "total_time_minutes": int(summary.get("total_time_minutes", 0)),
                        "walking_distance_meters": int(summary.get("walking_distance_meters", 0)),
                        "transfers": int(summary.get("transfers", 0)),
                        "cost": float(summary.get("cost", 0.0)),
                        "modes": summary.get("modes", []),
                    },
                    "legs": clean_legs,
                    "text_summary": j.get("text_summary", ""),
                }
            )

        payload = {
            "origin": origin,
            "destination": dest,
            "journeys": clean_journeys
        }

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[json.dumps(payload, ensure_ascii=False)],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature= 0,
                response_mime_type="text/plain"
            )
        )

        return response.text

    except Exception as e:
        print(f"[LLM FORMAT ERROR] {e}")
        return "حصلت مشكلة واحنا بنجهز الرحلات، جرب تاني."
