from django.db import models
from django.conf import settings

class Profile(models.Model):
    GENDER_CHOICES = {
        ('male','Male'),
        ('female','Female')
    }

    ACTIVITY_CHOICES = [
        ('sit','Sedentary lifestyle'),
        ('low','Low activity'),
        ('mod', 'Moderate activity'),
        ('high','High activity'),
        ('vhigh', 'Very high activity')
    ]

    STATUS_CHOICES = {
        ('waiting','Waiting'),
        ('ongoing','Ongoing')
    }

    BODY_TYPE_CHOICES = {
        ('mezo','Mesomorph'),
        ('ekto','Ectomorph'),
        ('endo', 'Endomorphs'),
    }

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, default='male')
    age = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    physical_activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES, default='sit')
    new_weight = models.IntegerField(null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    time = models.IntegerField(null=True, blank=True)
    ppm = models.FloatField(null=True, blank=True)
    tdee = models.FloatField(null=True, blank=True)
    deficit = models.IntegerField(null=True, blank=True)
    daily_calory_limit = models.IntegerField(null=True, blank=True)

    kcal = models.IntegerField(null=True, blank=True)
    prot = models.IntegerField(null=True, blank=True)
    carb = models.IntegerField(null=True, blank=True)
    fat = models.IntegerField(null=True, blank=True)
    limit_kcal = models.IntegerField(null=True, blank=True)
    limit_prot = models.IntegerField(null=True, blank=True)
    limit_carb = models.IntegerField(null=True, blank=True)
    limit_fat = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
        return 'Profil użytkownika {}.'.format(self.user.username)