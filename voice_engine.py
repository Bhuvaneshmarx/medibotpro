import pyttsx3

class VoiceEngine:
    def __init__(self, language_name: str = "English"):
        self.engine = pyttsx3.init()
        self.language_name = language_name
        self._select_voice()

    def _select_voice(self):
        """
        Try to select an Indian male English voice.
        Actual voices depend on Windows installed TTS voices.
        """
        voices = self.engine.getProperty("voices")
        selected = None

        for v in voices:
            name = (v.name or "").lower()
            id_ = (v.id or "").lower()
            if ("india" in name or "en-in" in id_) and ("male" in name or "male" in id_):
                selected = v
                break

        if not selected:
            # Fallback: any Indian English voice
            for v in voices:
                name = (v.name or "").lower()
                id_ = (v.id or "").lower()
                if "india" in name or "en-in" in id_:
                    selected = v
                    break

        # Final fallback: default voice
        if selected:
            self.engine.setProperty("voice", selected.id)

        self.engine.setProperty("rate", 170)  # speaking speed

    def set_language(self, language_name: str):
        """
        Currently we always use the same TTS voice,
        but this method allows future expansion.
        """
        self.language_name = language_name
        # If later you add specific regional voices, change them here.
        self._select_voice()

    def speak(self, text: str):
        try:
            self.engine.stop()
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print("TTS error:", e)
5
