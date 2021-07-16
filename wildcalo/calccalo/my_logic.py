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
            mens_bm = 66 + (13.7 * self.weight) + (5 * self.height) - (6.8 * self.age)
            return int(mens_bm)

        else:
            women_bm = 655 + (9.6 * self.weight) + (1.8 * self.height) - (4.7 * self.age)
            return int(women_bm)

    def total_daily_energy_requirement(self):
        for activity in self.activity_choices.keys():
            if self.activity == activity:
                tder = self.activity_choices[activity] * self.basic_metabolism()

        return int(tder)

    def calculate_deficit(self):
        weight_to_lose = abs(self.weight - self.new_weight)
        daily_deficit = (abs(self.weight - self.new_weight)) * 7000 / self.time
        if self.new_weight < self.weight:
            daily_calorie_limit = self.total_daily_energy_requirement() - daily_deficit
        else:
            daily_calorie_limit = self.total_daily_energy_requirement() + daily_deficit

        return int(daily_deficit), int(daily_calorie_limit), int(weight_to_lose)

    def is_deficit_to_big(self):
        percent_deficit = int((self.calculate_deficit()[0]/self.total_daily_energy_requirement())*100)
        return percent_deficit


