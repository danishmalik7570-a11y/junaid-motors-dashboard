from django.db import models


class Purchase(models.Model):
    car = models.OneToOneField('inventory.Car', on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=200)
    seller_phone = models.CharField(max_length=20)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    dealer_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    document = models.FileField(upload_to='purchase_docs/', blank=True, null=True)
    purchase_date = models.DateField()
    notes = models.TextField(blank=True)

    def net_cost(self):
        return self.purchase_price + self.dealer_commission

    def __str__(self):
        return f"Purchase: {self.car.name} from {self.seller_name}"
