from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    country: str
    city: str
    age: int


app = FastAPI()


@app.get("/data")
async def get_json_data() -> list[User]:
    with open("data.json", "r") as file:
        data = json.load(file)
    
    return [User.model_validate(x) for x in data]

# poetry run uvicorn main:app --reload