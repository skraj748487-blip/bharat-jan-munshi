#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd ~/mission

# बैकग्राउंड वेब सर्वर चालू रखें
pgrep -f "http.server 8080" || nohup python -m http.server 8080 > server.log 2>&1 &

while true; do
    # नोटिफिकेशन बार हमेशा एक्टिव
    termux-notification \
      --id 101 \
      --title "🇮🇳 भारत जन-मुंशी OS (लाइव)" \
      --content "मुंशी तैयार है - आवाज़ देने के लिए यहाँ टैप करें" \
      --priority max \
      --ongoing \
      --action "python ~/mission/brain.py"

    # हर 10 सेकंड में सर्विस को ज़िंदा रखना
    sleep 10
done
