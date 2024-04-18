from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db.mongo import db
import bcrypt
from services.commonService import *
# Create your views here.


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
                    token = create_jwt_token(email)
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
                            samesite= 'None',
                            secure=True,
                            max_age=timedelta(days=2).total_seconds(),  # Set cookie expiration time
                            path='/'  # Set a specific path for the refresh token cookie
                        )
                    response.set_cookie(
                            key='role',
                            value=str(user['role']),
                            samesite='None',
                            httponly=True,
                            secure=True,
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