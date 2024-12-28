import azure.functions as func

# import fastapi
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Optional
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# app = fastapi.FastAPI()
app = FastAPI()

@app.get("/sample")
async def index():
    return {
        "info": "Try /hello/Sandro for parameterized route.",
    }
    

 

@app.get("/hello/{name}")
async def get_name(name: str):
    return {
        "name": name,
    }
    
@app.get("/test")
async def index():
    return {
        "test": "Should be running now.",
    }
    
# ? modelnya
class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

# ? urusan hashing / password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ? cumn dummy db, remind me (future self) untuk hubungin ke external database
dummy_users_db = {
    "diddy": {
        "username": "diddy",
        "hashed_password": pwd_context.hash("secret"),
    }
}

# ? config untuk JWT
SECRET_KEY = "diddy-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#? OAuth2 Scheme dari FastAPI security (liat docs)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ? fungsi utils
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    user = dummy_users_db.get(username)
    if user:
        return UserInDB(**user)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ? endpoint untuk dapetin toketn
@app.post("/api/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ? fungsi untuk bantuin cek dependency/session
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

# ? protected route untuk pengujian user yang eligible
@app.get("/api/protected-route")
async def read_protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}

