# ==============================================================================
# 🇮🇳 BHARAT JAN-MUNSHI OS v18.0 (Phonebook Sync + GPS Live SOS + Headless)
# Nirmaata: Sahil Ahmad | 100% Offline Civic OS
# ==============================================================================

import re
import json
import os
import subprocess
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import qrcode
except ImportError:
    pass

class MeshServerThread(threading.Thread):
    def run(self):
        try:
            server = HTTPServer(("0.0.0.0", 8080), SimpleHTTPRequestHandler)
            server.serve_forever()
        except Exception:
            pass

class BharatJanMunshi:
    def __init__(self):
        self.ledger_file = "khata_bahi.json"
        self.contacts_file = "contacts.json"
        self.grievance_file = "grievances.json"
        self.secret_voice_pin = "1234"
        self._init_files()
        self._start_mesh()

    def _init_files(self):
        for p in [self.ledger_file, self.grievance_file]:
            if not os.path.exists(p):
                with open(p, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=4)

    def _start_mesh(self):
        mesh = MeshServerThread()
        mesh.daemon = True
        mesh.start()

    def speak(self, text):
        clean = text.replace('"', '').replace("'", "")
        os.system(f'termux-tts-speak "{clean}"')

    def listen(self, prompt="Sun raha hoon..."):
        print(f"\n{prompt}")
        try:
            res = subprocess.run(["termux-speech-to-text"], stdout=subprocess.PIPE, text=True)
            return res.stdout.strip()
        except Exception:
            return ""

    def send_sms(self, phone, msg):
        clean_num = "".join(filter(str.isdigit, str(phone)))[-10:]
        if len(clean_num) == 10:
            os.system(f'termux-sms-send -n {clean_num} "{msg}"')

    # फोन की असली कॉन्टैक्ट बुक से नाम ढूंढना
    def find_number_in_phone(self, name):
        name_clean = name.lower().strip()
        try:
            res = subprocess.run(["termux-contact-list"], stdout=subprocess.PIPE, text=True, timeout=5)
            contacts = json.loads(res.stdout)
            for c in contacts:
                c_name = c.get("name", "").lower()
                if name_clean in c_name:
                    num = c.get("number", "")
                    clean = "".join(filter(str.isdigit, str(num)))[-10:]
                    if len(clean) == 10:
                        return clean
        except Exception:
            pass

        # अगर फोनबुक में न मिले तो लोकल फाइल चेक करना
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, "r", encoding="utf-8") as f:
                    local_c = json.load(f)
                    return local_c.get(name_clean, None)
            except Exception:
                pass
        return None

    def save_new_contact(self, name, phone):
        try:
            with open(self.contacts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
        data[name.lower().strip()] = str(phone)
        with open(self.contacts_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # लाइव GPS लोकेशन निकालना
    def get_live_gps_link(self):
        try:
            res = subprocess.run(["termux-location", "-p", "network", "-r", "once"], stdout=subprocess.PIPE, text=True, timeout=8)
            loc = json.loads(res.stdout)
            lat = loc.get("latitude")
            lon = loc.get("longitude")
            if lat and lon:
                return f"https://maps.google.com/?q={lat},{lon}"
        except Exception:
            pass
        return "Location unavailable (GPS timeout)"

    def trigger_sos_alert(self):
        os.system('termux-vibrate -f -d 2000')
        self.speak("Emergency SOS sakriya! Live location bheji ja rahi hai.")
        
        gps_url = self.get_live_gps_link()
        guardian_num = "7484878440"
        time_str = datetime.now().strftime('%H:%M:%S')
        
        msg = f"EMERGENCY ALERT: Mujhe turant madad chahiye!\nSamay: {time_str}\nLive Location: {gps_url}"
        self.send_sms(guardian_num, msg)
        self.speak("Aapki live location ke sath alert SMS bhej diya gaya hai.")

    def verify_smart_pin(self, text):
        digits = "".join(filter(str.isdigit, text))
        if "1234" in digits:
            return True
        valid_words = ["ek do teen char", "one two three four", "1 2 3 4", "barah chautees"]
        return any(w in text.lower() for w in valid_words)

    def trigger_upi_payment(self, target, amount):
        clean_target = "".join(filter(str.isdigit, str(target)))
        phone = None

        if len(clean_target) == 10:
            phone = clean_target
            person_name = f"Number-{phone[-4:]}"
        else:
            person_name = target
            phone = self.find_number_in_phone(target)

        # अगर कॉन्टैक्ट में भी नहीं मिला, तब ही सिर्फ एक बार पूछेगा
        if not phone:
            self.speak(f"{person_name} ka number phone me nahi mila. Dus ankon ka mobile number bolein.")
            phone_voice = self.listen("Mobile number bolein...")
            clean_phone = "".join(filter(str.isdigit, phone_voice))

            if len(clean_phone) >= 10:
                phone = clean_phone[-10:]
                self.save_new_contact(person_name, phone)
            else:
                self.speak("Sahi number nahi mila, payment cancel.")
                return

        self.speak(f"{person_name} ko {amount} rupaye bhejne ke liye gupt voice pin bolein.")
        pin_voice = self.listen("Pin bolein...")

        if not self.verify_smart_pin(pin_voice):
            self.speak("Galat voice pin! Suraksha ke liye bhugtan rok diya gaya hai.")
            return

        self.speak(f"{person_name} ko {amount} rupaye ka payment shuru kiya ja raha hai.")
        upi_url = f"upi://pay?pa={phone}@ybl&pn={person_name}&am={amount}&cu=INR"
        os.system(f'termux-open-url "{upi_url}"')
        self.add_entry(person_name, amount, f"{person_name} ko transfer")

    def add_entry(self, person, amount, raw_text):
        try:
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.append({"timestamp": now, "name": person, "amount": amount, "raw_voice": raw_text})
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        phone = self.find_number_in_phone(person)
        if phone:
            self.send_sms(phone, f"Jan-Munshi Receipt: {person} ji, khate me Rs {amount} darj hue. Samay: {now}")

        self.speak(f"{person} ke khate me {amount} rupaye likh diye gaye hain.")

    def generate_legal_pdf(self, case_id, dept, act, issue):
        pdf_path = f"{case_id}.pdf"
        qr_img_path = f"{case_id}_qr.png"
        try:
            qr_data = f"Bharat Jan-Munshi OS\nCase: {case_id}\nDept: {dept}\nAct: {act}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            qr = qrcode.make(qr_data)
            qr.save(qr_img_path)

            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, "BHARAT JAN-MUNSHI: OFFICIAL LEGAL COMPLAINT")
            c.setFont("Helvetica", 10)
            c.drawString(50, 735, "Digitally Verified Autonomous OS | Architect: Sahil Ahmad")
            c.line(50, 725, 550, 725)

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 690, f"Case Tracking ID: {case_id}")
            c.drawString(50, 670, f"Department: {dept}")
            c.drawString(50, 650, f"Applicable Legal Act: {act}")
            c.drawString(50, 630, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 590, "Citizen Grievance Matter:")
            c.setFont("Helvetica", 11)
            c.drawString(50, 570, f"Statement: {issue}")

            if os.path.exists(qr_img_path):
                c.drawImage(qr_img_path, 430, 600, width=100, height=100)

            c.line(50, 520, 550, 520)
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(50, 500, "Statutory Notice: Anti-Dalal Direct Action.")
            c.save()

            if os.path.exists(qr_img_path):
                os.remove(qr_img_path)

            os.system(f"cp {pdf_path} /sdcard/Download/ 2>/dev/null")
            os.system(f"termux-open --chooser /sdcard/Download/{pdf_path} 2>/dev/null")
            return True
        except Exception:
            return False

    def file_grievance(self, cat, text):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cid = f"CASE-{datetime.now().strftime('%H%M%S')}"

        if cat == "PF":
            dept = "Employees Provident Fund Organisation (EPFO)"
            act = "EPF & MP Act 1952 Sec 7A"
        elif cat == "RATION":
            dept = "Food & Civil Supplies Directorate"
            act = "NFSA 2013 (Right to Food Guarantee)"
        elif cat == "BIJLI":
            dept = "Electricity Regulatory Commission"
            act = "Electricity Act 2003 (Billing Code)"
        elif cat == "LABOR":
            dept = "Labour & Employment Department"
            act = "Minimum Wages Act 1948"
        else:
            dept = "Public Grievance Cell"
            act = "Right to Public Services Act"

        self.generate_legal_pdf(cid, dept, act, text)

        try:
            with open(self.grievance_file, "r", encoding="utf-8") as f:
                cases = json.load(f)
        except Exception:
            cases = []

        cases.append({"case_id": cid, "timestamp": now, "department": dept, "category": cat, "legal_act": act, "raw_issue": text})
        with open(self.grievance_file, "w", encoding="utf-8") as f:
            json.dump(cases, f, ensure_ascii=False, indent=4)

        self.speak(f"Legal notice number {cid} QR code seal ke sath generate ho gaya hai.")

    def process_voice(self, text):
        if not text:
            return

        cleaned = text.replace("₹", "").replace(",", "").replace("taka", "").replace("rupiya", "").strip()
        t_low = text.lower()

        # 1. Emergency Live SOS
        if any(w in t_low for w in ["bachao", "madad", "help", "police", "khatra", "emergency"]):
            self.trigger_sos_alert()
            return

        # 2. Cyber Fraud
        if any(w in t_low for w in ["otp", "lottery", "password", "inaam", "bank band"]):
            os.system('termux-vibrate -f -d 1500')
            self.speak("Savdhan! Yeh fraud call hai. Koi secret code na dein.")
            return

        # 3. Grievances
        if any(w in t_low for w in ["pf", "claim", "reject", "katauti"]):
            self.file_grievance("PF", text)
            return
        elif any(w in t_low for w in ["ration", "khorak", "angootha", "galla"]):
            self.file_grievance("RATION", text)
            return
        elif any(w in t_low for w in ["bijli", "meter", "batti", "bill"]):
            self.file_grievance("BIJLI", text)
            return
        elif any(w in t_low for w in ["thekedaar", "mazdoori", "vetan", "salary"]):
            self.file_grievance("LABOR", text)
            return

        words = cleaned.split()
        amt_match = re.search(r'(\d+)', cleaned)
        amt = amt_match.group(1) if amt_match else None

        # 4. Payment to ANY Contact
        if any(w in t_low for w in ["bhejo", "pay", "transfer", "dalo", "bhejna"]) and amt:
            person = "raju"
            for i, w in enumerate(words):
                if w.lower() in ["ko", "pe", "par"] and i > 0:
                    person = words[i-1]
                    break
            self.trigger_upi_payment(person, amt)
            return

        # 5. Ledger
        if amt:
            person = "sahil"
            for i, w in enumerate(words):
                if w.lower() in ["ko", "ka", "ke"] and i > 0:
                    person = words[i-1]
                    break
            self.add_entry(person, amt, text)
            return

        self.speak("Aadesh samajh nahi aaya, kripya dobara bolein.")

if __name__ == "__main__":
    munshi = BharatJanMunshi()
    voice_command = munshi.listen("Bharat Jan-Munshi sun raha hai...")
    munshi.process_voice(voice_command)
