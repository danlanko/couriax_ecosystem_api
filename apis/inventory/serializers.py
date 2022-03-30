from rest_framework import serializers
from .models import InventoryLog
from .utils import InventoryAction


def quantity_depletion(is_in, product, qty, is_system, remark, user=None):
    is_in = is_in
    previous_qty = product.stock_unit
    if is_system:
        remark = "Sales depletion"
    if is_in:
        stock_unit = product.stock_unit + qty
    else:
        stock_unit = product.stock_unit - qty
    product.stock_unit = stock_unit
    product.save()
    inventory_log = InventoryLog.objects.create(
        product=product,
        business=product.business,
        quantity=qty,
        previous_qty=previous_qty,
        is_in=is_in,
        remark=remark,
        performed_by=user,
        is_system=is_system
    )
    inventory_log.save()
    return inventory_log


class InventoryLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryLog
        fields = "__all__"

    def create(self, validated_data):
        inventory_action = InventoryAction(
            is_system=False,
            product=validated_data['product'],
            is_in=validated_data["is_in"],
            qty=validated_data['quantity'],
            remark=validated_data["remark"],
            user=self.context["request"].user
        )
        inventory_action.quantity_depletion()
        return validated_data

