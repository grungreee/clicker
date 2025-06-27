from PyQt5.QtWidgets import QMessageBox


class DefaultDialog(QMessageBox):
    def __init__(self, title: str, text: str) -> None:
        super().__init__()

        self.setWindowTitle(title)
        self.setText(text)


def show_confirm_dialog(title: str, message: str) -> bool:
    dialog = DefaultDialog(title, message)
    dialog.setIcon(QMessageBox.Question)
    dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    dialog.setDefaultButton(QMessageBox.No)

    return dialog.exec_() == QMessageBox.Yes


def show_error_dialog(title: str, message: str) -> None:
    dialog = DefaultDialog(title, message)
    dialog.setIcon(QMessageBox.Critical)
    dialog.setStandardButtons(QMessageBox.Ok)
    dialog.exec_()


def show_info_dialog(title: str, message: str) -> None:
    dialog = DefaultDialog(title, message)
    dialog.setIcon(QMessageBox.Information)
    dialog.setStandardButtons(QMessageBox.Ok)
    dialog.exec_()
