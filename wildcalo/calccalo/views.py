from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.models import User
from .my_logic import HarrisBededictEquation


@login_required
def dashboard(request):

    days = request.user.profile.time
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'days': days})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

@login_required
def settings(request):
    if request.method == 'POST':
        profile_form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()



    else:
        profile_form = ProfileForm(instance=request.user.profile)
        person = request.user.profile

        calculate = HarrisBededictEquation(person.gender, person.age, person.weight, person.height,
                                           person.physical_activity, person.new_weight, person.time)
        calculate.total_daily_energy_requirement()

        print(request.user.profile.gender, request.user.profile.age, request.user.profile.physical_activity, )

    return render(request,
                  'account/settings.html',
                  {'profile_form': profile_form})


