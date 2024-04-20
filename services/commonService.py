import jwt
import pandas as pd    
import os
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

def jsonTocsv(data, pathObj, columnsKeys):
    try:
        path = pathObj[0]
        print( 'path--->', path, 'columnsKeys--->', columnsKeys)
        abs_path = os.path.abspath(path)

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        df = pd.DataFrame(data)
        df = df[columnsKeys]  # Keep only the specified columns
        df.to_csv(abs_path, index=False)

        print("File created successfully at:", abs_path)
    except Exception as e:
        print({"error": "An error occurred: " + str(e)})

def get_data_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

def insert_data_into_csv(data, file_path):
    try:
        # Check if the file exists
        file_exists = os.path.isfile(file_path)
        
        # Write data to CSV file
        df = pd.DataFrame(data)
        df.to_csv(file_path, mode='a', header=not file_exists, index=False)
        
        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def find_and_update_in_csv(condition, update_values, file_path):
    try:
        # Read data from CSV file
        df = pd.read_csv(file_path)
        
        # Update data based on condition
        df.loc[condition, list(update_values.keys())] = list(update_values.values())
        
        # Write updated data back to CSV file
        df.to_csv(file_path, index=False)
        
        print("Data updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_and_delete_in_csv(condition, file_path):
    try:
        # Read data from CSV file
        df = pd.read_csv(file_path)
        
        # Delete rows based on condition
        df = df[~condition]
        
        # Write updated data back to CSV file
        df.to_csv(file_path, index=False)
        
        print("Data deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
# file_path = "example.csv"
# data = get_data_from_csv(file_path)

# # Insert data into CSV
# new_data = {'Name': ['John', 'Alice'], 'Age': [30, 25]}
# insert_data_into_csv(new_data, file_path)
# new_data = {'Name': ['surya', 'aaa'], 'Age': [30, 25]}
# insert_data_into_csv(new_data, file_path)
# new_data = {'Name': ['vv', 'ggg'], 'Age': [30, 25]}
# insert_data_into_csv(new_data, file_path)

# df = pd.read_csv(file_path)
# condition = df['Name'] == 'John'

# # Values to update in matching rows
# update_values = {'Age': 35}

# # File path of the CSV file
# file_path = "example.csv"

# # Call the function to find and update data in the CSV file
# find_and_update_in_csv(condition, update_values, file_path)

# condition = df['Name'] == 'John'

# # File path of the CSV file
# file_path = "example.csv"

# # Call the function to find and delete data in the CSV file
# find_and_delete_in_csv(condition, file_path)
