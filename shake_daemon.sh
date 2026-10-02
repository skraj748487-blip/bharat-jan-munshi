#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd ~/mission

# सेंसर से शेक (हिलाने) को पकड़ना
termux-sensor -s "linear_acceleration" -d 200 | while read -r line; do
    # जब फोन को तेजी से हिलाया जाए
    val=$(echo "$line" | grep -o '"values": \[[^]]*\]' | head -n 1)
    if [ -n "$val" ]; then
        # फोर्स चेक
        termux-sensor -c
        termux-vibrate -d 300
        python brain.py
        sleep 3
    fi
done
