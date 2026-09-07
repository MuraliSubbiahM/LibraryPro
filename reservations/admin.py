from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "book",
        "status",
        "reserved_at",
        "due_date",
        "renewal_count",
    )

    list_filter = ("status",)
    search_fields = ("user__username", "book__title")