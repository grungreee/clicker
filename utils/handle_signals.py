import globals
from gui.dialogs import show_error_dialog
from gui.loading import show_spinner_overlay, close_spinner_overlay
from PyQt5.QtCore import pyqtSignal, QObject


class RequestSignals(QObject):
    error_signal = pyqtSignal(str, str)
    response_signal = pyqtSignal(int, dict)
    show_spinner_signal = pyqtSignal()
    close_spinner_signal = pyqtSignal()


def handle_signals() -> None:
    globals.request_signals.error_signal.connect(show_error_dialog)
    globals.request_signals.show_spinner_signal.connect(show_spinner_overlay)
    globals.request_signals.close_spinner_signal.connect(close_spinner_overlay)


def show_error(title: str, text: str) -> None:
    globals.request_signals.error_signal.emit(title, text)


def show_spinner() -> None:
    globals.request_signals.show_spinner_signal.emit()


def close_spinner() -> None:
    globals.request_signals.close_spinner_signal.emit()

