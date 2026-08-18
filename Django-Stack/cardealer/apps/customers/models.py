from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    cnic = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_purchases(self):
        return self.sale_set.count()

    def pending_amount(self):
        return self.installment_set.filter(status__in=['pending', 'overdue']).aggregate(
            total=models.Sum('amount'))['total'] or 0

    def __str__(self):
        return f"{self.name} - {self.cnic}"


class KhattaEntry(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('lene_hain', 'Lene Hain (Receivable)'),
        ('dene_hain', 'Dene Hain (Payable)'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('settled', 'Settled / Paid'),
    ]

    name = models.CharField(max_length=200, help_text="Person / Customer Name (e.g. Ali Khan)")
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES, default='lene_hain', help_text="Lene Hain or Dene Hain")
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount in PKR")
    note = models.TextField(blank=True, help_text="Transaction description or remarks")
    date = models.DateField(help_text="Transaction Date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    settled_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_entry_type_display()} (Rs. {self.amount})"

