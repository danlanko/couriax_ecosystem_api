from apis.inventory.models import InventoryLog


class InventoryAction:

    def __init__(self, product, is_in, qty, is_system, remark, user=None):
        self.product = product
        self.is_in = is_in
        self.qty = qty
        self.is_system = is_system
        self.remark = remark
        self.user = user

    def quantity_depletion(self):
        previous_qty = self.product.stock_unit
        if self.is_system:
            self.remark = "Sales depletion"
        if self.is_in:
            stock_unit = self.product.stock_unit + self.qty
        else:
            stock_unit = self.product.stock_unit - self.qty
        self.product.stock_unit = stock_unit
        self.product.save()
        inventory_log = InventoryLog.objects.create(
            product=self.product,
            business=self.product.business,
            quantity=self.qty,
            previous_qty=previous_qty,
            is_in=self.is_in,
            remark=self.remark,
            performed_by=self.user,
            is_system=self.is_system
        )
        inventory_log.save()
        return inventory_log