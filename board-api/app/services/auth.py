import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.db.session import SessionLocal # <-- ADD THIS IMPORT
from app.auth.models import User
from app.services.email_service import send_password_reset_email

# --- 1. Import password utils from your central security file ---
from app.utils.security import hash_password

# (We don't need verify_password for this flow, but if we did, we'd import it here too)


# --- 2. Token Hashing (using hashlib) ---
# This is for the reset token, NOT user passwords.
# A fast hash is secure for a high-entropy token.
def get_token_hash(token: str) -> str:
    """Hashes a plain-text token using SHA-256."""
    return hashlib.sha256(token.encode()).hexdigest()


# --- 3. Password Reset Service Functions ---

async def request_password_reset(email: str) -> bool:
    """
    Handles the "Forgot Password" request as a background task.
    This function creates and manages its own database session.
    """
    
    # 1. Create a new, independent database session
    with SessionLocal() as db:
        try:
            # 2. Find user by email.
            user = db.query(User).filter(User.email == email).first()

            # 3. !! IMPORTANT !!
            # If no user is found, we return True anyway.
            if not user:
                print(f"Password reset request for non-existent email: {email}")
                return True # Do not reveal that the user does not exist.

            # 4. Generate a secure, URL-safe token (e.g., 32 bytes)
            plain_text_token = secrets.token_urlsafe(32)

            # 5. Hash the token before storing it in the database.
            hashed_token = get_token_hash(plain_text_token)

            # 6. Set an expiry time (e.g., 15 minutes from now)
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

            # 7. Save the hashed token and expiry to the user model
            user.reset_password_token = hashed_token
            user.reset_token_expires_at = expires_at
            db.commit()

            # 8. Send the email with the *plain-text* token
            # This is safe to do *after* the commit.
            await send_password_reset_email(
                to_email=user.email,
                reset_token=plain_text_token
            )
            
            print(f"Password reset email sent to {email}")
            return True

        except Exception as e:
            print(f"Error in background request_password_reset: {e}")
            db.rollback()
            # Even if the email fails, we don't tell the user.
            return True
        
        
async def perform_password_reset(token: str, new_password: str, db: Session) -> bool:
    """
    Handles the "Reset Password" submission.
    Validates the token, checks expiry, and updates the password.
    """
    try:
        # 1. Hash the incoming plain-text token to find it in the DB
        hashed_token = get_token_hash(token)

        # 2. Find the user by the *hashed* token
        user = db.query(User).filter(
            User.reset_password_token == hashed_token
        ).first()

        # 3. Check if token is valid or expired
        if not user:
            print("Password reset attempt with invalid token.")
            return False # Token not found

        if user.reset_token_expires_at <= datetime.now(timezone.utc):
            print(f"Password reset attempt with expired token for user {user.email}")
            # Clear the expired token
            user.reset_password_token = None
            user.reset_token_expires_at = None
            db.commit()
            return False # Token expired

        # 4. Token is valid. Update the password.
        #    We use the imported hash_password function from security.py
        user.hashed_password = hash_password(new_password)
        
        # 5. Invalidate the token so it can't be used again.
        user.reset_password_token = None
        user.reset_token_expires_at = None
        
        db.commit()
        print(f"Password successfully reset for user {user.email}")
        return True

    except Exception as e:
        print(f"Error in perform_password_reset: {e}")
        db.rollback()
        return False