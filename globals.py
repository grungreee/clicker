import sys
from PyQt5.QtWidgets import QApplication
from utils.handle_signals import RequestSignals
from gui.main_window import Clicker

request_signals = RequestSignals()
app = QApplication(sys.argv)
window = Clicker()
spinner = None
