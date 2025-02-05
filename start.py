import json
from fastapi import FastAPI

from models.User import User
import uvicorn

app = FastAPI()

users: list[User]

if __name__ == "__main__":
    with open("users.json") as f:
        users = json.load(f)

    for user in users:
        User.model_validate(user)

    print("Users loaded")
    uvicorn.run(app, host="localhost", port=8001)