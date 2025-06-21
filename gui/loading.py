from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QSize
import globals


def show_spinner_overlay() -> QWidget:
    overlay = QWidget(globals.window)
    overlay.setObjectName("spinnerOverlay")
    overlay.setStyleSheet("""
        QWidget#spinnerOverlay {
            background-color: rgba(0, 0, 0, 100);
        }
    """)
    overlay.setGeometry(globals.window.rect())
    overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
    overlay.setAttribute(Qt.WA_NoSystemBackground)
    overlay.setWindowFlags(Qt.SubWindow)

    spinner = QLabel(overlay)
    movie = QMovie("assets/spinner.gif")
    movie.setScaledSize(QSize(100, 100))
    spinner.setMovie(movie)
    movie.start()

    spinner.adjustSize()
    spinner.move(
        (overlay.width() - spinner.width()) // 2,
        (overlay.height() - spinner.height()) // 2
    )

    overlay.raise_()
    overlay.show()

    globals.spinner = overlay


def close_spinner_overlay() -> None:
    if globals.spinner is not None:
        globals.spinner.close()

