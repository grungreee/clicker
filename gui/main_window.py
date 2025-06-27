import globals
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QFrame, QTabWidget, QLabel,
                             QSizePolicy, QLineEdit)
from PyQt5.QtCore import Qt, QSize
from utils.file_operations import write_account_data, hash_password, check_all
from utils.requests import authenticate
from utils.handle_signals import show_info, show_error, update_account_tab


class Clicker(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.total_label = None
        self.clicks: int = 0
        self.username_entry = None
        self.password_entry = None

        self.setWindowTitle("Camel Clicker")
        self.setGeometry(100, 100, 700, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.on_tab_changed)  # type: ignore
        self.tab_widget.setObjectName("tab_widget")

        self.create_clicker_tab()
        self.create_account_tab()

        main_layout.addWidget(self.tab_widget)
        self.load_stylesheet_from_file()

    def load_stylesheet_from_file(self) -> None:
        try:
            with open('style.css', 'r', encoding='utf-8') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("style.css file is not found")

    def on_tab_changed(self, index: int) -> None:
        if self.tab_widget.tabText(index) == "Account":
            update_account_tab()

    def create_clicker_tab(self):
        clicker_widget = QWidget()

        main_layout = QVBoxLayout(clicker_widget)
        clicker_widget.setLayout(main_layout)

        title_frame = QFrame()
        title_frame.setObjectName("main_frame")
        main_layout.addWidget(title_frame, 1)

        title_layout = QVBoxLayout(title_frame)

        title_label = QLabel("Camel Clicker")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)

        content_frame = QFrame()
        content_frame.setObjectName("main_frame")
        main_layout.addWidget(content_frame, 3)

        content_layout = QHBoxLayout(content_frame)

        stats_frame = QFrame()
        stats_frame.setObjectName("frame")
        content_layout.addWidget(stats_frame, 1)

        stats_layout = QVBoxLayout(stats_frame)

        stats_label = QLabel("Stats")
        stats_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(stats_label)
        stats_layout.addStretch()

        self.total_label = QLabel("Total Clicks: 0")
        self.total_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(self.total_label)

        coins_label = QLabel("Total CamelCoins: 0")
        coins_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(coins_label)

        per_sec_label = QLabel("CamelCoins per seconds: 0")
        per_sec_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(per_sec_label)
        stats_layout.addStretch()

        clicker_frame = QFrame()
        clicker_frame.setObjectName("frame")
        content_layout.addWidget(clicker_frame, 1)

        clicker_layout = QVBoxLayout(clicker_frame)
        clicker_layout.setContentsMargins(10, 10, 10, 10)

        click_button = QPushButton()
        click_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        click_button.clicked.connect(self.on_click)  # type: ignore
        click_button.setIcon(QIcon("assets/camel.png"))
        click_button.setIconSize(QSize(100, 100))
        clicker_layout.addWidget(click_button)

        self.tab_widget.addTab(clicker_widget, "Clicker")

    def create_account_tab(self) -> None:
        account_widget = QWidget()
        self.create_account_tab_content(account_widget)
        self.tab_widget.addTab(account_widget, "Account")

    def create_account_tab_content(self, account_widget: QWidget) -> None:
        main_layout = QVBoxLayout(account_widget)
        account_widget.setLayout(main_layout)

        title_label = QLabel("Account")
        title_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title_label)

        main_layout.addStretch()
        account_layout = QVBoxLayout()
        account_layout.setAlignment(Qt.AlignHCenter)
        main_layout.addLayout(account_layout)

        account_frame = QFrame()
        account_frame.setObjectName("frame")
        account_frame.setFixedSize(300, 150)
        account_layout.addWidget(account_frame)
        main_layout.addStretch()

        account_layout = QVBoxLayout(account_frame)
        account_layout.setAlignment(Qt.AlignCenter)

        if globals.account is None:
            self.username_entry = QLineEdit()
            self.username_entry.setPlaceholderText("Username")
            account_layout.addWidget(self.username_entry)

            self.password_entry = QLineEdit()
            self.password_entry.setPlaceholderText("Password")
            self.password_entry.setEchoMode(QLineEdit.Password)
            account_layout.addWidget(self.password_entry)

            buttons_layout = QHBoxLayout()
            account_layout.addLayout(buttons_layout)

            login_button = QPushButton("Login")
            login_button.clicked.connect(self.login)  # type: ignore
            buttons_layout.addWidget(login_button)

            register_button = QPushButton("Register")
            register_button.clicked.connect(self.register)  # type: ignore
            buttons_layout.addWidget(register_button)
        else:
            username_label = QLabel(f"Logged in as: {globals.account[0]}")
            username_label.setAlignment(Qt.AlignCenter)
            account_layout.addWidget(username_label)

            logout_button = QPushButton("Logout")
            logout_button.clicked.connect(self.logout)  # type: ignore
            account_layout.addWidget(logout_button)

    def update_account_tab(self) -> None:
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Account":
                account_widget = self.tab_widget.widget(i)

                old_layout = account_widget.layout()
                if old_layout is not None:
                    self._delete_layout(old_layout)

                self.create_account_tab_content(account_widget)
                break

    def _delete_layout(self, layout: QVBoxLayout) -> None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._delete_layout(child.layout())
        QWidget().setLayout(layout)

    def on_click(self) -> None:
        self.clicks += 1
        self.total_label.setText(f"Total Clicks: {self.clicks}")

    def login(self) -> None:
        def on_success(_=None) -> None:
            globals.account = (username, password)
            write_account_data(username, password)

            show_info("Info", "Login successful!")
            update_account_tab()

        username: str = self.username_entry.text()
        password: str = self.password_entry.text()

        status: bool | str = check_all(username, password)

        if status is True:
            password = hash_password(password)
            authenticate("login", username, password, on_success)
        else:
            show_error("Error", status)

    def register(self) -> None:
        def on_success(_=None) -> None:
            self.username_entry.setText("")
            self.password_entry.setText("")

            show_info("Info", "Registration successful!")

        username: str = self.username_entry.text()
        password: str = self.password_entry.text()

        status: bool | str = check_all(username, password)

        if status is True:
            password = hash_password(password)
            authenticate("register", username, password, on_success)
        else:
            show_error("Error", status)

    @staticmethod
    def logout() -> None:
        write_account_data(None, None)
        globals.account = None
        update_account_tab()
