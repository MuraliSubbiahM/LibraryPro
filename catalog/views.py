from django.db.models import Q
from django.shortcuts import render
from .models import Book, Category


def book_list(request):
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()

    books = Book.objects.select_related("category").all()

    # Search by title, author, or ISBN
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    # Filter by category
    if category_id:
        books = books.filter(category_id=category_id)

    categories = Category.objects.all().order_by("name")

    return render(
        request,
        "catalog/book_list.html",
        {
            "books": books,
            "categories": categories,
            "query": query,
            "selected_category": category_id,
        },
    )