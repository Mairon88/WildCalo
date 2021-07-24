from django.contrib import admin
from .models import Profile, Meals, Products, MealsProducts, UserProducts


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'weight', 'height', 'physical_activity', 'new_weight', 'time', 'kcal', 'carb', 'prot', 'fat')
    list_filter = ('gender', 'physical_activity', 'time')


@admin.register(Meals)
class MealsAdmin(admin.ModelAdmin):
    list_display = ('person', 'name', 'kcal', 'carb', 'prot', 'fat')

@admin.register(Products)
class MealsProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'kcal', 'carb', 'prot', 'fat')

@admin.register(MealsProducts)
class MealsProductsAdmin(admin.ModelAdmin):
    list_display = ('meal', 'name', 'weight', 'kcal', 'carb', 'prot', 'fat')

@admin.register(UserProducts)
class UserProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'kcal', 'carb', 'prot', 'fat')