from django.shortcuts import render
from django.utils import timezone

from catalog.models import Book
from reservations.models import Reservation


def dashboard(request):
    today = timezone.localdate()

   
    total_books = Book.objects.count()

    total_copies = sum(
        book.total_copies
        for book in Book.objects.all()
    )

    available_copies = sum(
        book.available_copies
        for book in Book.objects.all()
    )

    borrowed_books = total_copies - available_copies


    active_reservations = Reservation.objects.filter(
        status__in=["RESERVED", "BORROWED"]
    ).count()

    

    overdue_books = Reservation.objects.filter(
        status="BORROWED",
        due_date__lt=today
    ).select_related("user", "book")

    overdue_count = overdue_books.count()

    

    context = {
        "total_books": total_books,
        "total_copies": total_copies,
        "available_copies": available_copies,
        "borrowed_books": borrowed_books,
        "total_reservations": active_reservations,
        "overdue_count": overdue_count,
        "overdue_books": overdue_books,
    }

    return render(
        request,
        "analytics/dashboard.html",
        context
    )