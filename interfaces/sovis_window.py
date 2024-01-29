
from interfaces.base_window import BaseWindow
class SovisWindow(BaseWindow):
    def __init__(self, parent=None):
        super(SovisWindow, self).__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Sovis") 
        self.width = 800
        self.height = 600
    