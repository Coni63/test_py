from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):  
    id: int | None = Field(default=None, primary_key=True)  
    first_name: str  
    last_name: str  
    country: str  
    city: str  
    age: int