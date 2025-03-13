import shelve
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

users = {
    "alice": "password123",
    "bob": "password456",
    "charlie": "password789"
}

class UserAccount(BaseModel):
    username: str
    password: str


db_path = "./users_accounts_db"


with shelve.open(db_path) as db:
    for user, password in users.items():
        db[user] = password

print("stored users in shelve db")

with shelve.open(db_path) as db:
    for user, password in db.items():
        print (f"{user} - {password}")

app = FastAPI()

@app.get("/users/", response_model=list[UserAccount])
def get_users():
    user_accounts = []
    with shelve.open(db_path) as db:
        for usr, pwd in db.items():
            user_accounts.append(UserAccount(username=usr, password=pwd))
    return user_accounts

# main website in file ./index.html
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html") as f:
        return f.read()




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

