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

class MealsProductsForm(forms.ModelForm):

    class Meta:
        model = MealsProducts
        fields = ('weight',)

    weight_b = forms.FloatField()
    product_b = forms.ModelChoiceField(queryset=Products.objects.all())

    weight_b2 = forms.FloatField()
    product_b2 = forms.ModelChoiceField(queryset=Products.objects.all())

    weight_d = forms.FloatField()
    product_d = forms.ModelChoiceField(queryset=Products.objects.all())

    weight_l = forms.FloatField()
    product_l = forms.ModelChoiceField(queryset=Products.objects.all())

    weight_su = forms.FloatField()
    product_su = forms.ModelChoiceField(queryset=Products.objects.all())

    weight_sn = forms.FloatField()
    product_sn = forms.ModelChoiceField(queryset=Products.objects.all())
