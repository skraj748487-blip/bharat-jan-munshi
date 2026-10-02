import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

Window.clearcolor = (0.05, 0.08, 0.12, 1)

class MunshiApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        
        title = Label(
            text="🇮🇳 BHARAT JAN-MUNSHI OS",
            font_size='22sp',
            bold=True,
            size_hint=(1, 0.2),
            color=(1, 0.6, 0.2, 1)
        )
        layout.add_widget(title)

        self.btn = Button(
            text="🎙️\n\nआदेश दें\n(Tap to Speak)",
            font_size='24sp',
            bold=True,
            background_normal='',
            background_color=(0, 0.6, 0.4, 1),
            size_hint=(1, 0.6)
        )
        self.btn.bind(on_press=self.trigger_engine)
        layout.add_widget(self.btn)

        footer = Label(
            text="Nirmaata: Sahil Ahmad | 100% Offline Civic Tech",
            font_size='12sp',
            size_hint=(1, 0.2),
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(footer)
        return layout

    def trigger_engine(self, instance):
        os.system("python ~/mission/brain.py &")

if __name__ == "__main__":
    MunshiApp().run()
