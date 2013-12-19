from django.shortcuts import render
from mailme.web.forms import RegisterForm


def index(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # register
            pass
    else:
        form = RegisterForm()
    return render(request, 'mailme/web/index.html', {
        'form': form
    })
