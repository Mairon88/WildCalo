from .models import Profile

class HarrisBededictEquation:

    def __init__(self, gender, age, weight, height, activity, new_weight, time):

        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.activity = activity
        self.new_weight = new_weight
        self.time = time
        self.activity_choices = {'sit':1.2,
                                 'low':1.375,
                                 'mod':1.55,
                                 'high':1.725,
                                 'vhigh':1.9}




    def basic_metabolism(self):
        if self.gender == 'male':
            try:
                mens_bm = 66 + (13.7 * self.weight) + (5 * self.height) - (6.8 * self.age)
                return int(mens_bm)
            except:
                mens_bm = None
                return mens_bm

        else:
            try:
                women_bm = 655 + (9.6 * self.weight) + (1.8 * self.height) - (4.7 * self.age)
                return int(women_bm)
            except:
                women_bm = None
                return women_bm


    def total_daily_energy_requirement(self):
        for activity in self.activity_choices.keys():
            if self.activity == activity:
                try:
                    tder = self.activity_choices[activity] * self.basic_metabolism()
                except:
                    tder = None
                    return tder

        return int(tder)

    def calculate_deficit(self):
        daily_deficit = None

        try:
            weight_to_lose = abs(self.weight - self.new_weight)
            daily_deficit = (abs(self.weight - self.new_weight)) * 7000 / self.time
            if self.new_weight < self.weight:
                daily_calorie_limit = self.total_daily_energy_requirement() - daily_deficit
            else:
                daily_calorie_limit = self.total_daily_energy_requirement() + daily_deficit
        except:
            daily_deficit=  None
            daily_calorie_limit = None
            weight_to_lose = None
            return daily_deficit, daily_calorie_limit,  weight_to_lose

        return int(daily_deficit), int(daily_calorie_limit), int(weight_to_lose)

    def is_deficit_to_big(self):
        try:
            percent_deficit = int((self.calculate_deficit()[0]/self.total_daily_energy_requirement())*100)
        except:
            percent_deficit = None
            return percent_deficit
        return percent_deficit


class NutritionalValues:
    carb = 4 # 1 gram carb = 4 kcal
    prot = 4
    fat = 9

    proportions = {'carb': 0.5, 'prot':0.3, 'fat': 0.2}

    def __init__(self, daily_calories_limit):
        self.daily_calories_limit = daily_calories_limit

    def carb_value(self):
        try:
            carb_cal = self.daily_calories_limit * NutritionalValues.proportions['carb']
            carb_g = carb_cal / NutritionalValues.carb
        except:
            return 0
        return int(carb_g)

    def prot_value(self):
        try:
            prot_cal = self.daily_calories_limit * NutritionalValues.proportions['prot']
            prot_g = prot_cal / NutritionalValues.prot
        except:
            return 0
        return int(prot_g)

    def fat_value(self):
        try:
            fat_cal = self.daily_calories_limit * NutritionalValues.proportions['fat']
            fat_g = fat_cal / NutritionalValues.fat
        except:
            return 0
        return int(fat_g)





