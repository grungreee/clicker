import time
import mysql.connector
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv


class User(BaseModel):
    username: str
    password: str


class UserStats(BaseModel):
    clicks: int
    camel_coins: int


class SyncData(BaseModel):
    delta_clicks: int


class MessageResponse(BaseModel):
    message: str


class UpgradesResponse(BaseModel):
    user_upgrades: dict
    all_upgrades: dict


# uvicorn server.api:app --host 0.0.0.0 --port 8000
app = FastAPI()

load_dotenv("server/.env")
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_USER"),
    port=os.getenv("MYSQL_PORT"),
    connection_timeout=10)

cursor = db.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users ("
    "username VARCHAR(255) PRIMARY KEY,"
    "password VARCHAR(255) NOT NULL,"
    "clicks INTEGER DEFAULT 0,"
    "camel_coins INTEGER DEFAULT 0,"
    "last_sync_time INTEGER DEFAULT 0"
    ")"
)

cursor.execute("DROP TABLE IF EXISTS upgrades")
cursor.execute("CREATE TABLE IF NOT EXISTS upgrades "
               "(id INT PRIMARY KEY AUTO_INCREMENT, "
               "name VARCHAR(50) NOT NULL, "
               "cost INT NOT NULL, effect TEXT, "
               "value INT NOT NULL, "
               "type ENUM('click', 'auto', 'passive') NOT NULL"
               ")")

cursor.execute("INSERT INTO upgrades (name, cost, value, type) VALUES "
               "('Auto Camel', 100, 1, 'auto'), "
               "('Auto Camel II', 1000, 6, 'auto'), "
               "('Camel Farm', 1000, 10, 'auto'), "
               "('Camel King', 10000, 100, 'auto'), "
               "('Camel Emperor', 100000, 1000, 'auto'), "
               "('Camel Overlord', 500000, 5000, 'auto'), "
               "('Camel Titan', 1000000, 10000, 'auto'), "

               "('Camel Cursor', 500, 1, 'click'), "
               "('Camel Clicker', 400, 5, 'click'), "
               "('Camel Clickstorm', 2000, 100, 'click'), "
               "('Camel Clickzilla', 100000, 1000, 'click'), "
               "('Camel Clicknado', 10000000, 10000, 'click')"
               )

cursor.execute(
    "CREATE TABLE IF NOT EXISTS user_upgrades ("
    "id INT PRIMARY KEY AUTO_INCREMENT, "
    "username VARCHAR(255), "
    "upgrade_id INT, "
    "count INT DEFAULT 1, "
    "FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE, "
    "FOREIGN KEY (upgrade_id) REFERENCES upgrades(id) ON DELETE CASCADE, "
    "UNIQUE(username, upgrade_id)"
    ")"
)

db.commit()


def check_account(username, password) -> None:
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE username = %s AND password = %s", (username, password))
    if cursor.fetchone()[0] == 0:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


@app.post("/register")
async def register(user: User) -> MessageResponse:
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (user.username,))
    if cursor.fetchone()[0] > 0:
        raise HTTPException(status_code=400, detail="Nickname already exists")

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (user.username, user.password),
    )
    db.commit()

    return MessageResponse(message="User registered successfully!")


@app.post("/login")
async def login(user: User) -> MessageResponse:
    check_account(user.username, user.password)

    return MessageResponse(message="Login successful!")


@app.post("/get_data")
async def get_data(user: User) -> UserStats:
    check_account(user.username, user.password)

    cursor.execute("SELECT clicks, camel_coins FROM users WHERE username = %s", (user.username,))
    stats = cursor.fetchone()

    return UserStats(clicks=stats[0], camel_coins=stats[1])


@app.post("/sync_data")
async def sync_data(user: User, stats: SyncData) -> UserStats:
    check_account(user.username, user.password)

    cursor.execute(
        "SELECT clicks, camel_coins, last_sync_time FROM users WHERE username = %s", (user.username,)
    )
    clicks, coins, last_sync_time = cursor.fetchone()

    delta_clicks = min((int(time.time()) - last_sync_time) * 35, stats.delta_clicks)

    cursor.execute("UPDATE users SET clicks = %s, camel_coins = %s, last_sync_time = %s WHERE username = %s",
                   (clicks + delta_clicks, coins + delta_clicks, int(time.time()), user.username))
    db.commit()
    return UserStats(clicks=clicks + delta_clicks, camel_coins=coins + delta_clicks)


@app.post("/get_upgrades")
async def get_upgrades(user: User) -> UpgradesResponse:
    check_account(user.username, user.password)

    cursor.execute("""
        SELECT u.id, u.name, u.cost, u.value, u.type, uu.count
        FROM upgrades u
        JOIN user_upgrades uu ON u.id = uu.upgrade_id
        WHERE uu.username = %s
    """, (user.username,))

    bought = cursor.fetchall()
    user_upgrades_dict = {}

    for id_, name, cost, value, type_, count in bought:
        user_upgrades_dict[id_] = {
            "name": name,
            "cost": cost,
            "value": value,
            "type": type_,
            "count": count
        }

    cursor.execute("SELECT id, name, cost, value, type FROM upgrades")
    all_upgrades = cursor.fetchall()
    all_upgrades_dict = {
        id_: {
            "name": name,
            "cost": cost,
            "value": value,
            "type": type_
        }
        for id_, name, cost, value, type_ in all_upgrades
    }

    return UpgradesResponse(user_upgrades=user_upgrades_dict, all_upgrades=all_upgrades_dict)

