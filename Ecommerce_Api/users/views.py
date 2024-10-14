from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.shortcuts import redirect
from .models import Profile
from .serializers import ProfileSerializer

User = get_user_model()

# User Registration View
class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Redirect to login page
        return Response(
            {
                "message": "Registration successful! Please log in.",
                "redirect_url": "http://127.0.0.1:8000/users/login/"
            },
            status=status.HTTP_201_CREATED,
        )

# User Login View
class UserLoginAPIView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
        }, status=status.HTTP_200_OK)


# User Logout View
class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the token from the request headers
            token = request.META.get('HTTP_AUTHORIZATION').split()[1]
            # Blacklist the token
            OutstandingToken.objects.get(token=token).blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except OutstandingToken.DoesNotExist:
            return Response({"detail": "Token already blacklisted."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for listing and creating

    def perform_create(self, serializer):
        # Automatically assign the user to the profile
        serializer.save(user=self.request.user)

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for retrieving, updating, and deleting