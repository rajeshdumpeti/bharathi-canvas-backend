import brevo_python
from brevo_python.rest import ApiException
from app.core.config import settings

# --- 1. Configure the Brevo API client ---
# We configure it once when the module is loaded.
configuration = brevo_python.Configuration()
configuration.api_key['api-key'] = settings.brevo_api_key

# Create an API client instance
api_client = brevo_python.ApiClient(configuration)

# Create an instance of the TransactionalEmailsApi
api_instance = brevo_python.TransactionalEmailsApi(api_client)


async def send_password_reset_email(to_email: str, reset_token: str) -> bool:
    """
    Sends the password reset email using the Brevo API.
    """
    # --- 2. Create the Email Payload ---
    
    # We must provide a full URL for the frontend
    # TODO: We should add a FRONTEND_URL to config.py later.
    reset_url = f"{settings.frontend_url}/reset-password?token={reset_token}"
    sender = {
        "name": settings.email_from_name,
        "email": settings.email_from_address
    }
    to = [{"email": to_email}]
    
    subject = "Reset Your Password for Bharathi's Canvas"
    html_content = f"""
    <html>
    <body>
        <h1>Password Reset Request</h1>
        <p>You requested a password reset for your Bharathi's Canvas account.</p>
        <p>Please click the link below to set a new password. This link will expire in 15 minutes.</p>
        <a href="{reset_url}" 
           style="background-color: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
           Reset Your Password
        </a>
        <p>If you did not request this, please ignore this email.</p>
    </body>
    </html>
    """

    send_smtp_email = brevo_python.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_content
    )

    # --- 3. Send the Email ---
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Password reset email sent, Message ID: {api_response.message_id}")
        return True
    except ApiException as e:
        print(f"Error sending email via Brevo: {e}")
        return False