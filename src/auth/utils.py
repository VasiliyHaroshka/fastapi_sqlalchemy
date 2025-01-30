import jwt

from config import settings


def encode_jwt_token(
        payload,
        key,
        algorithm,
):
    """Return encoded jwt token"""
    encoded = jwt.encode(
        payload=payload,
        key=key,
        algorithm=algorithm,
    )
    return encoded
