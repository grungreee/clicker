from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QFrame, QTabWidget, QLabel,
                             QSizePolicy, QLineEdit)
from PyQt5.QtCore import Qt, QSize


class Clicker(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.total_label = None
        self.clicks: int = 0

        self.setWindowTitle("Camel Clicker")
        self.setGeometry(100, 100, 700, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tab_widget")

        self.create_clicker_tab()
        self.create_account_tab()
        self.create_upgrades_tab()
        self.create_leaderboard_tab()

        main_layout.addWidget(self.tab_widget)
        self.load_stylesheet_from_file()

    def load_stylesheet_from_file(self) -> None:
        try:
            with open('style.css', 'r', encoding='utf-8') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("style.css file is not found")

    def create_account_tab(self):
        account_widget = QWidget()

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

        username_entry = QLineEdit()
        username_entry.setPlaceholderText("Username")
        account_layout.addWidget(username_entry)

        password_entry = QLineEdit()
        password_entry.setPlaceholderText("Password")
        password_entry.setEchoMode(QLineEdit.Password)
        account_layout.addWidget(password_entry)

        buttons_layout = QHBoxLayout()
        account_layout.addLayout(buttons_layout)

        login_button = QPushButton("Login")
        buttons_layout.addWidget(login_button)

        register_button = QPushButton("Register")
        buttons_layout.addWidget(register_button)

        self.tab_widget.addTab(account_widget, "Account")

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

    def create_upgrades_tab(self):
        """Создает вкладку Upgrades"""
        upgrades_widget = QWidget()
        upgrades_widget.setObjectName("upgrades_tab")

        layout = QVBoxLayout(upgrades_widget)

        # Пример содержимого для вкладки Upgrades
        title_label = QLabel("Upgrades Tab")
        title_label.setAlignment(Qt.AlignCenter)

        # Примеры апгрейдов
        upgrade1_button = QPushButton("Auto Clicker - 100 coins")
        upgrade1_button.setObjectName("upgrade1_button")

        upgrade2_button = QPushButton("Double Click - 250 coins")
        upgrade2_button.setObjectName("upgrade2_button")

        upgrade3_button = QPushButton("Triple Click - 500 coins")
        upgrade3_button.setObjectName("upgrade3_button")

        layout.addWidget(title_label)
        layout.addWidget(upgrade1_button)
        layout.addWidget(upgrade2_button)
        layout.addWidget(upgrade3_button)
        layout.addStretch()

        self.tab_widget.addTab(upgrades_widget, "Upgrades")

    def create_leaderboard_tab(self):
        """Создает вкладку Leaderboard"""
        leaderboard_widget = QWidget()
        leaderboard_widget.setObjectName("leaderboard_tab")

        layout = QVBoxLayout(leaderboard_widget)

        # Пример содержимого для вкладки Leaderboard
        title_label = QLabel("Leaderboard Tab")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")

        # Пример таблицы лидеров
        leaderboard_frame = QFrame()
        leaderboard_frame.setObjectName("leaderboard_frame")
        leaderboard_layout = QVBoxLayout(leaderboard_frame)

        for i in range(1, 6):
            player_label = QLabel(f"{i}. Player{i} - {1000 - i * 100} points")
            player_label.setStyleSheet("padding: 5px; margin: 2px;")
            leaderboard_layout.addWidget(player_label)

        layout.addWidget(title_label)
        layout.addWidget(leaderboard_frame)
        layout.addStretch()

        self.tab_widget.addTab(leaderboard_widget, "Leaderboard")

    def on_click(self) -> None:
        self.clicks += 1
        self.total_label.setText(f"Total Clicks: {self.clicks}")
