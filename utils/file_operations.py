import os
import json
from utils.requests import login


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

        if "username" not in data or "password" not in data:
            os.remove("data.json")
            check_data_file()
        elif data["username"] is not None and data["password"] is not None:
            response = login(data["username"], data["password"])
