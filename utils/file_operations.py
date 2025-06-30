import os
import json
import hashlib
import string
import globals
from utils.requests import authenticate
from utils.handle_signals import start_sync


def get_data() -> dict:
    check_data_file()

    with open("data.json", "r") as file:
        data: dict = json.load(file)

    return data


def check_data_file() -> None:
    if not os.path.exists("data.json"):
        template: dict = {
            "account": {
                "username": None,
                "password": None
            }
        }

        with open("data.json", "w") as file:
            json.dump(template, file, indent=4)
    else:
        with open("data.json", "r") as file:
            data: dict = json.load(file)

        if "username" not in data["account"] or "password" not in data["account"]:
            os.remove("data.json")
            check_data_file()
        elif ((data["account"]["username"] is not None and data["account"]["password"] is not None)
              and globals.account is None):
            username: str = data["account"]["username"]
            password: str = data["account"]["password"]

            def on_success(_) -> None:
                globals.account = {"username": username, "password": password}
                globals.window.sync_data(background=False)
                start_sync(4000)

            def on_error(_) -> None:
                os.remove("data.json")
                check_data_file()

            authenticate("login", username, password, on_success, on_error)


def write_account_data(username: str, password: str) -> None:
    data: dict = get_data()

    data["account"]["username"] = username
    data["account"]["password"] = password

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


def check_all(username: str, password: str) -> str | bool:
    if username == "":
        return "The username input field is empty"
    if password == "":
        return "The password input field is empty"

    for symbol in username:
        if symbol not in string.ascii_letters + string.digits + "_-":
            return "Unsupported characters in username"
    if len(username) < 4:
        return "The length of the username must be longer than 3 characters"
    elif len(username) > 20:
        return "Username length should not be longer than 20 characters"

    for symbol in password:
        if symbol not in string.ascii_letters + string.digits + "_-":
            return "Unsupported characters in password"
    if len(password) < 5:
        return "The length of the password must be longer than 4 characters"
    elif len(username) > 30:
        return "Password length should not be longer than 30 characters"

    return True


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
