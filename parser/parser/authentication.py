from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.shortcuts import render, redirect
from rest_framework.response import Response
import rest_framework.status as status

class SecretKeyAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        SessionMiddleware(self.get_response).process_request(request)

        if request.session.get('is_authenticated'):
            return self.get_response(request)
        
        secret_key = request.POST.get('secret_key') or request.GET.get('secret_key')

        if secret_key and secret_key == settings.AUTH_KEY:
            request.session['is_authenticated'] = True
            return redirect('home_page')
        if secret_key == None:
            context = None
        if secret_key and not secret_key == settings.AUTH_KEY:
            context = {'wrong_key': 'The key is wrong, try again!'}
        
        return render(request, 'not_authenticated.html', context=context)


        