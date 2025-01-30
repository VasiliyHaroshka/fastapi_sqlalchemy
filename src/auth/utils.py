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

def decode_jwt_token(
    token,
    puclic_key,
    algorithm,
):
    """Return decoded jwt token"""
    decoded = jwt.decode(
        token,
        puclic_key,
        algorithms=[algorithm],
    )
    return decoded

