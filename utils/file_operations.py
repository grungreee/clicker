import os
import json


def get_data() -> dict:
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
        data: dict = get_data()

        if "username" not in data or "password" not in data:
            os.remove("data.json")
            check_data_file()
        else:
            pass

