import decimal, csv

from django.contrib import admin
from django.http import HttpResponse
from django.db.models import F

from .models import Book


def export_books(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Publication Date', 'Author', 'Price', 'Pages', 'Book Type'])
    books = queryset.values_list('title', 'publication_date', 'author', 'price', 'pages', 'book_type')
    for book in books:
        writer.writerow(book)
    return response
export_books.short_description = 'Export to csv'


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_date', 'author', 'price', 'book_type']
    actions = ['apply_discount', export_books, 'increase_price']

    def apply_discount(self, request, venkatesh):
        venkatesh.update(price=F('price') * decimal.Decimal('0.9'))
    apply_discount.short_description = 'Apply 10%% discount'

    def increase_price(self, request, queryset):
        queryset.update(price=F('price') * decimal.Decimal('1.1'))
    increase_price.short_description = 'Increse 10%% On total price'



admin.site.register(Book, BookAdmin)
