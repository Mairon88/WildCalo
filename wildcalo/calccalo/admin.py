from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth', 'weight', 'height', 'physical_activity', 'new_weight', 'days_to_lose_weight')
    list_filter = ('gender', 'physical_activity', 'days_to_lose_weight')
# Register your models here.
