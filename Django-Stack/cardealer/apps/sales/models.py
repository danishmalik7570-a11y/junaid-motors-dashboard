from django.db import models
import django.utils.timezone


class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('installment', 'Installment'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('pending', 'Pending'),
    ]

    invoice_no = models.CharField(max_length=20, unique=True, blank=True)
    car = models.ForeignKey('inventory.Car', on_delete=models.PROTECT)
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT)
    sale_date = models.DateField(default=django.utils.timezone.now, verbose_name="Sale Date")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash', verbose_name="Sale Type")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash', verbose_name="Payment Method")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="Payment Status")
    video = models.FileField(upload_to='sale_videos/', blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Sale Price")
    payment_received = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Payment Received")
    down_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Down Payment")
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Installment Amount")
    installment_months = models.IntegerField(default=0, verbose_name="Total Installments")
    profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Property Aliases & Derived Fields
    @property
    def total_sale_price(self):
        return self.total_amount

    @property
    def total_installments(self):
        return self.installment_months

    @property
    def installment_amount(self):
        return self.monthly_installment

    @property
    def installments_paid(self):
        if not self.pk:
            return 0
        return self.installment_set.filter(status='paid').count()

    @property
    def paid_installments_count(self):
        return self.installments_paid

    @property
    def paid_installments_amount(self):
        if not self.pk:
            return 0
        from django.db.models import Sum
        val = self.installment_set.filter(status='paid').aggregate(Sum('amount'))['amount__sum']
        return val or 0

    @property
    def installments_remaining(self):
        if self.payment_type == 'cash':
            return 0
        rem = self.installment_months - self.installments_paid
        return rem if rem > 0 else 0

    @property
    def remaining_installments_count(self):
        return self.installments_remaining

    @property
    def total_paid_amount(self):
        calc_paid = (self.down_payment or 0) + self.paid_installments_amount
        if self.payment_type == 'cash':
            return self.payment_received if self.payment_received > 0 else self.total_amount
        return max(self.payment_received or 0, calc_paid)

    @property
    def remaining_balance(self):
        rem = self.total_amount - self.total_paid_amount
        return rem if rem > 0 else 0

    @property
    def next_installment_due_date(self):
        if not self.pk:
            return None
        next_inst = self.installment_set.filter(status__in=['pending', 'overdue']).order_by('due_date').first()
        return next_inst.due_date if next_inst else None


    @property
    def paid_percentage(self):
        if not self.total_amount or self.total_amount == 0:
            return 100.0
        pct = (float(self.total_paid_amount) / float(self.total_amount)) * 100
        return min(round(pct, 1), 100.0)

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            last = Sale.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.invoice_no = f"INV-{num:05d}"
        if self.car_id:
            self.profit = self.total_amount - self.car.purchase_price
        
        # Default payment_received calculations
        if self.payment_type == 'cash' and (not self.payment_received or self.payment_received == 0):
            self.payment_received = self.total_amount
        elif self.payment_type == 'installment' and (not self.payment_received or self.payment_received == 0):
            self.payment_received = (self.down_payment or 0) + self.paid_installments_amount

        # Automatic payment status update based on balance
        total_paid = self.total_paid_amount
        if total_paid >= self.total_amount and self.total_amount > 0:
            self.payment_status = 'paid'
        elif total_paid > 0:
            self.payment_status = 'partially_paid'
        else:
            self.payment_status = 'pending'

        super().save(*args, **kwargs)
        if self.car_id:
            self.car.status = 'sold'
            self.car.save()

    def __str__(self):
        return f"{self.invoice_no} - {self.car.name if self.car_id else ''} to {self.customer.name if self.customer_id else ''}"

