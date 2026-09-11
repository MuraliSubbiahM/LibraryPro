from django.urls import path
from . import views


urlpatterns = [
    path(
        "reserve/<int:book_id>/",
        views.reserve_book,
        name="reserve_book"
    ),

    path(
        "renew/<int:reservation_id>/",
        views.renew_book,
        name="renew_book"
    ),

    path(
        "borrow/<int:reservation_id>/",
        views.borrow_book,
        name="borrow_book"
    ),

    path(
        "my-reservations/",
        views.my_reservations,
        name="my_reservations"
    ),
]