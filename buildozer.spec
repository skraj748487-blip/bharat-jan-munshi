[app]
title = Bharat Jan-Munshi
package.name = bharatjanmunshi
package.domain = org.sahil.munshi
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
requirements = python3,kivy,reportlab,qrcode
orientation = portrait

android.permissions = RECORD_AUDIO,SEND_SMS,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,READ_CONTACTS,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,VIBRATE,INTERNET
android.api = 33
android.minapi = 24
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
