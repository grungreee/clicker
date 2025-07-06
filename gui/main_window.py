import globals
import threading
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QFrame, QTabWidget, QLabel,
                             QSizePolicy, QLineEdit)
from PyQt5.QtCore import Qt, QSize, QTimer
from utils.file_operations import write_account_data, hash_password, check_all
from utils.requests import authenticate, do_request
from utils.handle_signals import (show_info, show_error, update_account_tab,
                                  start_sync, stop_sync, load_upgrades)


class Clicker(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.sync_timer_callback)  # type: ignore

        self.prestige = None
        self.coins_label_clicker = None
        self.coins_label_upgrades = None
        self.per_sec_label = None
        self.total_label = None
        self.username_entry = None
        self.password_entry = None
        self.clicks_layout = None
        self.multiplayer_layout = None
        
        self.syncing: bool = False
        
        self.camel_coins: int = 0

        self.server_clicks: int = 0
        self.local_clicks: int = 0
        self.delta_clicks: int = 0

        self.all_upgrades: dict = {}
        self.delta_upgrades: dict = {}
        self.local_upgrades: dict = {}
        self.server_upgrades: dict = {}

        self.setWindowIcon(QIcon("assets/camel.png"))
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

        with open('style.css', 'r', encoding='utf-8') as file:
            self.setStyleSheet(file.read())

    def sync_timer_callback(self):
        if (self.delta_upgrades or self.delta_clicks) and not self.syncing:
            threading.Thread(target=self.sync_data).start()

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

        self.coins_label_clicker = QLabel("CamelCoins: 0 🪙")
        self.coins_label_clicker.setAlignment(Qt.AlignLeft)
        stats_layout.addWidget(self.coins_label_clicker)

        self.per_sec_label = QLabel("CamelCoins per seconds: 0 🪙")
        self.per_sec_label.setAlignment(Qt.AlignLeft)
        stats_layout.addWidget(self.per_sec_label)

        self.prestige = QLabel("Prestige: 0")
        self.prestige.setAlignment(Qt.AlignLeft)
        stats_layout.addWidget(self.prestige)

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
        self.create_upgrades_tab_content(upgrades_widget)
        self.tab_widget.addTab(upgrades_widget, "Upgrades")

    def create_upgrades_tab_content(self, upgrades_widget: QWidget) -> None:
        main_layout = QVBoxLayout(upgrades_widget)
        main_layout.setContentsMargins(10, 10, 5, 5)
        upgrades_widget.setLayout(main_layout)

        upper_layout = QHBoxLayout()
        upper_layout.setContentsMargins(0, 5, 0, 0)
        main_layout.addLayout(upper_layout)

        title_label = QLabel("Upgrades")
        title_label.setAlignment(Qt.AlignLeft)
        upper_layout.addWidget(title_label)

        self.coins_label_upgrades = QLabel(f"CamelCoins: {self.camel_coins} 🪙")
        self.coins_label_upgrades.setAlignment(Qt.AlignRight)
        upper_layout.addWidget(self.coins_label_upgrades)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 10, 5, 5)
        main_layout.addLayout(content_layout)

        multiplayer_frame = QFrame()
        multiplayer_frame.setObjectName("frame")
        multiplayer_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(multiplayer_frame, 1)

        self.multiplayer_layout = QVBoxLayout(multiplayer_frame)
        multiplayer_label = QLabel("Multiplayer Upgrades")
        multiplayer_label.setAlignment(Qt.AlignLeft)
        self.multiplayer_layout.addWidget(multiplayer_label)

        clicks_frame = QFrame()
        clicks_frame.setObjectName("frame")
        clicks_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(clicks_frame, 1)

        self.clicks_layout = QVBoxLayout(clicks_frame)
        clicks_label = QLabel("Clicks per Second")
        clicks_label.setAlignment(Qt.AlignLeft)
        self.clicks_layout.addWidget(clicks_label)

        if globals.account is not None:
            threading.Thread(target=lambda: self.sync_data(background=False)).start()

    def load_upgrades(self, user_upgrades: dict, all_upgrades: dict) -> None:
        self.clear_layout(self.clicks_layout)
        self.clear_layout(self.multiplayer_layout)

        for id_, upgrade in all_upgrades.items():
            layout = QHBoxLayout()
            layout.setSpacing(10)

            button = QPushButton(f"{upgrade["name"]}"
                                 f"{f" ({user_upgrades[id_]} obtained)" if id_ in user_upgrades else ""}")
            button.clicked.connect(lambda _, upgrade_id=id_: self.buy_upgrade(upgrade_id))  # type: ignore
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            label = QLabel(f"{upgrade['cost']} 🪙")

            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label.setFixedWidth(130)
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

            layout.addWidget(button)
            layout.addWidget(label)

            if upgrade["type"] == "click":
                self.clicks_layout.addLayout(layout)
            elif upgrade["type"] == "auto":
                self.multiplayer_layout.addLayout(layout)

    def update_upgrades_tab(self) -> None:
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Upgrades":
                upgrades_widget = self.tab_widget.widget(i)

                old_layout = upgrades_widget.layout()
                if old_layout is not None:
                    self._delete_layout(old_layout)

                self.create_upgrades_tab_content(upgrades_widget)
                break

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

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def _delete_layout(self, layout: QVBoxLayout) -> None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._delete_layout(child.layout())
        QWidget().setLayout(layout)

    def on_click(self) -> None:
        self.delta_clicks += 1
        self.local_clicks += 1
        self.camel_coins += 1

        self.total_label.setText(f"Total Clicks: {self.local_clicks}")
        self.coins_label_clicker.setText(f"CamelCoins: {self.camel_coins} 🪙")
        self.coins_label_upgrades.setText(f"CamelCoins: {self.camel_coins} 🪙")

    def sync_data(self, background: bool = True) -> None:
        self.syncing = True

        data: dict = {
            "user": globals.account,
            "stats": {
                "delta_clicks": self.delta_clicks,
                "delta_upgrades": self.delta_upgrades
            }
        }

        self.delta_clicks = 0
        self.delta_upgrades = {}

        print("Syncing data...")

        response: tuple[int, dict] = do_request("sync_data", data, background=background)

        if response[0] == 200:
            server_stats: dict = response[1]

            self.server_clicks = server_stats["clicks"]
            self.local_clicks = self.server_clicks + self.delta_clicks

            self.all_upgrades = server_stats["all_upgrades"]
            self.server_upgrades = server_stats["user_upgrades"]

            self.local_upgrades = self.server_upgrades.copy()
            for upgrade_id, count in self.delta_upgrades.items():
                self.local_upgrades[upgrade_id] = self.local_upgrades.get(upgrade_id, 0) + count

            self.camel_coins = server_stats["camel_coins"] + self.delta_clicks

            self.total_label.setText(f"Total Clicks: {self.local_clicks}")
            self.coins_label_clicker.setText(f"CamelCoins: {self.camel_coins} 🪙")
            self.coins_label_upgrades.setText(f"CamelCoins: {self.camel_coins} 🪙")
            load_upgrades(self.local_upgrades, self.all_upgrades)
            print("Data synced successfully!")

        self.syncing = False

    def buy_upgrade(self, upgrade_id: str) -> None:
        cost = self.all_upgrades[upgrade_id]["cost"]
        if cost <= self.camel_coins:
            self.delta_upgrades[upgrade_id] = self.delta_upgrades.get(upgrade_id, 0) + 1
            self.local_upgrades[upgrade_id] = self.local_upgrades.get(upgrade_id, 0) + 1
            self.camel_coins -= cost

            self.coins_label_clicker.setText(f"CamelCoins: {self.camel_coins} 🪙")
            self.coins_label_upgrades.setText(f"CamelCoins: {self.camel_coins} 🪙")
            load_upgrades(self.local_upgrades, self.all_upgrades)
        else:
            show_error("Warn", "Not enough CamelCoins 🪙 to buy this upgrade")

    def login(self) -> None:
        def on_success(_=None) -> None:
            globals.account = {"username": username, "password": password}
            write_account_data(username, password)
            self.sync_data(background=False)
            start_sync(4000)

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
