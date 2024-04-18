import jwt
from datetime import datetime, timedelta
secreatKey = 'your_secret_key'
def create_jwt_token(payLoad):
    # Set payload with expiration time
    payload = {
        'payload': payLoad,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
    }
    # Encode payload with a secret key
    token = jwt.encode(payload, secreatKey, algorithm='HS256')
    return token


def verify_jwt_token(token):
    try:
        # Decode token using the secret key
        payload = jwt.decode(token, secreatKey, algorithms=['HS256'])
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
        exp_datetime = datetime.utcfromtimestamp(decoded_token['exp'])

        # print('cur time--->', datetime.datetime.utcnow())
        if exp_datetime < datetime.utcnow():
            raise jwt.ExpiredSignatureError('Token has expired')

        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Error: jwt token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Error: Invalid token.")
        return None

