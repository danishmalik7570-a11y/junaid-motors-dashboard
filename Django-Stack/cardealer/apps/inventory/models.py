from django.db import models


class Car(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
        ('under_repair', 'Under Repair'),
    ]
    name = models.CharField(max_length=200)
    model_year = models.IntegerField()
    color = models.CharField(max_length=100)
    registration_no = models.CharField(max_length=50, unique=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    video = models.FileField(upload_to='car_videos/', blank=True, null=True)
    entry_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def profit_margin(self):
        return self.selling_price - self.purchase_price

    def days_in_stock(self):
        from django.utils import timezone
        return (timezone.now().date() - self.entry_date).days

    def __str__(self):
        return f"{self.name} ({self.model_year}) - {self.registration_no}"


class CarRepair(models.Model):
    REPAIR_STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('pending_parts', 'Pending Parts'),
        ('completed', 'Completed'),
    ]
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='repairs')
    workshop_name = models.CharField(max_length=200)
    work_description = models.TextField(help_text="Details of repair or maintenance work")
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    completion_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=REPAIR_STATUS_CHOICES, default='in_progress')
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status in ['in_progress', 'pending_parts']:
            self.car.status = 'under_repair'
            self.car.save()
        elif self.status == 'completed':
            open_repairs = CarRepair.objects.filter(car=self.car, status__in=['in_progress', 'pending_parts']).exclude(pk=self.pk)
            if not open_repairs.exists() and self.car.status == 'under_repair':
                self.car.status = 'available'
                self.car.save()

    def __str__(self):
        return f"Repair: {self.car.name} @ {self.workshop_name} ({self.get_status_display()})"


class CarRent(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals')
    date = models.DateField(help_text="Rental Date")
    city = models.CharField(max_length=150, help_text="Destination / City")
    total_rent = models.DecimalField(max_digits=12, decimal_places=2, help_text="Total Rent Amount (PKR)")
    petrol_expense = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Petrol Expense (PKR)")
    total_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Total Profit (PKR)")
    notes = models.TextField(blank=True, help_text="Additional rental notes")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.total_profit:
            rent_val = float(self.total_rent or 0)
            petrol_val = float(self.petrol_expense or 0)
            self.total_profit = rent_val - petrol_val
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rent #{self.pk}: {self.car.name} ({self.city}) — {self.date}"



