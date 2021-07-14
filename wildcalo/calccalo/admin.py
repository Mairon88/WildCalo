from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'weight', 'height', 'physical_activity', 'new_weight', 'time')
    list_filter = ('gender', 'physical_activity', 'time')
# Register your models here.
