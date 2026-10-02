# Mission Engine - Phase 0
import json
from datetime import datetime

class CitizenPortal:
    def __init__(self):
        self.records_file = "citizens_data.json"

    def register_case(self, name, phone, problem_type, description):
        case_data = {
            "timestamp": str(datetime.now()),
            "name": name,
            "phone": phone,
            "category": problem_type,
            "description": description,
            "status": "QUEUED_FOR_RESOLUTION"
        }
        
        # डेटा को सुरक्षित फाइल में सेव करना
        try:
            with open(self.records_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(case_data)

        with open(self.records_file, "w") as f:
            json.dump(data, f, indent=4)

        print(f"\n[सफलता] {name} का केस सिस्टम में दर्ज हो गया है।")
        print("अगला कदम: इस समस्या के समाधान का रूट तैयार करना।\n")

if __name__ == "__main__":
    portal = CitizenPortal()
    print("=== भारत जन-समस्या समाधान इंजन ===")
    naam = input("नागरिक का नाम दर्ज करें: ")
    mobile = input("मोबाइल नंबर दर्ज करें: ")
    print("समस्या का वर्ग चुनें: 1. राशन/योजना  2. पीएफ/पेंशन  3. मजदूरी/उधार")
    varg = input("विकल्प नंबर लिखें: ")
    vivaran = input("समस्या का पूरा विवरण लिखें: ")
    
    portal.register_case(naam, mobile, varg, vivaran)
