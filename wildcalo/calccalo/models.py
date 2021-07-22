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
    daily_calory_limit = models.IntegerField(null=True, blank=True, default=0)

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
        return self.user.username


class Meals(models.Model):
    MEAL_CHOICES = [
        ('breakfast','Breakfast'),
        ('breakfast_2','II Breakfast'),
        ('dinner', 'Dinner'),
        ('lunch', 'Lunch'),
        ('supper', 'Supper'),
        ('snacks', 'Snacks')
    ]

    kcal = models.IntegerField(null=True, blank=True)
    prot = models.IntegerField(null=True, blank=True)
    carb = models.IntegerField(null=True, blank=True)
    fat = models.IntegerField(null=True, blank=True)
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=MEAL_CHOICES, default='breakfast')

    class Meta:
        verbose_name_plural = 'Meals'

    def __str__(self):
        return f'{self.person} - {self.name}'

class MealsProducts(models.Model):
    weight = models.FloatField(null=True, blank=True)
    name = name = models.CharField(max_length=50, null=True, blank=True )
    kcal = models.FloatField(null=True, blank=True)
    prot = models.FloatField(null=True, blank=True)
    carb = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Meal Products'


class Products(models.Model):
    TYPE_CHOICES = [
        ('vegetables','Vegetables'),
        ('fruits','Fruits'),
        ('meat', 'Meat'),
        ('fish', 'Fish'),
        ('sea foods', 'Sea foods'),
        ('dairy foods', 'Dairy foods'),
        ('eggs', 'Eggs'),
        ('nuts', 'Nuts'),
        ('seeds','Seeds'),
        ('sweets', 'Sweets'),
        ('salty snacks','Salty snacks'),
        ('drinks', 'Drinks'),
        ('breads', 'Breads'),
        ('spices', 'Spices')
    ]
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    kcal = models.FloatField()
    carb = models.FloatField()
    prot = models.FloatField()
    fat = models.FloatField()
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} - {self.kcal} - {self.carb} - {self.prot} - {self.fat}"

class UserProducts(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    kcal = models.FloatField()
    carb = models.FloatField()
    prot = models.FloatField()
    fat = models.FloatField()

    class Meta:
        verbose_name_plural = 'User Products'

