from fastapi import HTTPException, status


def unauth_exception():
    unauth_error = HTTPException(
        status_code=401,
        detail="wrong username or password"
    )
    raise unauth_error
