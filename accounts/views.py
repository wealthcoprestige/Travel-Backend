from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout
from accounts.serializers import LoginSerializer
from rest_framework.response import Response
from accounts.middlewares import UserMiddlewares
from rest_framework import status
from rest_framework.views import APIView
from travel.models.applicants import Applicant
from travel.serializers import ApplicantSerializers

# Create your views here.


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = UserMiddlewares.getUserByEmailOrUsername(
            email=validated_data["email"],
            password=validated_data["password"],
        )

        if not user:
            return Response(
                {"message": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"message": "Account is not activated"},
                status=status.HTTP_403_FORBIDDEN,
            )

        applicant_data = None
        try:
            applicant = Applicant.objects.get(user=user)
            applicant_data = ApplicantSerializers(
                applicant, context={"request": request}
            ).data
        except Applicant.DoesNotExist:
            applicant_data = None

        token = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful",
                "applicant": applicant_data,
                "token": {"access": str(token.access_token), "refresh": str(token)},
            },
            status=status.HTTP_200_OK,
        )


class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                return Response(
                    {"message": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            logout(request)

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

        except TokenError:
            return Response(
                {"message": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
