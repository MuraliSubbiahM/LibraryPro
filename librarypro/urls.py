from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analytics/', include('analytics.urls')),
    path("", include("catalog.urls")),
    path("reservations/", include("reservations.urls")),
]