import sys
from PyQt5.QtWidgets import QApplication
from utils.handle_signals import RequestSignals
from gui.main_window import Clicker

account: dict[str, str] | None = None
app = QApplication(sys.argv)
window = Clicker()
request_signals = RequestSignals()
spinner = None
