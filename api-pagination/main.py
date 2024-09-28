from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, func
from sqlmodel import Session, col, select

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
    draw: int = 0
    columns: list[ColumnModel] = Field(default_factory=list)
    order: list[OrderModel] = Field(default_factory=list)
    start: int = 0
    length: Optional[int] = None
    search: Optional[SearchModel] = None

class Response(BaseModel):
    items: list[User]
    total: int      # number of record total before filtering
    filtered: int   # number of match before pagination


app = FastAPI()

engine = create_engine("sqlite:///database.db")  


@app.post("/data")
async def get_json_data(params: SearchRequestModel) -> Response:
    print(params)

    query_base = select(User)                 # add there filtering of project    
    query_filtered = query_base.where(User.first_name == "David")
    query_paginated = query_filtered.limit(params.length).offset(params.start)

    with Session(engine) as session:
        total = session.scalar(select(func.count()).select_from(query_base.subquery()))
        filtered = session.scalar(select(func.count()).select_from(query_filtered.subquery()))
        items = session.exec(query_paginated).all()

    return Response(items=items, total=total, filtered=filtered)


# poetry run uvicorn main:app --reload
