import globals
from gui.dialogs import show_error_dialog, show_info_dialog
from gui.loading import show_spinner_overlay, close_spinner_overlay
from PyQt5.QtCore import pyqtSignal, QObject


class RequestSignals(QObject):
    error_signal = pyqtSignal(str, str)
    info_signal = pyqtSignal(str, str)
    show_spinner_signal = pyqtSignal()
    close_spinner_signal = pyqtSignal()
    update_account_signal = pyqtSignal()
    update_upgrades_signal = pyqtSignal()
    load_upgrades_signal = pyqtSignal(dict, dict)
    start_sync_signal = pyqtSignal(int)
    stop_sync_signal = pyqtSignal()


def handle_signals() -> None:
    globals.request_signals.error_signal.connect(show_error_dialog)
    globals.request_signals.info_signal.connect(show_info_dialog)
    globals.request_signals.show_spinner_signal.connect(show_spinner_overlay)
    globals.request_signals.close_spinner_signal.connect(close_spinner_overlay)
    globals.request_signals.update_account_signal.connect(globals.window.update_account_tab)
    globals.request_signals.update_upgrades_signal.connect(globals.window.update_upgrades_tab)
    globals.request_signals.load_upgrades_signal.connect(globals.window.load_upgrades)
    globals.request_signals.start_sync_signal.connect(globals.window.sync_timer.start)
    globals.request_signals.stop_sync_signal.connect(globals.window.sync_timer.stop)


def show_error(title: str, text: str) -> None:
    globals.request_signals.error_signal.emit(title, text)


def show_info(title: str, text: str) -> None:
    globals.request_signals.info_signal.emit(title, text)


def show_spinner() -> None:
    globals.request_signals.show_spinner_signal.emit()


def close_spinner() -> None:
    globals.request_signals.close_spinner_signal.emit()


def update_account_tab() -> None:
    globals.request_signals.update_account_signal.emit()


def update_upgrades_tab() -> None:
    globals.request_signals.update_upgrades_signal.emit()


def load_upgrades(user_upgrades: dict, all_upgrades: dict) -> None:
    globals.request_signals.load_upgrades_signal.emit(user_upgrades, all_upgrades)


def start_sync(delay: int) -> None:
    globals.request_signals.start_sync_signal.emit(delay)


def stop_sync() -> None:
    globals.request_signals.stop_sync_signal.emit()
