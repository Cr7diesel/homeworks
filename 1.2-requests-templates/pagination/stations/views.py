from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import csv


def index(request):
    return redirect(reverse('bus_stations'))


with open('data-398-2018-08-30.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = []
    for row in reader:
        res = {
            'Name': row['Name'],
            'Street': row['Street'],
            'District': row['District']
        }
        data.append(res)


def bus_stations(request):
    current_page = int(request.GET.get('page', 1))
    paginator = Paginator(data, 10)
    page = paginator.get_page(current_page)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
