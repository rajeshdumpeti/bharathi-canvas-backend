from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.auth.utils import hash_password, verify_password, create_access_token

# Import your new schemas
from app.auth.schemas import (
    UserCreate, UserOut, Token,
    ForgotPasswordRequest, ResetPasswordRequest
)
# Import your new services
from app.services.auth import (
    request_password_reset, perform_password_reset
)


from app.auth.schemas import UserCreate, UserOut, Token
from app.auth.models import User
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(credentials: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user


# --- Password Reset Routes ---

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks, # Use background tasks to send email
):
    """
    Kicks off the password reset process.
    We run this as a background task so the API returns immediately.
    """
    # We do NOT pass the db session. The background task will create its own.
    background_tasks.add_task(request_password_reset, email=request.email)
    return {"message": "If an account with this email exists, a password reset link has been sent."}


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Verifies the token and sets the new password.
    """
    success = await perform_password_reset(
        token=request.token,
        new_password=request.new_password,
        db=db
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token."
        )

    return {"message": "Password has been reset successfully."}