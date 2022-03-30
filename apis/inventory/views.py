from rest_framework import generics
from .models import InventoryLog
from .serializers import InventoryLogSerializer
# Create your views here.


class InventoryLogAPIView(generics.ListCreateAPIView):
    queryset = InventoryLog.objects.all()
    serializer_class = InventoryLogSerializer

    def get_queryset(self):
        query = self.queryset
        if self.request.user.user_type == "client_admin":
            if "business_id" in self.request.query_params:
                query = query.filter(business_id=self.request.query_params.get("business_id", None))
            else:
                query = query.filter(product__business__account_id=self.request.user.account_id)
        elif self.request.user.user_type == "client":
            query = query.filter(business_id=self.request.user.business_id)
        else:
            query = self.queryset
        return query
