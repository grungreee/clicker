import sys
from PyQt5.QtWidgets import QApplication
from utils.handle_signals import RequestSignals
from gui.main_window import Clicker

account: tuple[str, str] | None = None
request_signals = RequestSignals()
app = QApplication(sys.argv)
window = Clicker()
spinner = None
