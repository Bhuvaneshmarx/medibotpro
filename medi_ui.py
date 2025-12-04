from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from medical_db import analyze_symptoms
from hospital_finder import open_hospitals_near, auto_detect_and_open

class MediBotUI(QMainWindow):
    def __init__(self, ai_engine, voice_engine):
        super().__init__()

        self.ai_engine = ai_engine
        self.voice_engine = voice_engine

        self.current_language = "English"
        self.voice_enabled = True

        self.setWindowTitle("MediBot Pro - AI Health Assistant")
        self.setGeometry(200, 100, 1000, 600)
        self.setStyleSheet("background-color: #E3F2FD;")

        self.layout = QHBoxLayout()
        self.left_menu()
        self.chat_area()

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    # ---------- LEFT SIDE ----------
    def left_menu(self):
        left = QFrame()
        left.setFixedWidth(280)
        left.setStyleSheet("background-color: #1976d2; border-right: 2px solid #0d47a1;")

        logo = QLabel("MediBot Pro")
        logo.setFont(QFont("Arial", 18, QFont.Bold))
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("color: white; padding: 20px;")

        desc = QLabel("AI Health Assistant\nLanguages: EN | HI | TA | TE")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #e3f2fd; font-size: 13px; padding-bottom: 20px;")

        # Language selector
        lang_label = QLabel("Preferred Language:")
        lang_label.setStyleSheet("color: white; font-size: 13px; padding-left: 10px;")

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Hindi", "Tamil", "Telugu"])
        self.lang_combo.setCurrentText("English")
        self.lang_combo.currentTextChanged.connect(self.change_language)
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background-color: #bbdefb;
                padding: 5px;
                border-radius: 5px;
                margin: 5px 10px;
            }
        """)

        # Voice toggle
        self.voice_checkbox = QCheckBox("Speak Responses")
        self.voice_checkbox.setChecked(True)
        self.voice_checkbox.stateChanged.connect(self.toggle_voice)
        self.voice_checkbox.setStyleSheet("color: #e3f2fd; font-size: 13px; padding-left: 10px;")

        # Offline Symptom Check button
        self.symptom_btn = QPushButton("🔎 Symptom Check (Offline DB)")
        self.symptom_btn.clicked.connect(self.run_offline_symptom_check)
        self.symptom_btn.setStyleSheet("""
            QPushButton {
                background-color: #1565c0;
                color: white;
                margin: 10px;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #0d47a1;
            }
        """)

        # Hospital finder button
        self.hospital_btn = QPushButton("🏥 Find Nearby Hospital")
        self.hospital_btn.clicked.connect(self.open_hospital_finder)
        self.hospital_btn.setStyleSheet("""
            QPushButton {
                background-color: #1565c0;
                color: white;
                margin: 10px;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #0d47a1;
            }
        """)

        info_label = QLabel(
            "Disclaimer:\n"
            "• MediBot Pro is NOT a real doctor.\n"
            "• For serious or emergency cases,\n"
            "  visit a hospital or call emergency\n"
            "  services immediately.\n"
            "• Offline Symptom Check is only\n"
            "  general information, not diagnosis."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #e3f2fd; font-size: 11px; padding: 10px;")

        vbox = QVBoxLayout()
        vbox.addWidget(logo)
        vbox.addWidget(desc)
        vbox.addWidget(lang_label)
        vbox.addWidget(self.lang_combo)
        vbox.addWidget(self.voice_checkbox)
        vbox.addWidget(self.symptom_btn)
        vbox.addWidget(self.hospital_btn)
        vbox.addWidget(info_label)
        vbox.addStretch()

        left.setLayout(vbox)
        self.layout.addWidget(left)

    # ---------- RIGHT SIDE ----------
    def chat_area(self):
        right = QFrame()
        right.setStyleSheet("background-color: #f5faff;")
        vbox = QVBoxLayout(right)

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.setStyleSheet("""
            background-color: white;
            font-size: 14px;
            border: 1px solid #90caf9;
            padding: 10px;
        """)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Describe your symptoms or ask about a medicine...")
        self.input_box.setStyleSheet("""
            font-size: 14px; padding: 10px;
            border-radius: 5px;
            border: 2px solid #90caf9;
        """)
        self.input_box.returnPressed.connect(self.send_message)

        send_btn = QPushButton("➤")
        send_btn.setFixedSize(60, 45)
        send_btn.setStyleSheet("""
            background-color: #1976d2;
            color: white;
            border-radius: 10px;
            font-size: 22px;
        """)
        send_btn.clicked.connect(self.send_message)

        hbox = QHBoxLayout()
        hbox.addWidget(self.input_box)
        hbox.addWidget(send_btn)

        vbox.addWidget(self.chat_box)
        vbox.addLayout(hbox)

        self.layout.addWidget(right)

        self.append_message("MediBot Pro",
                            "Hello! I'm your AI health assistant.\n"
                            "You can:\n"
                            "• Type symptoms (e.g., 'I have headache and fever').\n"
                            "• Click 'Symptom Check (Offline DB)' for quick info.\n"
                            "• Click 'Find Nearby Hospital' to open hospitals in Google Maps.\n"
                            "I only provide general information, not a medical diagnosis.")

    # ---------- CHAT HELPERS ----------
    def append_message(self, sender, msg):
        color = "#0d47a1" if sender == "MediBot Pro" else "#1e88e5"
        formatted = "<p><b style='color:%s'>%s:</b> %s</p>" % (color, sender, msg)
        self.chat_box.append(formatted)

    def change_language(self, lang_text):
        self.current_language = lang_text
        self.voice_engine.set_language(lang_text)
        self.append_message("MediBot Pro", "Language set to %s." % lang_text)

    def toggle_voice(self, state):
        self.voice_enabled = (state == Qt.Checked)
        status = "enabled" if self.voice_enabled else "disabled"
        self.append_message("MediBot Pro", "Voice output %s." % status)

    # ---------- OFFLINE SYMPTOM CHECK ----------
    def run_offline_symptom_check(self):
        text, ok = QInputDialog.getText(
            self,
            "Offline Symptom Check",
            "Describe your main symptoms (few words):",
        )
        if not ok or not text.strip():
            return

        user_text = text.strip()
        self.append_message("You (Offline Symptom Check)", user_text)

        result_html = analyze_symptoms(user_text)
        if result_html:
            self.append_message("MediBot Pro (Offline DB)", result_html)
        else:
            self.append_message(
                "MediBot Pro (Offline DB)",
                "I could not match these symptoms in my small offline database.\n"
                "You can still ask me in the main chat box for more detailed guidance."
            )

    # ---------- HOSPITAL FINDER ----------
    def open_hospital_finder(self):
        choice = QMessageBox.question(
            self,
            "Hospital Finder",
            "Do you want to auto-detect your approximate location using internet?\n"
            "(If you choose 'No', you can enter city or pincode manually.)",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )

        if choice == QMessageBox.Cancel:
            return

        if choice == QMessageBox.Yes:
            msg = auto_detect_and_open()
            self.append_message("MediBot Pro", msg)
        else:
            # Manual city / pincode input
            location, ok = QInputDialog.getText(
                self,
                "Manual Location",
                "Enter your city name or pincode:",
            )
            if not ok or not location.strip():
                return
            msg = open_hospitals_near(location.strip())
            self.append_message("MediBot Pro", msg)

    # ---------- MAIN SEND ----------
    def send_message(self):
        user_msg = self.input_box.text().strip()
        if user_msg == "":
            return

        self.append_message("You", user_msg)
        self.input_box.clear()

        # First, show offline suggestion if any
        offline_result = analyze_symptoms(user_msg)
        if offline_result:
            self.append_message("MediBot Pro (Offline DB)", offline_result)

        # Then call AI engine
        self.append_message("MediBot Pro", "Thinking...")
        QApplication.processEvents()

        reply = self.ai_engine.get_response(user_msg, self.current_language)
        self.append_message("MediBot Pro", reply)

        if self.voice_enabled:
            self.voice_engine.speak(reply)


def start_ui(ai_engine, voice_engine):
    app = QApplication(sys.argv)
    window = MediBotUI(ai_engine, voice_engine)
    window.show()
    sys.exit(app.exec_())
