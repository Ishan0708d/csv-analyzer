import requests
import os
import json

HISTORY_FILE = "upload_history.json"
API_BASE = "http://127.0.0.1:8000/api"
TOKEN_FILE = "token.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE) as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)


def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"access": token}, f)


def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE) as f:
        return json.load(f).get("access")


def clear_token():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)


def login(username, password):
    res = requests.post(
        f"{API_BASE}/token/",
        json={"username": username, "password": password},
    )
    if res.status_code != 200:
        return None
    return res.json()["access"]


def register(username, password):
    res = requests.post(
        f"{API_BASE}/register/",
        json={"username": username, "password": password},
    )
    return res.status_code == 201


def upload_csv(token, file_path):
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, "rb") as f:
        return requests.post(
            f"{API_BASE}/upload/",
            headers=headers,
            files={"file": f},
        )
