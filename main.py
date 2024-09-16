from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import PlainTextResponse

# Create an instance of FastAPI
app = FastAPI()

# In-Memory 'database'
user_db = [{
    "id": 1,
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
}]

# Define a Pydantic model for the user_data
class User(BaseModel):
    id: int
    name: str
    age: int 
    email: Optional[str] = None


@app.get('/', response_class=PlainTextResponse)
def home():
    return "Welcome to the FastAPI application!"

# Route to get the list of users
@app.get("/users", response_model=List[User])
def read_users():
    return user_db

# Route to get a user by id
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in user_db:
        if user['id'] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User Not Found")

# Route to add a new user
@app.post('/users', response_model=User)
def create_user(user: User):
    user_db.append(user.dict())  # Convert Pydantic model to dictionary
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)
