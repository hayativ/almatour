from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample

from apps.users.serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """Register a new user account.

    Creates a new user with the provided email, username, phone, and
    password.  Returns the created user profile on success.
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Authentication'],
        summary='Register a new user',
        description=(
            'Create a new Almatour account. '
            'Email and phone must be unique. Password must be at least 8 characters.'
        ),
        examples=[
            OpenApiExample(
                'Registration Example',
                summary='Valid registration data',
                value={
                    'email': 'user@example.com',
                    'username': 'almaty_traveler',
                    'phone': '+77001234567',
                    'password': 'strongpassword123',
                },
                request_only=True,
            ),
        ],
        responses={
            201: OpenApiResponse(
                response=UserSerializer,
                description='User created successfully.',
            ),
            400: OpenApiResponse(description='Validation error (duplicate email/phone, weak password, etc.).'),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(
    retrieve=extend_schema(
        tags=['Users'],
        summary='Get current user profile',
        description='Returns the profile of the currently authenticated user.',
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.'),
        },
    ),
    update=extend_schema(
        tags=['Users'],
        summary='Update current user profile',
        description="Fully update the authenticated user's username and/or phone.",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.'),
        },
    ),
    partial_update=extend_schema(
        tags=['Users'],
        summary='Partially update current user profile',
        description='Patch one or more profile fields (username, phone).',
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.'),
        },
    ),
)
class ProfileView(generics.RetrieveUpdateAPIView):
    """Get or update the authenticated user's profile."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
