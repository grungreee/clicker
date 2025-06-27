import globals
import threading
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QFrame, QTabWidget, QLabel,
                             QSizePolicy, QLineEdit)
from PyQt5.QtCore import Qt, QSize, QTimer
from utils.file_operations import write_account_data, hash_password, check_all
from utils.requests import authenticate, do_request
from utils.handle_signals import show_info, show_error, update_account_tab, start_sync, stop_sync


class Clicker(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(lambda: threading.Thread(target=self.sync_data).start())  # type: ignore

        self.coins_label = None
        self.per_sec_label = None
        self.total_label = None
        self.username_entry = None
        self.password_entry = None

        self.camel_coins: int = 0
        self.server_clicks: int = 0
        self.local_clicks: int = 0
        self.delta_clicks: int = 0

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
        self.create_upgrades_tab()
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

        stats_layout = QVBoxLayout()
        stats_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        content_layout.addLayout(stats_layout, 1)

        self.total_label = QLabel("Total Clicks: 0")
        self.total_label.setAlignment(Qt.AlignLeft)
        stats_layout.addWidget(self.total_label)

        self.coins_label = QLabel("Total CamelCoins: 0 🪙")
        self.coins_label.setAlignment(Qt.AlignLeft)
        stats_layout.addWidget(self.coins_label)

        self.per_sec_label = QLabel("CamelCoins per seconds: 0 🪙")
        self.per_sec_label.setAlignment(Qt.AlignLeft)
        stats_layout.addWidget(self.per_sec_label)

        clicker_layout = QVBoxLayout()
        clicker_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.addLayout(clicker_layout, 1)

        click_button = QPushButton()
        click_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        click_button.clicked.connect(self.on_click)  # type: ignore
        click_button.setIcon(QIcon("assets/camel.png"))
        click_button.setIconSize(QSize(100, 100))
        clicker_layout.addWidget(click_button)

        self.tab_widget.addTab(clicker_widget, "Clicker")

    def create_upgrades_tab(self) -> None:
        upgrades_widget = QWidget()

        main_layout = QVBoxLayout(upgrades_widget)
        main_layout.setContentsMargins(10, 10, 5, 5)
        upgrades_widget.setLayout(main_layout)

        title_label = QLabel("Upgrades")
        title_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title_label)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 10, 5, 5)
        main_layout.addLayout(content_layout)

        multiplayer_frame = QFrame()
        multiplayer_frame.setObjectName("frame")
        multiplayer_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(multiplayer_frame, 1)

        multiplayer_layout = QVBoxLayout(multiplayer_frame)
        multiplayer_label = QLabel("Multiplayer Upgrades")
        multiplayer_label.setAlignment(Qt.AlignLeft)
        multiplayer_layout.addWidget(multiplayer_label)

        # Пример апгрейдов для multiplayer
        multiplayer_upgrades = [
            {"name": "Double Coins", "cost": 50},
            {"name": "Triple Coins", "cost": 150}
        ]

        for upgrade in multiplayer_upgrades:
            button = QPushButton(f'{upgrade["name"]} - {upgrade["cost"]} 🪙')
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.clicked.connect(lambda _, u=upgrade: self.buy_upgrade(u))
            multiplayer_layout.addWidget(button)

        clicks_frame = QFrame()
        clicks_frame.setObjectName("frame")
        clicks_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(clicks_frame, 1)

        clicks_layout = QVBoxLayout(clicks_frame)
        clicks_label = QLabel("Clicks per Second")
        clicks_label.setAlignment(Qt.AlignLeft)
        clicks_layout.addWidget(clicks_label)

        # Пример апгрейдов для автокликов
        click_upgrades = [
            {"name": "Auto Clicker I", "cost": 100},
            {"name": "Auto Clicker II", "cost": 250}
        ]

        for upgrade in click_upgrades:
            button = QPushButton(f'{upgrade["name"]} - {upgrade["cost"]} 🪙')
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.clicked.connect(lambda _, u=upgrade: self.buy_upgrade(u))
            clicks_layout.addWidget(button)

        self.tab_widget.addTab(upgrades_widget, "Upgrades")

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
            username_label = QLabel(f"Logged in as: {globals.account["username"]}")
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
        self.local_clicks += 1
        self.delta_clicks += 1
        self.camel_coins += 1

        self.total_label.setText(f"Total Clicks: {self.local_clicks}")
        self.coins_label.setText(f"Total CamelCoins: {self.camel_coins} 🪙")

    def sync_data(self, background: bool = True) -> None:
        data: dict = {
            "user": globals.account,
            "stats": {
                "delta_clicks": self.delta_clicks
            }
        }

        self.delta_clicks = 0
        response: tuple[int, dict] = do_request("sync_data", data, background=background)

        if response[0] == 200:
            server_stats: dict = response[1]

            self.server_clicks = server_stats["clicks"] + self.delta_clicks
            self.local_clicks = self.server_clicks

            self.camel_coins = server_stats["camel_coins"] + self.delta_clicks

            self.total_label.setText(f"Total Clicks: {self.local_clicks}")
            self.coins_label.setText(f"Total CamelCoins: {self.camel_coins} 🪙")

    def login(self) -> None:
        def on_success(_=None) -> None:
            globals.account = {"username": username, "password": password}
            write_account_data(username, password)
            self.sync_data(background=False)
            start_sync()

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
        stop_sync()
        write_account_data(None, None)
        globals.account = None
        update_account_tab()

    def closeEvent(self, event):
        if globals.account is not None:
            self.sync_data(background=False)
        super().closeEvent(event)

