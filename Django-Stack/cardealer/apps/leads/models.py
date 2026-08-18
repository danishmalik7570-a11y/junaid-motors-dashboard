from django.db import models


class Lead(models.Model):
    SOURCE_CHOICES = [
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
        ('walkin', 'Walk-in'),
        ('referral', 'Referral'),
        ('phone', 'Phone Call'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('followup', 'Follow-up'),
        ('testdrive', 'Test Drive'),
        ('negotiating', 'Negotiating'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    interested_car = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True)
    next_followup = models.DateField(blank=True, null=True)
    test_drive_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.interested_car} ({self.status})"
