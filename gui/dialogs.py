from PyQt5.QtWidgets import QMessageBox


def show_confirm_dialog(title: str, message: str) -> bool:
    dialog = QMessageBox()
    dialog.setWindowTitle(title)
    dialog.setText(message)
    dialog.setIcon(QMessageBox.Question)
    dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    dialog.setDefaultButton(QMessageBox.No)

    return dialog.exec_() == QMessageBox.Yes


def show_error_dialog(title: str, message: str) -> None:
    dialog = QMessageBox()
    dialog.setWindowTitle(title)
    dialog.setText(message)
    dialog.setIcon(QMessageBox.Critical)
    dialog.setStandardButtons(QMessageBox.Ok)
    dialog.exec_()
