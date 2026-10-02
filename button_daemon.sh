#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd ~/mission

# Volume Down event trap
termux-volume-keys listen | while read -r line; do
    if [[ "$line" == *"volume_down"* ]]; then
        termux-vibrate -d 200
        python brain.py
    fi
done
