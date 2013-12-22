from django.shortcuts import render
from mailme.web.forms import RegisterForm
from mailme.core.models import User


def index(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("valid")
    else:
        form = RegisterForm()
    return render(request, 'mailme/web/index.html', {
        'form': form
    })
