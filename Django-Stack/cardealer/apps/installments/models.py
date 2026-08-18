from django.db import models


class Installment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    sale = models.ForeignKey('sales.Sale', on_delete=models.CASCADE)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    installment_no = models.IntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    paid_date = models.DateField(blank=True, null=True)
    late_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def check_overdue(self):
        from django.utils import timezone
        if self.status == 'pending' and self.due_date < timezone.now().date():
            self.status = 'overdue'
            self.save()

    @property
    def voucher_no(self):
        return f"VCH-INST-{self.id:05d}"

    @property
    def remaining_balance_after(self):
        sale = self.sale
        paid_installments = sale.installment_set.filter(
            models.Q(status='paid') | models.Q(pk=self.pk)
        )
        from django.db.models import Sum
        sum_paid = paid_installments.aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = (sale.down_payment or 0) + sum_paid
        rem = sale.total_amount - total_paid
        return rem if rem > 0 else 0

    @property
    def remaining_count_after(self):
        sale = self.sale
        paid_count = sale.installment_set.filter(
            models.Q(status='paid') | models.Q(pk=self.pk)
        ).count()
        rem = sale.installment_months - paid_count
        return rem if rem > 0 else 0

    def __str__(self):
        return f"Installment #{self.installment_no} - {self.customer.name}"
