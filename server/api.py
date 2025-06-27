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


class MessageResponse(BaseModel):
    message: str


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
    "camel_coins INTEGER DEFAULT 0"
    ")"
)


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
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE username = %s AND password = %s", (user.username, user.password))
    if cursor.fetchone()[0] == 0:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return MessageResponse(message="Login successful!")


@app.post("/get_data")
async def get_data(user: User) -> UserStats:
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE username = %s AND password = %s", (user.username, user.password))
    if cursor.fetchone()[0] == 0:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    cursor.execute("SELECT clicks, camel_coins FROM users WHERE username = %s", (user.username,))
    stats = cursor.fetchone()

    return UserStats(clicks=stats[0], camel_coins=stats[1])
