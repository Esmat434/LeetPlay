from django.contrib.auth import authenticate, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .permissions import IsAuthenticationToken, AllowAnyUser
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    LoginSerializer,
    CheckEmailExistsSerializer,
    SetNewPasswordSerializer,
)
from accounts.models import CustomUser, Password_Token


# this is registration class view
class CreateUserView(APIView):
    permission_classes = [AllowAnyUser]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# this is update delete and get class view
class GetUpdateUserView(APIView):
    permission_classes = [IsAuthenticationToken]

    def get_user(self, request):
        try:
            user = CustomUser.objects.get(username=request.user.username)
            return user
        except CustomUser.DoesNotExist:
            return False

    def get(self, request):
        user = self.get_user(request)

        if not user:
            return Response(
                {"error": "User does not exists"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = self.get_user(request)

        if not user:
            return Response(
                {"error": "User does not exists."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# this is login class view
class LoginView(APIView):
    permission_classes = [AllowAnyUser]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response(token.key, status=status.HTTP_200_OK)
            return Response(
                {"error": "User does not exists."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticationToken]

    def delete(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            logout(request)
            return Response(
                {"success": "You successfully loged out."}, status=status.HTTP_200_OK
            )
        except Token.DoesNotExist:
            return Response(
                {"error": "User does not exists."}, status=status.HTTP_404_NOT_FOUND
            )


# this is profile class view
class ProfileView(APIView):
    permission_classes = [IsAuthenticationToken]

    def get_user(self, request):
        try:
            user = CustomUser.objects.get(username=request.user.username)
            return user
        except CustomUser.DoesNotExist:
            return False

    def get(self, request):
        user = self.get_user(request)
        if not user:
            return Response(
                {"error": "User does not exists."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# this is password forgot class view
class PasswrdForgotView(APIView):
    permission_classes = [AllowAnyUser]

    def post(self, request):
        serializer = CheckEmailExistsSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {
                    "success": "Your email verified successfully and send change password token to your email."
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# this is set new password class view that can set new password if you forgot your password
class SetNewPasswordView(APIView):
    permission_classes = [AllowAnyUser]

    def get_token(self, key):
        try:
            token = Password_Token.objects.get(token=key)
        except Password_Token.DoesNotExist:
            return False

        if token.CheckTokenExpiration():
            token.delete()
            return False
        return token

    def post(self, request, token):
        password = request.data.get("password1")
        token = self.get_token(token)
        if not token:
            return Response(
                {"error": "Please create another token this token is expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token.user.set_password(password)
            token.user.save()
            token.delete()
            return Response(
                {
                    "success": "Your password changed successfully. Please login to your account."
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
