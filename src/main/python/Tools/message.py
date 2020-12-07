from PyQt5.QtWidgets import QMessageBox


def detailed_message(self, icon, title, text, detailed_text):
    msgBox = QMessageBox(self)
    msgBox.setIcon(icon)
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    msgBox.setDetailedText(detailed_text)
    msgBox.exec()
