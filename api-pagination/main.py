from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel
from fastapi_pagination import Page, add_pagination, paginate, LimitOffsetPage
from fastapi_pagination.customization import (
    CustomizedPage,
    UseParamsFields,
)
from sqlalchemy import create_engine
from sqlmodel import Session, select

from model import User

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

class Response(BaseModel):
    items: list[User]
    total: int
    filtered: int


app = FastAPI()
add_pagination(app)

engine = create_engine("sqlite:///database.db")  


@app.post("/data")
async def get_json_data(params: SearchRequestModel) -> Response:
    print(params)

    query = select(User).limit(params.length).offset(params.start)

    with Session(engine) as session:
        items = session.exec(query).all()

    return Response(items=items, total=1000, filtered=150)


# poetry run uvicorn main:app --reload
