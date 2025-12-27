from app.services.llm import llm_parse
from dotenv import load_dotenv
load_dotenv()

tests = [
    # "عايزة أروح من العصافرة لسيدي جابر",
    # "ازاي اروح محطة مصر",
    "من سان ستيفانو لبحري",
    # "عايز اقرب محطة ترام", 
    "بقولك يا صاحبي ازاي اروح من سيدي جابر لسيدي بشر", 
    # "اريد الذهاب من العصفرة الي الشاطبي",
    "عايز اروح من الموقف الجديد للمنشية"
    
]

for t in tests:
    print(t)
    print(llm_parse(t))
    print("------")

# parsed using gemini 3 flash , all extracted correct 