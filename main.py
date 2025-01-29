import random
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class SupportData(BaseModel):
    url: str
    text: str


class ResponseModel(BaseModel):
    data: UserData
    support: SupportData


class UserRequest(BaseModel):
    name: str
    job: str


class CreateUserResponse(BaseModel):
    name: str
    job: str
    id: int
    createdAt: str


class UpdateUserResponse(BaseModel):
    name: str
    job: str
    updatedAt: str


class PatchUserRequest(BaseModel):
    name: Optional[str] = None
    job: Optional[str] = None


@app.get("/api/users/{user_id}", response_model=ResponseModel)
def get_user(user_id: int):
    # Mock data for demonstration purposes
    users = {
        2: {
            "id": 2,
            "email": "janet.weaver@reqres.in",
            "first_name": "Janet",
            "last_name": "Weaver",
            "avatar": "https://reqres.in/img/faces/2-image.jpg",
        }
    }

    support_info = {
        "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
        "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
    }

    user = users.get(user_id)
    if not user:
        # improve error message
        raise HTTPException(status_code=404, detail="{}")

    return {
        "data": user,
        "support": support_info
    }


@app.post("/api/users", response_model=CreateUserResponse, status_code=201)
def create_user(user: UserRequest):
    created_at = datetime.now().isoformat() + "Z"
    return {
        "name": user.name,
        "job": user.job,
        "id": random.randint(1, 1000),
        "createdAt": created_at
    }


@app.put("/api/users/{user_id}", response_model=UpdateUserResponse)
def update_user(user: UserRequest):
    updated_at = datetime.now().isoformat() + "Z"
    return {
        "name": user.name,
        "job": user.job,
        "updatedAt": updated_at
    }


@app.patch("/api/users/{user_id}", response_model=UpdateUserResponse)
def update_user(user: UserRequest):
    updated_at = datetime.now().isoformat() + "Z"
    return {
        "name": user.name,
        "job": user.job,
        "updatedAt": updated_at
    }

# To run this app, use the following command in your terminal:
# uvicorn fastapi_microservice:app --reload


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)