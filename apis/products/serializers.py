from rest_framework import serializers
from apis.products.models import Category, SubCategory, Supplier, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = "__all__"

    def create(self, validated_data):
        category = validated_data['category']
        business_id = category.business_id
        sub_cat = SubCategory(**validated_data, business_id=business_id)
        sub_cat.save()
        return validated_data


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = "__all__"

    def create(self, validated_data):
        category = validated_data['category']
        instance = Supplier(**validated_data, business_id=category.business_id,
                            account_id=self.context['request'].user.account_id)
        instance.save()
        return validated_data


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ('sku', 'business')

    @staticmethod
    def generate_sku(business):
        from apis.helpers.utils import generate_product_sku
        sku = generate_product_sku(8)
        x = 0
        while True:
            if x == 0:
                try:
                    Product.objects.get(sku=sku, business=business)
                except Product.DoesNotExist:
                    return str(sku)
            else:
                new_sku = generate_product_sku(8)
                try:
                    Product.objects.get(sku=new_sku, business=business)
                except Product.DoesNotExist:
                    return str(new_sku)
            x += 1
            if x > 10:
                raise Exception("Generating SKU error. Please contact admin.")

    def create(self, validated_data):
        category = validated_data['category']
        instance = Product(**validated_data, business_id=category.business_id,
                           sku=self.generate_sku(category.business))
        instance.save()
        return validated_data


class ProductImageSerializer(serializers.ModelSerializer):
    """Separate Serializer to handle upload of file"""

    class Meta:
        """Class Meta"""
        model = Product
        fields = ['image', ]
