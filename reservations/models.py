from django.db import models
from django.contrib.auth.models import User
from catalog.models import Book


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("RESERVED", "Reserved"),
        ("BORROWED", "Borrowed"),
        ("RETURNED", "Returned"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    reserved_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="RESERVED"
    )

    renewal_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"