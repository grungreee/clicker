import threading
import requests as rq
from typing import Callable, Literal
from gui.dialogs import show_confirm_dialog
from utils.handle_signals import show_error, show_spinner, close_spinner, update_account_tab

__local__: bool = True

url: str = "http://127.0.0.1:8000" if __local__ else "https://clicker-xnay.onrender.com"


def do_request(endpoint: str, data: dict = None) -> tuple | None:
    try:
        response: rq.Response = rq.post(f"{url}/{endpoint}", json=data)

        if response.status_code != 200:
            show_error("Error", response.json()["detail"])

        return response.status_code, response.json()
    except rq.exceptions.ConnectionError:
        show_error("Error", "Failed to connect to the server (servers are currently down).")
        return None
    except Exception as e:
        show_error(f"{type(e).__name__}", f"Error: {e}")
        return None


def authenticate(type_: Literal["login", "register"], username: str, password: str, on_success: Callable | None = None,
                 on_error: Callable | None = None) -> None:
    if type_ == "login" or show_confirm_dialog("Confirmation", "Are you sure you want to register?"):
        data: dict = {
            "username": username,
            "password": password
        }

        show_spinner()

        def request():
            response = do_request(type_, data)
            close_spinner()
            if response is not None:
                if response[0] == 200:
                    if on_success is not None:
                        on_success(response[1])
                else:
                    if on_error is not None:
                        on_error(response[1])

        threading.Thread(target=request).start()
