from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, ProfileForm, BreakfastProductsForm, Breakfast2ProductsForm, \
    SnacksProductsForm, SupperProductsForm, DinnerProductsForm, LunchProductsForm, ProductsForm
from django.contrib.auth.models import User
from .my_logic import HarrisBededictEquation, NutritionalValues, create_meals
from .models import Profile, Products, MealsProducts, Meals
from django.http import HttpResponseRedirect
import datetime
from django.db.models import Sum
from django.http import JsonResponse
from .serializers import ProductsSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


@login_required
def dashboard(request):

    nutritional_values = NutritionalValues(request.user.profile.daily_calory_limit)
    request.user.profile.limit_carb = nutritional_values.carb_value()
    request.user.profile.limit_prot = nutritional_values.prot_value()
    request.user.profile.limit_fat = nutritional_values.fat_value()

    time = request.user.profile.time


    profile = request.user.profile

    profile.kcal = Meals.objects.filter(person=profile).aggregate(Sum('kcal'))['kcal__sum']
    profile.prot = Meals.objects.filter(person=profile).aggregate(Sum('carb'))['carb__sum']
    profile.carb = Meals.objects.filter(person=profile).aggregate(Sum('prot'))['prot__sum']
    profile.fat = Meals.objects.filter(person=profile).aggregate(Sum('fat'))['fat__sum']

    if (profile.kcal or profile.prot or  profile.carb or profile.fat) is None:
        profile.kcal = 0
        profile.prot = 0
        profile.carb = 0
        profile.fat = 0

    profile.save()


    if request.method == 'POST':
        profile.status = 'ongoing'
        today = datetime.date.today()
        profile.mem_today = today
        days_time = datetime.timedelta(days=time)
        end = today + days_time
        profile.end_date = end
        profile.days_left = abs((end - today).days)
        profile.save()

    if profile.days_left is not None:
        today = datetime.date.today()

        if profile.mem_today != today:

            meal = Meals.objects.filter(person=profile.id)
            meal.delete()
            profile.mem_today = today
            profile.save()
            return HttpResponseRedirect(request.path_info)

        profile.days_left = abs((profile.end_date - today).days)
        profile.save()

    if profile.days_left == 0 and profile.status == 'ongoing':
        profile.status = 'waiting'
        profile.time = None
        profile.weight = None
        profile.new_weight = None
        meal = Meals.objects.filter(person=profile.id)
        meal.delete()
        profile.kcal = 0
        profile.prot = 0
        profile.carb = 0
        profile.fat = 0
        profile.save()


    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'days': profile.days_left,
                   'limit_carb':request.user.profile.limit_carb,
                   'limit_prot': request.user.profile.limit_prot,
                   'limit_fat': request.user.profile.limit_fat,
                   'daily_calory_limit':request.user.profile.daily_calory_limit,
                   'kcal': profile.kcal,
                   'prot': profile.prot,
                   'carb': profile.carb,
                   'fat': profile.fat,
                   'person_status': profile.status,
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
        person.status = 'ready'
        meal = Meals.objects.filter(person=person.id)
        meal.delete()
        person.kcal = 0
        person.prot = 0
        person.carb = 0
        person.fat = 0
        person.save()
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


