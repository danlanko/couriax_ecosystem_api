from rest_framework import viewsets, serializers, generics
from .models import Category, SubCategory, Supplier, Product
from .serializers import CategorySerializer, SubCategorySerializer, SupplierSerializer, ProductSerializer, \
    ProductImageSerializer


class CategoryAPIView(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'patch', 'options']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.request.user.user_type == 'client_admin':
            if "business_id" in self.request.query_params:
                query = Category.objects.filter(business_id=self.request.query_params.get("business_id", None))
            else:
                query = Category.objects.filter(business__account_id=self.request.user.account_id)
        elif self.request.user.user_type == 'client':
            query = Category.objects.filter(business_id=self.request.user.business_id)
        else:
            query = self.queryset
        return query


class SubCategoryAPIView(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'patch']
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        if "category_id" in self.request.query_params:
            query = SubCategory.objects.filter(category_id=self.request.query_params.get('category_id', None))
        else:
            query = SubCategory.objects.filter(category__business__account_id=self.request.user.account_id)

        return query


class SupplierAPIView(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'patch']
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get_queryset(self):
        if self.request.user.user_type == "client_admin":
            if "business_id" in self.request.query_params:
                query = Supplier.objects.filter(business_id=self.request.query_params.get('business_id', None))
            else:
                query = Supplier.objects.filter(account_id=self.request.user.account_id)
        elif self.request.user.user_type == 'staff':
            query = self.queryset
            if "business_id" in self.request.query_params:
                query = query.filter(business_id=self.request.query_params.get('category_id', None))
        else:
            raise serializers.ValidationError({
                "error": "You are not allowed to perform this action"
            })
        if "category_id" in self.request.query_params:
            query = query.filter(category_id=self.request.query_params.get('category_id', None))
        return query


class ProductAPIView(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'patch']
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.queryset
        if "category_id" in self.request.query_params:
            query = query.filter(category_id=self.request.query_params.get("category_id", None))
        if "sub_category_id" in self.request.query_params:
            query = query.filter(sub_category_id=self.request.query_params.get("sub_category_id", None))
        if "business_id" in self.request.query_params:
            query = query.filter(business_id=self.request.query_params.get("business_id", None))

        return query


class ProductImagesAPIView(generics.UpdateAPIView):
    """Product Image """
    http_method_names = ['put']
    serializer_class = ProductImageSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

