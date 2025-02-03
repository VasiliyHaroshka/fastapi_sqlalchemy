from fastapi import HTTPException, status


def unauth_exception():
    unauth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="wrong username or password"
    )
    raise unauth_error


def unactive_exception():
    unactive_error = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user is not active"
    )
    raise unactive_error
