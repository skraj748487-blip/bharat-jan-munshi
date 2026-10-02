#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd ~/mission

# परमानेंट क्विक एक्शन नोटिफिकेशन
termux-notification \
  --id 101 \
  --title "🇮🇳 भारत जन-मुंशी OS" \
  --content "आवाज़ से आदेश देने के लिए यहाँ टैप करें" \
  --priority high \
  --ongoing \
  --action "python ~/mission/brain.py"
