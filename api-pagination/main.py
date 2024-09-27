from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel
from fastapi_pagination import Page, add_pagination, paginate, LimitOffsetPage
from fastapi_pagination.customization import (
    CustomizedPage,
    UseParamsFields,
)

class User(BaseModel):
    first_name: str
    last_name: str
    country: str
    city: str
    age: int


class SearchModel(BaseModel):
    value: str
    regex: bool
    fixed: list = []  # Adjust based on what kind of data is in the fixed field

class ColumnModel(BaseModel):
    data: str
    name: str = ""
    searchable: bool
    orderable: bool
    search: SearchModel

class OrderModel(BaseModel):
    column: int
    dir: str
    name: str = ""

class SearchRequestModel(BaseModel):
    draw: int
    columns: list[ColumnModel]
    order: list[OrderModel]
    start: int
    length: int
    search: SearchModel


app = FastAPI()
add_pagination(app)


@app.post("/data")
async def get_json_data(params: SearchRequestModel) -> CustomizedPage[LimitOffsetPage[User], UseParamsFields(limit=10)]:
    print(params)

    with open("data.json", "r") as file:
        data = json.load(file)
    
    data = [User.model_validate(x) for x in data]

    return paginate(data)


# poetry run uvicorn main:app --reload
