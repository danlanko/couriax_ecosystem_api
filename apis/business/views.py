from rest_framework import viewsets, renderers
from apis.business.models import Business
from apis.business.serializers import BusinessSerializer, BusinessUpdateSerializer


class BusinessAPIView(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'patch']
    queryset = Business.objects.all()

    def perform_create(self, serializer):
        serializer.save(account_id=self.request.user.account_id)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return BusinessUpdateSerializer
        else:
            return BusinessSerializer

    def get_queryset(self):
        if self.request.user.is_client is True:
            query = Business.objects.filter(account_id=self.request.user.account_id)
        else:
            query = self.queryset
        return query

