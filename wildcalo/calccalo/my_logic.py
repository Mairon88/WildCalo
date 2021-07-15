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
            mens_bm = round(66 + (13.7 * self.weight) + (5 * self.height) - (6.8 * self.age),2)
            print(mens_bm)
            return mens_bm

        else:
            women_bm = round(655 + (9.6 * self.weight) + (1.8 * self.height) - (4.7 * self.age), 2)
            return women_bm

    def total_daily_energy_requirement(self):
        for activity in self.activity_choices.keys():
            if self.activity == activity:
                tder = self.activity_choices[activity] * self.basic_metabolism()
                print(tder)
                return tder

    # def calculate_deficit(self):
    #     daily_deficit =