@login_required
def meals(request):

    profile = request.user.profile
    create_meals(profile) # functions creates a meals fater click add a meals.

    today = datetime.date.today()
    products = Products.objects.all()

    # forms for all single meals
    breakfast_form = BreakfastProductsForm(data=request.GET)
    breakfast2_form = Breakfast2ProductsForm(data=request.GET)
    lunch_form = LunchProductsForm(data=request.GET)
    dinner_form = DinnerProductsForm(data=request.GET)
    supper_form = SupperProductsForm(data=request.GET)
    snacks_form = SnacksProductsForm(data=request.GET)

    forms = [(breakfast_form,'breakfast','weightb', 'productb'), (breakfast2_form,'breakfast_2','weightb2', 'productb2'),
             (lunch_form, 'lunch','weightl', 'productl'), (dinner_form, 'dinner','weightd', 'productd'),
             (supper_form,'supper','weightsu', 'productsu'), (snacks_form, 'snacks','weightsn', 'productsn')]



    message=''

    if 'term' in request.GET:
        qs = Products.objects.filter(name__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            if product.active:
                titles.append(product.name)
        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)

    for form in forms: # this loop allows to shorten code
        if form[0].is_valid():
            weight = int(request.GET[form[2]])
            product_id = request.GET[form[3]].title()
            try:
                id_prod = Products.objects.get(name=product_id).id
                obj = Products.objects.get(pk=id_prod)

                if obj.active:

                    if weight <= 0:
                        message = "Sorry, weight is lower or equal 0, it does not make sense"
                        break

                    meal_id = Meals.objects.get(person=profile, name=form[1])

                    weight_to_add = weight
                    product_name_to_add = obj.name
                    kcal_to_add = round((weight / 100) * obj.kcal,1)
                    prot_to_add = round((weight / 100) * obj.prot, 1)
                    carb_to_add = round((weight / 100) * obj.carb, 1)
                    fat_to_add = round((weight / 100) * obj.fat, 1)

                    meal_id.kcal +=  kcal_to_add
                    meal_id.prot += prot_to_add
                    meal_id.carb += carb_to_add
                    meal_id.fat += fat_to_add
                    meal_id.save()

                    MealsProducts.objects.create(weight=weight_to_add, name=product_name_to_add, kcal=kcal_to_add,
                                                 prot=prot_to_add, carb=carb_to_add, fat=fat_to_add, meal_id=meal_id.id)

                    return HttpResponseRedirect(request.path_info)

                else:
                    message = "Sorry, the given product is not active now"


            # dodać do konkretnego posilku ale i do ogolnego kcal uzytkownika
            # suma kalorii itd zawsze powinna byc obliczana w czasie rzecyzwistym
            # ze wszystkich posiklow. Bo jak trzeba bedzie cos usunac to wtedy wystarycz usunac produkt i juz
            # nie mozna zapisywac wyniku do... bo pozniej ciezko bedzie to po


            except:
                message = "The given product is not on the list of available products"


    #Ta pętla i każda inna, która coś dodaje zmienić na pobieranie listy konkretnych wartosci np. wszystkie posiłki śniadanie i kcal. zastosować sum(lista)
    for meal in Meals.objects.filter(person=profile):
        meal.kcal = MealsProducts.objects.filter(meal=meal).aggregate(Sum('kcal'))['kcal__sum']
        meal.carb = MealsProducts.objects.filter(meal=meal).aggregate(Sum('carb'))['carb__sum']
        meal.prot = MealsProducts.objects.filter(meal=meal).aggregate(Sum('prot'))['prot__sum']
        meal.fat = MealsProducts.objects.filter(meal=meal).aggregate(Sum('fat'))['fat__sum']
        if (meal.kcal or meal.carb or meal.prot or meal.fat) is None:
            meal.kcal = 0
            meal.carb = 0
            meal.prot = 0
            meal.fat = 0
        meal.save()

    breakfast_kcal = round(Meals.objects.get(person=profile, name='breakfast').kcal,1)
    breakfast_carb = round(Meals.objects.get(person=profile, name='breakfast').carb,1)
    breakfast_prot = round(Meals.objects.get(person=profile, name='breakfast').prot,1)
    breakfast_fat = round(Meals.objects.get(person=profile, name='breakfast').fat,1)

    breakfast_2_kcal = round(Meals.objects.get(person=profile, name='breakfast_2').kcal,1)
    breakfast_2_carb = round(Meals.objects.get(person=profile, name='breakfast_2').carb,1)
    breakfast_2_prot = round(Meals.objects.get(person=profile, name='breakfast_2').prot,1)
    breakfast_2_fat = round(Meals.objects.get(person=profile, name='breakfast_2').fat,1)

    dinner_kcal = round(Meals.objects.get(person=profile, name='dinner').kcal,1)
    dinner_carb = round(Meals.objects.get(person=profile, name='dinner').carb,1)
    dinner_prot = round(Meals.objects.get(person=profile, name='dinner').prot,1)
    dinner_fat = round(Meals.objects.get(person=profile, name='dinner').fat,1)

    lunch_kcal = round(Meals.objects.get(person=profile, name='lunch').kcal,1)
    lunch_carb = round(Meals.objects.get(person=profile, name='lunch').carb,1)
    lunch_prot = round(Meals.objects.get(person=profile, name='lunch').prot,1)
    lunch_fat = round(Meals.objects.get(person=profile, name='lunch').fat,)

    supper_kcal = round(Meals.objects.get(person=profile, name='supper').kcal,1)
    supper_carb = round(Meals.objects.get(person=profile, name='supper').carb,1)
    supper_prot = round(Meals.objects.get(person=profile, name='supper').prot,1)
    supper_fat = round(Meals.objects.get(person=profile, name='supper').fat,1)

    snacks_kcal = round(Meals.objects.get(person=profile, name='snacks').kcal,1)
    snacks_carb = round(Meals.objects.get(person=profile, name='snacks').carb,1)
    snacks_prot = round(Meals.objects.get(person=profile, name='snacks').prot,1)
    snacks_fat = round(Meals.objects.get(person=profile, name='snacks').fat,1)

    breakfast_products = MealsProducts.objects.filter(meal=Meals.objects.get(person=profile, name='breakfast'))
    breakfast_2_products = MealsProducts.objects.filter(meal=Meals.objects.get(person=profile, name='breakfast_2'))
    lunch_products = MealsProducts.objects.filter(meal=Meals.objects.get(person=profile, name='lunch'))
    dinner_products = MealsProducts.objects.filter(meal=Meals.objects.get(person=profile, name='dinner'))
    supper_products = MealsProducts.objects.filter(meal=Meals.objects.get(person=profile, name='supper'))
    snacks_products = MealsProducts.objects.filter(meal=Meals.objects.get(person=profile, name='snacks'))

    if request.method == "POST" and request.POST.get('delete_items'):
        items_to_delete = request.POST.getlist('delete_items')
        MealsProducts.objects.filter(pk__in=items_to_delete).delete()





    return render(request,
                  'account/meals.html',
                  {'products':products,
                   'today':today,
                   'breakfast_form': breakfast_form,
                   'breakfast2_form': breakfast2_form,
                   'lunch_form': lunch_form,
                   'dinner_form': dinner_form,
                   'supper_form': supper_form,
                   'snacks_form': snacks_form,
                   'breakfast_kcal':breakfast_kcal,
                   'breakfast_carb': breakfast_carb,
                   'breakfast_prot': breakfast_prot,
                   'breakfast_fat': breakfast_fat,
                   'breakfast_2_kcal': breakfast_2_kcal,
                   'breakfast_2_carb': breakfast_2_carb,
                   'breakfast_2_prot': breakfast_2_prot,
                   'breakfast_2_fat': breakfast_2_fat,
                   'dinner_kcal':dinner_kcal,
                   'dinner_carb':dinner_carb,
                   'dinner_prot':dinner_prot,
                   'dinner_fat':dinner_fat,
                   'lunch_kcal': lunch_kcal,
                   'lunch_carb': lunch_carb,
                   'lunch_prot': lunch_prot,
                   'lunch_fat': lunch_fat,
                   'supper_kcal': supper_kcal,
                   'supper_carb': supper_carb,
                   'supper_prot': supper_prot,
                   'supper_fat': supper_fat,
                   'snacks_kcal': snacks_kcal,
                   'snacks_carb': snacks_carb,
                   'snacks_prot': snacks_prot,
                   'snacks_fat': snacks_fat,
                   'breakfast_products':breakfast_products,
                   'breakfast_2_products': breakfast_2_products,
                   'lunch_products': lunch_products,
                   'dinner_products': dinner_products,
                   'supper_products': supper_products,
                   'snacks_products': snacks_products,
                   'message': message,
                   'limit_carb': request.user.profile.limit_carb,
                   'limit_prot': request.user.profile.limit_prot,
                   'limit_fat': request.user.profile.limit_fat,
                   'daily_calory_limit': request.user.profile.daily_calory_limit,
                   'kcal': profile.kcal,
                   'prot': profile.prot,
                   'carb': profile.carb,
                   'fat': profile.fat,
                   }

                  )
@login_required
def user_products(request):
    if request.method == 'POST':
        user_prod_form = ProductsForm(request.POST)
        if user_prod_form.is_valid():
            new_user_prod = user_prod_form.save(commit=False)
            new_user_prod.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_prod_form = ProductsForm()

    return render(request,
                  'account/user_products.html',
                  {'user_prod_form': user_prod_form},)

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        product = Products.objects.all()
        serializer = ProductsSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)



