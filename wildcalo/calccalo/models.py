from django.db import models
from django.conf import settings

class Profile(models.Model):
    GENDER_CHOICES = {
        ('male','Male'),
        ('female','Female')
    }

    ACTIVITY_CHOICES = {
        ('sit','sedentary lifestyle'),
        ('low','low activity'),
        ('mod', 'moderate activity'),
        ('mod', 'moderate activity'),
        ('high','high activity'),
        ('vhigh', 'very high activity')
    }

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, default='male')
    date_of_birth = models.DateField()
    weight = models.IntegerField()
    height = models.IntegerField()
    physical_activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES, default='sit')
    new_weight = models.IntegerField(default=weight)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    days_to_lose_weight = models.IntegerField(null=True, blank=True)
    ppm = models.FloatField(null=True, blank=True)
    tdee = models.FloatField(null=True, blank=True)
    deficit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return 'Profil użytkownika {}.'.format(self.user.username)