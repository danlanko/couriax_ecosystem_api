from rest_framework import viewsets, renderers, permissions
from apis.users.authentication.models import CustomUser as User
from .serializers import UserOnboardSerializer, UserUpdateSerializer


class UserOnboarding(viewsets.ModelViewSet):
    renderer_classes = [renderers.JSONRenderer]
    http_method_names = ['post', 'get', 'patch']
    queryset = User.objects.all()
    serializer_class = UserOnboardSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserUpdateSerializer
        else:
            return UserOnboardSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [permissions.IsAuthenticated, ]
        return super().get_permissions()
