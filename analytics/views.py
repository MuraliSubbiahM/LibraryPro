from django.shortcuts import render


def dashboard(request):
    context = {
        'total_books': 0,
        'available_books': 0,
        'total_reservations': 0,
        'borrowed_books': 0,
        'overdue_count': 0,
        'overdue_books': [],
    }

    return render(request, 'analytics/dashboard.html', context)