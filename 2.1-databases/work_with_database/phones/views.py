from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sorted_result = request.GET.get('sort')
    if sorted_result == 'name':
        phones = Phone.objects.order_by('name')
    elif sorted_result == 'min_price':
        phones = Phone.objects.order_by('price')
    elif sorted_result == 'max_price':
        phones = Phone.objects.order_by('-price')
    else:
        phones = Phone.objects.all()
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phones = request.GET.get(slug=slug)
    context = {'phones': phones}
    return render(request, template, context)
