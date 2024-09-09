from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Union
from pydantic import BaseModel
from fastapi.params import Body
# import random
from random import randrange, choices
import psycopg
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)

load_dotenv()
app = FastAPI()

# Connecting to Database(postgres)
import psycopg

# try:
#     conn = psycopg.connect("dbname=students user=postgres password=2020 host=localhost")
#     cur = conn.cursor()
#     print("Connected Successfully")
    
#     # Execute the SQL command to create the table
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id serial PRIMARY KEY,
#             firstname character varying,
#             lastname character varying,
#             age integer,
#             email character varying UNIQUE,
#             address character varying,
#             reg_number character varying UNIQUE,
#             created_at timestamp with time zone DEFAULT NOW()
#         )
#     """)
            
#     # Commit the transaction
#     conn.commit()
#     print("Table created and committed successfully.")
# except psycopg.OperationalError as e:
#     print(f"Operational error occurred: {e}")
# except Exception as e:
#     print(f"An error occurred: {e}")


# Using Pydantic schema to creat our registeration model.
class AccountCreating(BaseModel):
    firstname: str
    lastname: str
    age: int
    email: str
    address: str



# Creating a unique reg number
reg = randrange(0, 9999)

def createRegNo():
    alphabet_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    reg_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    random_letters = choices(alphabet_list, k=3)
    random_numbers = choices(reg_num, k=5)
    random_string = ''.join(random_letters)
    random_number = ''.join(random_numbers)

    return f"{random_string}{random_number}"

regNo = createRegNo()
print(regNo)


# looping through users to get ID
def get_user_id(id, db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    for user in users:
        if user["id"] == id:
            return user
        

# Getting the user index
def user_index(id, db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    for i, u in enumerate(users):
        if u["id"] == id:
            return i

@app.get("/")
def home():
    return {"task": "Anniversary"}

@app.get("/test")
def test(db: Session = Depends(get_db)):
    return {"data": "Succesfull"}



# Post New Users to database
@app.post("/user", status_code=status.HTTP_201_CREATED)
def signup(newuser: AccountCreating, db: Session = Depends(get_db)):
    # cur.execute(""" INSERT INTO users (firstname, lastname, age, email, address, reg_number) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * """, (newuser.firstname, newuser.lastname, newuser.age, newuser.email, newuser.address, regNo))
    # new_user = cur.fetchone()
    # conn.commit()
    new_user = db.query(models.Users)
    return {"Users": new_user}


@app.get("/user")
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.Users).all()
    return {"users": all_users}

# Getting a user by ID
@app.get("/user/{id}")
def get_users_By_Id(id: int, db: Session = Depends(get_db)):
    # cur.execute(""" SELECT * from users WHERE id = %s """, (str(id),))
    # datab_id = cur.fetchone()
    datab_id = db.query(models.Users).all()
    print(datab_id)
    if not datab_id: # If the ID doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} not found")
    print(datab_id)
    return {"User No": datab_id}


# Deleting a User
@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    user_to_delete = user_index(id)
    if user_to_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id: {id} not found or already deleted")
    users.pop(user_to_delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updating a user info

@app.put("/user/{id}")
def update_user(id: int, newuser: AccountCreating):
    index = user_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id: {id} not found")
    user_list = newuser.model_dump()
    user_list["id"] = id
    users[index] = user_list
    return {"data": user_list}