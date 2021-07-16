from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.models import User
from .my_logic import HarrisBededictEquation, NutritionalValues
from .models import Profile


@login_required
def dashboard(request):

    nutritional_values = NutritionalValues(request.user.profile.daily_calory_limit)
    request.user.profile.limit_carb = nutritional_values.carb_value()
    request.user.profile.limit_prot = nutritional_values.prot_value()
    request.user.profile.limit_fat = nutritional_values.fat_value()

    days = request.user.profile.time

    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'days': days,
                   'limit_carb':request.user.profile.limit_carb,
                   'limit_prot': request.user.profile.limit_prot,
                   'limit_fat': request.user.profile.limit_fat,
                   'daily_calory_limit':request.user.profile.daily_calory_limit,
                   })

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
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
        person = request.user.profile

        calculate = HarrisBededictEquation(person.gender, person.age, person.weight, person.height,
                                           person.physical_activity, person.new_weight, person.time)
        tder = calculate.total_daily_energy_requirement()
        bm = calculate.basic_metabolism()
        dd_dcl = calculate.calculate_deficit()
        person.daily_calory_limit = dd_dcl[1]
        person.save()
        def_percent = calculate.is_deficit_to_big()

    else:
        profile_form = ProfileForm(instance=request.user.profile)
        person = request.user.profile

        calculate = HarrisBededictEquation(person.gender, person.age, person.weight, person.height,
                                           person.physical_activity, person.new_weight, person.time)
        tder = calculate.total_daily_energy_requirement()
        bm = calculate.basic_metabolism()
        dd_dcl = calculate.calculate_deficit()
        person.daily_calory_limit = dd_dcl[1]
        def_percent = calculate.is_deficit_to_big()


    return render(request,
                  'account/settings.html',
                  {'profile_form': profile_form,
                   'tder':tder,
                   'bm':bm,
                   'dd':dd_dcl[0],
                   'dcl': dd_dcl[1],
                   'dw' : dd_dcl[2],
                   'time': person.time,
                   'def_percent': def_percent,
                   'weight': person.weight,
                   'new_weight': person.new_weight,
                   })


