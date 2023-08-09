from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

class ConfigWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ConfigWindow,self).__init__(parent)
        self.setWindowTitle("Config")
        self.setFixedSize(400, 400)
        #absolute window, cant close until finish config
        self.setWindowModality(Qt.WindowModal)
        self.show()
        
    

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ConfigWindow()
    sys.exit(app.exec())