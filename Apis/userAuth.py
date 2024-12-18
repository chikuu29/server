from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db.mongo import db
import bcrypt
from services.commonService import *
# Create your views here.

secreatKey = "your_secret_key"
class RegisterAPIView(APIView):
    def post(self, request):
        try:
        # Get data from request
            email = request.data.get('email')
            password = request.data.get('password')
            # confirm_password = request.data.get('confirmPswd')
            role = request.data.get('role')
            if(not email or not password or not role):
                return Response({"message": "Please fill in all fields","success":False}, status=status.HTTP_400_BAD_REQUEST)

            # Check if passwords match
            # if password != confirm_password:
            #     return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

            # Connect to MongoDB
            collection = db['users']

            # Check if email already exists
            if collection.find_one({"email": email}):
                return Response({"message": "Email already exists","success":False}, status=status.HTTP_400_BAD_REQUEST)

            # Insert new user into MongoDB
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_data = {
                "email": email,
                "password": hashed_password.decode('utf-8') ,
                 "role":role # In practice, you should hash the password
            }
            inserted_id = collection.insert_one(user_data).inserted_id

            # Return success response
            return Response({"message": "User registered successfully", "email":email,'success':True}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "An error occurred: " + str(e),'success':False}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    def post(self,request):
        response = Response(
            {
            "message": "Loginout successful"
            }, status=status.HTTP_200_OK )
        response.delete_cookie(
            key="jwt_token",
             samesite= 'Lax',
            path="/"
            )
        return response


class LoginAPIView(APIView):
    def post(self, request):
        try:
            # Get data from request
            email = request.data.get('email')
            password = request.data.get('password')
            print
            if not email or not password:
                return Response({"error": "Please provide both email and password"}, status=status.HTTP_400_BAD_REQUEST)

            # Connect to MongoDB
            collection = db['users']

            # Check if user exists
            user = collection.find_one({"email": email})
            if user:
                print("User exists", user)
                if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    print("Password is correct")
                    payLoad = {
                        "email": email,
                        "role":user['role']
                    }
                    token = create_jwt_token(payLoad)
                    response = Response(
                        {
                            "message": "Login successful",
                              "role":user['role'],
                              "email": email,
                                'success': True
                                },
                                  status=status.HTTP_200_OK
                                  )
                    response.set_cookie(
                            key='jwt_token',
                            value=str(token),
                            httponly=True,
                            samesite= 'Lax',
                            secure=False,
                            max_age=timedelta(days=2).total_seconds(),  # Set cookie expiration time
                            path='/'  # Set a specific path for the refresh token cookie
                        )
                    response.set_cookie(
                            key='role',
                            value=str(user['role']),
                            samesite= 'Lax',
                            httponly=True,
                            secure=False,
                            max_age=timedelta(days=2).total_seconds(),  # Set cookie expiration time
                            path='/'  # Set a specific path for the refresh token cookie
                        )
                    return response
                else:
                    return Response({"message": "Invalid email or password", 'success': False}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message": "Invalid email or password", 'success': False}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": "An error occurred: " + str(e), 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        
class checkLoginStatus(APIView):
    def get(self, request):
        try:
            # Get data from request
            

            token = request.COOKIES['jwt_token']
         
            if not token:
                return Response({"error": "Please provide token"}, status=status.HTTP_400_BAD_REQUEST)
           
            tokenData = validate_jwt_token(token,secreatKey)['payload']
            print(tokenData)
            if tokenData:
                return Response({"message": "Login successful", "email":tokenData['email'],"role":tokenData['role'],'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid token", 'success': False}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": "An error occurred: " + str(e), 'success': False}, status=status.HTTP_400_BAD_REQUEST)
