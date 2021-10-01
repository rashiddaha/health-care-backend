from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from users.models import APKBuild
from users.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
    UserProfileSerializer,
    APKBuildSerializer, ReSendSerializer
)


User = get_user_model()


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.none()
    http_method_names = ["post", "option"]

    @swagger_auto_schema(request_body=ReSendSerializer)
    @action(methods=['post'], detail=False, url_path='re-send', url_name='re-send')
    def re_send(self, request, *args, **kwargs):
        response = "Email sent!"
        serializer = ReSendSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(response)


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})


class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    http_method_names = ["get", "patch"]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({"error": "Please login first"}, status=status.HTTP_403_FORBIDDEN)
        queryset = self.filter_queryset(self.get_queryset()).filter(id=self.request.user.id)
        serializer = self.get_serializer(queryset.first(), many=False)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        if not self.request.user.is_authenticated:
            return Response({"error": "Please login first"}, status=status.HTTP_403_FORBIDDEN)
        if instance.id == self.request.user.pk:
            return self.update(request, *args, **kwargs)
        else:
            return Response({"error": "Only owner can update the details."}, status=status.HTTP_403_FORBIDDEN)


class APKBuildViewSet(ReadOnlyModelViewSet):
    queryset = APKBuild.objects.all()
    serializer_class = APKBuildSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset.first(), many=False)
        return Response(serializer.data)

