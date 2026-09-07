from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from catalog.models import Book
from .models import Reservation


@login_required
def reserve_book(request, book_id):
    if request.method != "POST":
        return redirect("book_list")

    with transaction.atomic():
        book = get_object_or_404(Book, id=book_id)

        already_reserved = Reservation.objects.filter(
            user=request.user,
            book=book,
            status__in=["RESERVED", "BORROWED"]
        ).exists()

        if already_reserved:
            messages.warning(
                request,
                "You already have an active reservation for this book."
            )
            return redirect("book_list")

        if book.available_copies <= 0:
            messages.error(
                request,
                "Sorry, this book is currently unavailable."
            )
            return redirect("book_list")

        Reservation.objects.create(
            user=request.user,
            book=book,
            status="RESERVED"
        )

        book.available_copies -= 1
        book.save(update_fields=["available_copies"])

    messages.success(
        request,
        f'"{book.title}" has been reserved successfully.'
    )

    return redirect("book_list")


@login_required
def renew_book(request, reservation_id):
    if request.method != "POST":
        return redirect("book_list")

    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user,
        status="BORROWED"
    )

    if reservation.renewal_count >= 2:
        messages.error(
            request,
            "This book has already reached the maximum renewal limit."
        )
        return redirect("my_reservations")

    if reservation.due_date is None:
        reservation.due_date = timezone.now().date()

    reservation.due_date += timedelta(days=7)
    reservation.renewal_count += 1

    reservation.save(
        update_fields=["due_date", "renewal_count"]
    )

    messages.success(
        request,
        f'"{reservation.book.title}" has been renewed successfully.'
    )

    return redirect("my_reservations")


@login_required
def borrow_book(request, reservation_id):
    if request.method != "POST":
        return redirect("my_reservations")

    with transaction.atomic():
        reservation = get_object_or_404(
            Reservation,
            id=reservation_id,
            user=request.user,
            status="RESERVED"
        )

        reservation.status = "BORROWED"
        reservation.due_date = timezone.now().date() + timedelta(days=14)

        reservation.save(
            update_fields=["status", "due_date"]
        )

    messages.success(
        request,
        f'"{reservation.book.title}" has been borrowed successfully.'
    )

    return redirect("my_reservations")


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(
        user=request.user
    ).select_related("book").order_by("-reserved_at")

    return render(
        request,
        "reservations/my_reservations.html",
        {
            "reservations": reservations,
        }
    )