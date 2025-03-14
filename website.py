import shelve
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
import pprint
from datetime import timedelta, datetime
from jose import JWTError, jwt


users = {
    "alice": "password123",
    "bob": "password456",
    "charlie": "password789"
}

pwd_ctx = CryptContext(schemes=["sha256_crypt"])

def get_password_hash(password):
    return pwd_ctx.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password, hashed_password)



class UserAccount(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


db_path = "./users_accounts_db"


with shelve.open(db_path) as db:
    for user, password in users.items():
        db[user] = get_password_hash(password)

print("stored users in shelve db")


def get_user_hashed_pwd(username: str):
    with shelve.open(db_path) as db:
        if username in db:
            return db[username]


def authenticate_user(username: str, password: str):
    user_hashed = get_user_hashed_pwd(username)
    if not user_hashed:
        return False
    if verify_password(password, user_hashed):
        return True
    else:
        return False


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "SECRET_KEY", algorithm="HS256")
    return encoded_jwt


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


# Login endpoint
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"form_data: {form_data}")
    username = form_data.username
    success = authenticate_user(username, form_data.password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=10)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

