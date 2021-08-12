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

    weightb= forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Waga [g]'}))
    productb= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwa produktu'}))


class Breakfast2ProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightb2= forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Waga [g]'}))
    productb2= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwa produktu'}))

class LunchProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightl= forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Waga [g]'}))
    productl= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwa produktu'}))

class DinnerProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightd= forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Waga [g]'}))
    productd= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwa produktu'}))

class SupperProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightsu= forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Waga [g]'}))
    productsu= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwa produktu'}))

class SnacksProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightsn= forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Waga [g]'}))
    productsn= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwa produktu'}))


class NameField(forms.CharField):
    def to_python(self, value):
        return value.title()

class ProductsForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ('name','type', 'kcal', 'carb', 'prot', 'fat')

    name = NameField(label='Nazwa')
    type = forms.ChoiceField(choices = Products.TYPE_CHOICES, label='Typ')
    kcal = forms.FloatField(label='Kalorie')
    carb = forms.FloatField(label='Węglowodany')
    prot = forms.FloatField(label='Białko')
    fat = forms.FloatField(label='Tłuszcz')

    def clean_title(self):
        return self.cleaned_data['name'].title()
