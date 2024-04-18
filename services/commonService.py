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

def validate_jwt_token(jwt_token, secretKey):
    try:
        # print('jwt_token--->', jwt_token, 'secretKey---', secretKey)
        decoded_token = jwt.decode(jwt_token, secretKey, algorithms=['HS256'])
        # print('exp--->', decoded_token)

        # Convert 'exp' value to datetime.datetime
        exp_datetime = datetime.datetime.utcfromtimestamp(decoded_token['exp'])

        # print('cur time--->', datetime.datetime.utcnow())
        if exp_datetime < datetime.datetime.utcnow():
            raise jwt.ExpiredSignatureError('Token has expired')

        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Error: jwt token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Error: Invalid token.")
        return None

