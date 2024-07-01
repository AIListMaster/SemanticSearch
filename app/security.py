from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
import secrets
import os

# Implement JWT instead.
# Read credentials from environment variables
API_USERNAME = os.getenv("API_USERNAME", "apiuser")
API_PASSWORD = os.getenv("API_PASSWORD", "killbill")


# Function to verify credentials
def verify_credentials(credentials: HTTPBasicCredentials):
    correct_username = secrets.compare_digest(credentials.username, API_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, API_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
