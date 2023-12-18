from PySide6.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QPushButton
    )
class WindowInput(QMainWindow):
    def __init__(self, parent=None, text_instruction = None):
        super(WindowInput, self).__init__(parent)
        self.text_instruction = text_instruction
        self.input_result = None
        self.setup_ui()
        

    def setup_ui(self):
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(self.text_instruction)
        
        self.button_ok = QPushButton("Ok")
        self.button_ok.clicked.connect(self.get_input)
        
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.close)
        self.line_edit.setFixedSize(300, 30)
        self.setCentralWidget(self.line_edit)
        self.show()

    def get_input(self):
        self.input_result =  self.line_edit.text()
        self.accept()
    
    