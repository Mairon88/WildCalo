from django import forms
from django.contrib.auth.models import User
from .models import Profile, MealsProducts, Products
from django.forms.widgets import DateInput

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

    gender = forms.CharField(widget=forms.Select(choices=Profile.GENDER_CHOICES))
    age = forms.IntegerField()
    weight = forms.IntegerField()
    height = forms.IntegerField()
    new_weight = forms.IntegerField()
    physical_activity = forms.CharField(widget=forms.Select(choices=Profile.ACTIVITY_CHOICES))
    time = forms.IntegerField()

class BreakfastProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightb= forms.FloatField()
    productb= forms.ModelChoiceField(queryset=Products.objects.all())

class Breakfast2ProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightb2= forms.FloatField()
    productb2= forms.ModelChoiceField(queryset=Products.objects.all())

class LunchProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightl= forms.FloatField()
    productl= forms.ModelChoiceField(queryset=Products.objects.all())

class DinnerProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightd= forms.FloatField()
    productd= forms.ModelChoiceField(queryset=Products.objects.all())

class SupperProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightsu= forms.FloatField()
    productsu= forms.ModelChoiceField(queryset=Products.objects.all())

class SnacksProductsForm(forms.ModelForm):
    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weightsn= forms.FloatField()
    productsn= forms.ModelChoiceField(queryset=Products.objects.all())


