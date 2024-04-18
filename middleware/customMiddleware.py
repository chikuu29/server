from rest_framework import status
from django.http import JsonResponse
import jwt

class UserValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path includes 'AuthTn'
        print(request.path)
        if 'authTn' in request.path:
            print("UserValidationMiddleware")
            # Check if Authorization header is present
            if 'Authorization' not in request.headers:
                return JsonResponse({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

            token = request.cookies['jwt_token'].split(' ')[1]

            try:
                payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
                user_role = payload.get('role')

                # Check user's role
                # if user_role != 'admin':  # Replace 'admin' with the role you want to validate
                #     return Response({"error": "Unauthorized access. Insufficient privileges"}, status=status.HTTP_403_FORBIDDEN)

                # Add user information to request for further processing
                request.user_email = payload.get('email')

            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)
        return response
