from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


def favicon(request):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#F59E0B"/><circle cx="10" cy="22" r="3" fill="#0A0B0F"/><circle cx="22" cy="22" r="3" fill="#0A0B0F"/><rect x="4" y="14" width="24" height="8" rx="2" fill="#0A0B0F"/><rect x="7" y="10" width="18" height="6" rx="2" fill="#0A0B0F"/></svg>'
    return HttpResponse(svg, content_type='image/svg+xml')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', favicon),
    path('', RedirectView.as_view(url='/dashboard/')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('sales/', include('apps.sales.urls')),
    path('purchases/', include('apps.purchases.urls')),
    path('customers/', include('apps.customers.urls')),
    path('installments/', include('apps.installments.urls')),
    path('leads/', include('apps.leads.urls')),
    path('staff/', include('apps.staff.urls')),
    path('reports/', include('apps.reports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
