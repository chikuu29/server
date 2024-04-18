import jwt
from datetime import datetime, timedelta

def create_jwt_token(email):
    # Set payload with expiration time
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
    }
    # Encode payload with a secret key
    token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
    return token


def verify_jwt_token(token):
    try:
        # Decode token using the secret key
        payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None

