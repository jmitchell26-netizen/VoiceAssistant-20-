import sys
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox
from app.main_window import MainWindow

def show_error_message(error_text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText("Error Starting Application")
    msg.setInformativeText(error_text)
    msg.setWindowTitle("Error")
    msg.exec()

def main():
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Voice Assistant")
        app.setOrganizationName("VoiceAssistant")
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
    except Exception as e:
        error_text = f"An error occurred:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(error_text)
        if QApplication.instance():
            show_error_message(error_text)
        sys.exit(1)

if __name__ == "__main__":
    main()