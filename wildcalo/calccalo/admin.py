from django.contrib import admin
from .models import Profile, Meals, Products


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'weight', 'height', 'physical_activity', 'new_weight', 'time')
    list_filter = ('gender', 'physical_activity', 'time')


@admin.register(Meals)
class MealsAdmin(admin.ModelAdmin):
    list_display = ('person', 'name', 'products', 'kcal', 'prot', 'carb', 'fat')

@admin.register(Products)
class MealsProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'kcal', 'carb', 'prot', 'fat')