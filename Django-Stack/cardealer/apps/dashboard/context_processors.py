from django.db.models import Q
from django.utils import timezone
from apps.installments.models import Installment


def overdue_count(request):
    if request.user.is_authenticated:
        today = timezone.now().date()
        count = Installment.objects.filter(
            Q(status='overdue') | Q(status='pending', due_date__lt=today)
        ).count()
        return {'overdue_count': count}
    return {'overdue_count': 0}
