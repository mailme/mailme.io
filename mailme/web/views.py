from functools import wraps
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse


def login_required(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated():
            request.session['_next'] = request.get_full_path()
            return redirect('mailme-home')
        return func(request, *args, **kwargs)
    return wrapped


def home(request):
    """Home view, displays login mechanism"""
    return render(request, 'mailme/web/home.html', {
    })


@login_required
def account(request):
    """Login complete view, displays user data"""
    return render(request, 'mailme/web/account.html', {
        'user': request.user,
    })


@login_required
def login_redirect(request):
    default = reverse('mailme-home')
    login_url = request.session.pop('_next', None) or default
    if '//' in login_url:
        login_url = default
    elif login_url.startswith(reverse('mailme-login')):
        login_url = default
    return redirect(login_url)


def logout(request):
    from django.contrib.auth import logout

    logout(request)

    return redirect('mailme-home')
