import random
from faker import Faker
from sqlmodel import SQLModel, Session, create_engine

from model import User


f = Faker()
engine = create_engine("sqlite:///database.db")  

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)  

def create_users(n: int):
    users = []
    for _ in range(1000):
        users.append(User(
            first_name =f.first_name(),
            last_name = f.last_name(),
            country = f.country(),
            age = random.randint(0, 100),
            city = f.city(),
        ))

    with Session(engine) as session:
        session.add_all(users)

        session.commit()


if __name__ == "__main__":  
    create_db_and_tables()  
    create_users(1000)