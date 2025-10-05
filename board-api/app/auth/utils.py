from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.hash import pbkdf2_sha256  # <- length-safe, no 72-byte limit

SECRET_KEY = "umHJYaN1l4Bmrpz6oI1RG6XHeG+g7O9YDQPJ1nt64Xc="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    # strong, length-safe, widely used
    return pbkdf2_sha256.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # expected to contain {"sub": "<email>", "exp": ...}
        return payload
    except JWTError as e:
        raise ValueError("Invalid token") from e
