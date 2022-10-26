import math
import random
import datetime

class Customer:

    def __init__(self, arrival_time, log_base):

        self.errands = math.ceil(math.log(1.0/random.random(), log_base)) # enligt regel
        self.checkout_time = None
        self.arrival_time = arrival_time

    # Returnerar exit time.
    # Addition med datetime.datetime kräver att man först ändrar till en datetime
    def get_checkout_time(self, current_time, minutes_per_errand):
        return (datetime.datetime.combine(datetime.date.today(), current_time) +
        datetime.timedelta(minutes=minutes_per_errand*self.errands)).time()

    def get_waiting_time(self):
        _arrival_time = datetime.datetime.combine(datetime.date.today(), self.arrival_time)
        _checkout_time = datetime.datetime.combine(datetime.date.today(), self.checkout_time)

        delta_time = _checkout_time - _arrival_time
        return delta_time.total_seconds() / 60

    # Obsolete 
    def get_errands(self):
        errands = 1
        while random.randint(1,2) == 1:
            errands +=1

        return errands


    def __str__(self):
        return f"Har {self.errands} ärenden. Ankom {self.arrival_time}."
