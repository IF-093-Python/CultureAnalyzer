from django.shortcuts import render


def index(request):
    return render(request, 'users/index.html', context={
        'is_user_authenticated': True,
        'username': 'Vasya',
        'user_role': 'admin'
    })
