from ai_engine import MediAI
from voice_engine import VoiceEngine
from medi_ui import start_ui

if __name__ == "__main__":
    # Create AI + Voice engines
    ai = MediAI()                   # Uses API_KEY from ai_engine.py
    voice = VoiceEngine("English")  # Default: English, Indian male

    # Launch UI
    start_ui(ai, voice)
