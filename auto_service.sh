#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd ~/mission
pgrep -f "http.server 8080" || nohup python -m http.server 8080 > server.log 2>&1 &

while true; do
    termux-notification \
      --id 101 \
      --title "🇮🇳 Bharat Jan-Munshi OS" \
      --content "Aawaz se order dene ke liye yahan tap karein (Zero-Screen)" \
      --priority max \
      --ongoing \
      --action "python ~/mission/brain.py"
    sleep 3600
done
