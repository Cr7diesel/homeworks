from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    book = Book.objects.all()
    template = 'books/books_list.html'
    context = {'books': book}
    return render(request, template, context)


def book_page(request, date):
    template = 'books/books_list.html'

    book_pages = [book['pub_date'] for book in Book.objects.order_by('pub_date').values('pub_date').distinct()]

    paginator = Paginator(book_pages, 1)
    index = book_pages.index(date)
    page = paginator.get_page(index + 1)

    books = Book.objects.filter(pub_date=date)
    context = {
        'next_date': book_pages[index + 1] if page.has_next() else None,
        'previous_date': book_pages[index - 1] if page.has_previous() else None,
        'page': page,
        'books': books
    }

    return render(request, template, context)
