from django.contrib import admin
from .models import Book, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'isbn',
        'category',
        'total_copies',
        'available_copies'
    )

    search_fields = ('title', 'author', 'isbn')
    list_filter = ('category',)