import threading
import requests as rq
from gui.dialogs import show_confirm_dialog
from utils.handle_signals import show_error, show_spinner, close_spinner

__local__: bool = True

url: str = "http://127.0.0.1:8000" if __local__ else "https://clicker-xnay.onrender.com"


def do_request(endpoint: str, data: dict = None) -> tuple:
    try:
        response: rq.Response = rq.post(f"{url}/{endpoint}", json=data)

        if response.status_code != 200:
            show_error("Error", str(response.json()))

        return response.status_code, response.json()
    except Exception as e:
        show_error("Error", str(e))
        return ()


def register(username: str, password: str) -> None:
    if show_confirm_dialog("Confirmation", "Are you sure you want to register?"):
        data: dict = {
            "username": username,
            "password": password
        }

        show_spinner()

        def do():
            response = do_request("register", data)
            print(response[0], response[1])
            close_spinner()

        threading.Thread(target=do).start()


def login(username: str, password: str) -> None:
    data: dict = {
        "username": username,
        "password": password
    }

    show_spinner()

    def do():
        response = do_request("login", data)
        print(response[0], response[1])
        close_spinner()

    threading.Thread(target=do).start()
