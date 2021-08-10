from django import forms
from django.contrib.auth.models import User
from .models import Profile, MealsProducts, Products
from django.forms.widgets import DateInput
from django.shortcuts import get_object_or_404

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('gender', 'age', 'weight', 'height', 'physical_activity', 'new_weight', 'time')

    gender = forms.CharField(label='Płeć', widget=forms.Select(choices=Profile.GENDER_CHOICES))
    age = forms.IntegerField(label='Wiek')
    weight = forms.IntegerField(label='Waga')
    height = forms.IntegerField(label='Wzrost')
    new_weight = forms.IntegerField(label='Nowa waga')
    physical_activity = forms.CharField(label='Aktywność fizyczna',widget=forms.Select(choices=Profile.ACTIVITY_CHOICES))
    time = forms.IntegerField(label='Czas')


class BreakfastProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightb= forms.FloatField()
    productb= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name of product'}))


class Breakfast2ProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightb2= forms.FloatField()
    productb2= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name of product'}))

class LunchProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightl= forms.FloatField()
    productl= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name of product'}))

class DinnerProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightd= forms.FloatField()
    productd= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name of product'}))

class SupperProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightsu= forms.FloatField()
    productsu= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name of product'}))

class SnacksProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightsn= forms.FloatField()
    productsn= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name of product'}))


class NameField(forms.CharField):
    def to_python(self, value):
        return value.title()

class ProductsForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ('name','type', 'kcal', 'carb', 'prot', 'fat')

    name = NameField()
    type = forms.ChoiceField(choices = Products.TYPE_CHOICES)
    kcal = forms.FloatField()
    carb = forms.FloatField()
    prot = forms.FloatField()
    fat = forms.FloatField()

    def clean_title(self):
        return self.cleaned_data['name'].title()
