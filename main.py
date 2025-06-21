from PyQt5.QtWidgets import QApplication
from gui.main_window import Clicker
from utils.file_operations import check_data_file
import sys


def run_app() -> None:
    app = QApplication(sys.argv)

    window = Clicker()
    window.show()

    sys.exit(app.exec_())


def main() -> None:
    check_data_file()
    run_app()


if __name__ == "__main__":
    main()
