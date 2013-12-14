from django.shortcuts import render


def index(request):
    return render(request, 'mailme/web/index.html')
