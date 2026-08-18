from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
import random

from apps.inventory.models import Car
from apps.customers.models import Customer
from apps.sales.models import Sale
from apps.purchases.models import Purchase
from apps.installments.models import Installment
from apps.leads.models import Lead


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        if Car.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists. Skipping.'))
            return

        cars_data = [
            {'name': 'Toyota Corolla', 'model_year': 2022, 'color': 'Pearl White', 'registration_no': 'ABC-001', 'purchase_price': 3800000, 'selling_price': 4200000, 'status': 'available'},
            {'name': 'Honda Civic', 'model_year': 2023, 'color': 'Lunar Silver', 'registration_no': 'ABC-002', 'purchase_price': 5200000, 'selling_price': 5700000, 'status': 'available'},
            {'name': 'Suzuki Alto', 'model_year': 2021, 'color': 'Cerulean Blue', 'registration_no': 'ABC-003', 'purchase_price': 1500000, 'selling_price': 1750000, 'status': 'available'},
            {'name': 'Toyota Fortuner', 'model_year': 2022, 'color': 'Phantom Brown', 'registration_no': 'ABC-004', 'purchase_price': 8500000, 'selling_price': 9200000, 'status': 'available'},
            {'name': 'Hyundai Tucson', 'model_year': 2023, 'color': 'Midnight Black', 'registration_no': 'ABC-005', 'purchase_price': 6800000, 'selling_price': 7400000, 'status': 'reserved'},
            {'name': 'Honda City', 'model_year': 2020, 'color': 'Radiant Red', 'registration_no': 'ABC-006', 'purchase_price': 2800000, 'selling_price': 3100000, 'status': 'sold'},
            {'name': 'Suzuki Swift', 'model_year': 2021, 'color': 'Champion Yellow', 'registration_no': 'ABC-007', 'purchase_price': 2100000, 'selling_price': 2400000, 'status': 'sold'},
            {'name': 'Toyota Camry', 'model_year': 2022, 'color': 'Graphite Gray', 'registration_no': 'ABC-008', 'purchase_price': 7200000, 'selling_price': 7900000, 'status': 'available'},
            {'name': 'KIA Sportage', 'model_year': 2023, 'color': 'Clear White', 'registration_no': 'ABC-009', 'purchase_price': 7800000, 'selling_price': 8500000, 'status': 'under_repair'},
            {'name': 'MG HS', 'model_year': 2023, 'color': 'Dover White', 'registration_no': 'ABC-010', 'purchase_price': 7600000, 'selling_price': 8300000, 'status': 'available'},
        ]

        cars = []
        today = date.today()
        for data in cars_data:
            entry_offset = random.randint(1, 45)
            car = Car(**data, entry_date=today - timedelta(days=entry_offset) if entry_offset > 3 else today)
            car.save()
            cars.append(car)
            self.stdout.write(f'  Created car: {car.name}')

        customers_data = [
            {'name': 'Ahmad Ali Khan', 'cnic': '42201-1234567-1', 'phone': '0300-1234567', 'address': 'House 12, Block A, Gulshan', 'city': 'Karachi'},
            {'name': 'Muhammad Usman', 'cnic': '42301-2345678-2', 'phone': '0333-2345678', 'address': 'Flat 4, DHA Phase 5', 'city': 'Lahore'},
            {'name': 'Sara Malik', 'cnic': '42101-3456789-3', 'phone': '0321-3456789', 'address': 'Street 7, F-8', 'city': 'Islamabad'},
            {'name': 'Bilal Ahmed', 'cnic': '42401-4567890-4', 'phone': '0312-4567890', 'address': 'Plot 23, Bahria Town', 'city': 'Rawalpindi'},
            {'name': 'Fatima Sheikh', 'cnic': '42501-5678901-5', 'phone': '0345-5678901', 'address': 'Sector G-11, Street 3', 'city': 'Karachi'},
        ]

        customers = []
        for data in customers_data:
            customer = Customer.objects.create(**data)
            customers.append(customer)
            self.stdout.write(f'  Created customer: {customer.name}')

        sold_cars = [c for c in cars if c.status == 'sold']
        for i, car in enumerate(sold_cars):
            customer = customers[i % len(customers)]
            Purchase.objects.create(
                car=car,
                seller_name=f'Dealer {i+1}',
                seller_phone=f'0300-000000{i}',
                purchase_price=car.purchase_price,
                dealer_commission=50000,
                purchase_date=today - timedelta(days=random.randint(10, 60)),
            )

            sale = Sale(
                car=car,
                customer=customer,
                payment_type='installment' if i == 0 else 'cash',
                total_amount=car.selling_price,
                down_payment=car.selling_price * 2 // 10 if i == 0 else 0,
                monthly_installment=car.selling_price // 12 if i == 0 else 0,
                installment_months=12 if i == 0 else 0,
            )
            sale.save()
            self.stdout.write(f'  Created sale: {sale.invoice_no}')

            if sale.payment_type == 'installment':
                for month in range(1, 13):
                    due = today - timedelta(days=30) + timedelta(days=30 * month)
                    status = 'paid' if month <= 2 else ('overdue' if due < today else 'pending')
                    Installment.objects.create(
                        sale=sale,
                        customer=customer,
                        installment_no=month,
                        due_date=due,
                        amount=sale.monthly_installment,
                        status=status,
                        paid_date=due if status == 'paid' else None,
                    )

        leads_data = [
            {'name': 'Zain ul Abideen', 'phone': '0300-9999001', 'source': 'facebook', 'interested_car': 'Toyota Corolla 2023', 'budget': 4500000, 'status': 'new'},
            {'name': 'Ayesha Siddiqui', 'phone': '0333-8888002', 'source': 'whatsapp', 'interested_car': 'Honda Civic', 'budget': 5800000, 'status': 'followup', 'next_followup': today + timedelta(days=2)},
            {'name': 'Omar Farooq', 'phone': '0321-7777003', 'source': 'walkin', 'interested_car': 'Toyota Fortuner', 'budget': 9500000, 'status': 'testdrive'},
            {'name': 'Hina Butt', 'phone': '0312-6666004', 'source': 'referral', 'interested_car': 'Suzuki Alto', 'budget': 1900000, 'status': 'negotiating'},
            {'name': 'Tariq Mehmood', 'phone': '0345-5555005', 'source': 'phone', 'interested_car': 'KIA Sportage', 'budget': 8800000, 'status': 'converted'},
            {'name': 'Nadia Hassan', 'phone': '0300-4444006', 'source': 'facebook', 'interested_car': 'Hyundai Tucson', 'budget': 7500000, 'status': 'new'},
        ]

        for data in leads_data:
            Lead.objects.create(**data)
            self.stdout.write(f'  Created lead: {data["name"]}')

        self.stdout.write(self.style.SUCCESS('\n✓ Sample data seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('  Login: admin / admin123'))
