from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.utils import extend_schema, OpenApiExample

from apps.users.views import RegisterView, ProfileView


# Wrap SimpleJWT views with schema annotations so they appear under
# the "Authentication" tag with clear descriptions.
DecoratedTokenObtainPairView = extend_schema(
    tags=['Authentication'],
    summary='Obtain JWT token pair',
    description=(
        'Authenticate with email + password and receive an access/refresh '
        'token pair.  Use the access token in the `Authorization: Bearer <token>` '
        'header for protected endpoints.'
    ),
    examples=[
        OpenApiExample(
            'Login Example',
            summary='Valid credentials',
            value={
                'email': 'user@example.com',
                'password': 'strongpassword123',
            },
            request_only=True,
        ),
    ],
)(TokenObtainPairView)

DecoratedTokenRefreshView = extend_schema(
    tags=['Authentication'],
    summary='Refresh JWT access token',
    description=(
        'Submit a valid refresh token to obtain a new access token '
        'without re-authenticating.'
    ),
    examples=[
        OpenApiExample(
            'Refresh Example',
            summary='Valid refresh token',
            value={
                'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
            },
            request_only=True,
        ),
    ],
)(TokenRefreshView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
]
