from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta
import os
from tasksapi.crud.user import get_user_by_username, get_user_token
from config import settings

# Use settings from config
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="tasks/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Check if token has expired
        if "exp" in payload:
            expire = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            if expire < datetime.now(timezone.utc):
                raise HTTPException(status_code=401, detail="Token has expired")
        
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from token"""
    payload = verify_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Also verify token exists in database
    if not verify_token_from_db(token):
        raise HTTPException(status_code=401, detail="Token not found in database")
    
    return username

def verify_token_from_db(token: str) -> bool:
    """Verify if token exists in database for the user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("sub")
        
        if not user_id or not username:
            return False
        
        # Check if token exists in database and is active
        stored_token = get_user_token(user_id)
        if stored_token and stored_token == token:
            return True
        
        return False
    except JWTError:
        return False
