from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import MyForm
from .models import CustomUser


def signup_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            us = form.save()
            user_password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            user = CustomUser.objects.all().filter(username=username)
            user.update(user_password=user_password, is_staff=True)
            us.groups.add(Group.objects.get(name='Партнеры'))
            return redirect('/app_crypto/customuser/')
    else:
        form = MyForm()
    return render(request, 'sign_up.html', {'form': form})
