from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
import secrets

# User database (replace with a database or more secure storage in production)
USER_DB = {
    "apiuser": "killbill"
}


# Function to verify credentials
def verify_credentials(credentials: HTTPBasicCredentials):
    correct_username = secrets.compare_digest(credentials.username, "apiuser")
    correct_password = secrets.compare_digest(credentials.password, USER_DB.get(credentials.username))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
