from PySide6.QtWidgets import (
    QLineEdit,
    QPushButton,
    QApplication,
    QVBoxLayout,
    QDialog,
    QLabel
)
from PySide6.QtCore import Signal

class WindowInput(QDialog):
    input_completed = Signal(str)

    def __init__(self, parent=None, text_instruction=None):
        super(WindowInput, self).__init__(parent)
        self.text_instruction = text_instruction
        self.input_result = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Inserir Texto")
        self.label = QLabel(self.text_instruction)
        self.line_edit = QLineEdit()

        self.button_ok = QPushButton("Ok")
        self.button_ok.clicked.connect(self.get_input)
        self.button_cancel = QPushButton("Cancelar")
        self.button_cancel.clicked.connect(self.reject)
        self.line_edit.setFixedSize(500, 50)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button_ok)
        layout.addWidget(self.button_cancel)
        
    def get_input(self):
        self.input_result = self.line_edit.text()
        if self.input_result:
            self.input_completed.emit(self.input_result)
            self.accept()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = WindowInput()
    if window.exec() == QDialog.Accepted:
        print("Dialog Accepted")
    print("Continue with the rest of the code")
    app.exec()