import datetime
import random
import configparser
from select import select
from customer import Customer

class Model():
    def __init__(self):

        config = configparser.ConfigParser()
        config.read("config.ini") # IMPLEMENT EXCEPTION

        self.message = ""
        self.opening_hour = int(config.get("StandardValues", "OpeningHour"))
        self.closing_hour = int(config.get("StandardValues", "ClosingHour"))
        self.p_new_customer = float(config.get("StandardValues", "PNewCustomer"))
        self.minutes_per_errand = int(config.get("StandardValues", "MinutesPerErrand"))
        self.level_of_errands = str(config.get("StandardValues", "LevelOfErrands"))
        self.p_robber = float(config.get("StandardValues", "PRobber"))
        self.p_robber_fails = float(config.get("StandardValues", "PRobberFails"))
        self.pr_win = float(config.get("StandardValues", "PRWin"))
        self.pr_loss = float(config.get("StandardValues", "PRLoss"))

        self.customers = []
        self.current_pr = 0.0
        self.customer_counter = 0 # Counts customers, even those who hasn't been served 
        self.served_customers = 0
        self.total_waiting_time = 0
        self.open = True

        # Used for stats
        self.sucessful_robberies = 0
        self.failed_robberies = 0
        self.longest_queue = 0
        self.handled_errands = 0
        self.queue_lengths = [0]
        self.times = [0]

        # Is used for generating amount of errands of a customer
        #self.base_setting = 1

    def refine_line(self, message):
        """
        Sets a timestamp and adds a newline
        """

        return f'[{self.current_time.hour}:{self.current_time.minute}] {message} \n'

    def get_log_base(self):
        """
        Returns a good logarithm base for amount of errands of a customer.
        """

        # Dropdown menu settings
        print(self.level_of_errands)
        if self.level_of_errands == "Low":
            return 3
        if self.level_of_errands == "High": 
            return 5/3
        else:
            return 2 # Base 2 gives the normal distribution

    def add_customer(self):
        self.customers.append(Customer(self.current_time, self.get_log_base()))
        self.customer_counter += 1
        self.message += self.refine_line(f" kommer kund nummer {self.customer_counter} "+
            f"st??ller sig i k??n p?? plats {len(self.customers)}")
    
    def add_minute(self):
        # Adds one minute to current time. datetime.datetime doesn't support timedelta
        # Therefore it has to be converted to a regular datetime and then reverted.
        self.current_time = (datetime.datetime.combine(datetime.date(1,1,1), self.current_time) +
        datetime.timedelta(minutes=1)).time()

    def release_customer(self):
        """
        Pops the first cutomer and takes stats
        """
        self.served_customers += 1
        self.message += self.refine_line(f" Kund nummer {self.served_customers} har betj??nats")
        self.total_waiting_time += self.customers[0].get_waiting_time()
        self.handled_errands += self.customers[0].errands
        self.customers.pop(0)

    def rob_office(self):
        self.message += self.refine_line("En r??nare kommer in i butiken med illavarslande planer")
        self.customers.clear()
        
        if random.random() <= self.p_robber_fails:
            self.message += self.refine_line("Fru Franco lyckas ??vermanna r??naren och kunderna evakuerar butiken oskadda")
            self.message += self.refine_line("Postkontoret f??r en PR-boost och fler kunder vill bes??ka butiken")
            self.current_pr += self.pr_win
            self.failed_robberies += 1

        else:
            self.message += self.refine_line("R??naren lyckas r??na butiken med hot och v??ld.")
            self.message += self.refine_line("Postkontoret f??r ett d??ligt rykte och f??rre kunder vill bes??ka butiken")
            self.current_pr -= self.pr_loss
            self.sucessful_robberies += 1

    def simulate_minute(self):
        """
        Here is the key simulation logic.  
        """
        if self.open == False:
            return

        self.add_minute()        

        # potentiellt TODO: G??ra detta till en booleansk funktion som evaluearar skiten. Nedanst??ende rad ??r r??tt onice 
        if random.random() < self.p_new_customer + self.current_pr and self.current_time.hour < self.closing_hour:
            self.add_customer()
            if random.random() < self.p_robber:
                self.rob_office()
                return
        
        # Recording data for the matplotlib diagram
        self.queue_lengths.append(len(self.customers))
        self.times.append(self.times[len(self.times)-1] + 1) #Out: 0,1,2,3...

        # Record longest queue
        if len(self.customers) > self.longest_queue:
            self.longest_queue = len(self.customers)

        # Prevents IndexOutOfRange
        if len(self.customers) > 0:

            #Calculate checkout time
            if self.customers[0].checkout_time == None:
                self.customers[0].checkout_time = self.customers[0].get_checkout_time(
                    self.current_time, self.minutes_per_errand)

            if self.customers[0].checkout_time == self.current_time:
                self.release_customer()

        if self.current_time.hour == self.closing_hour and self.current_time.minute == 0:
            self.message += self.refine_line(f" D??rren st??nger och nya kunder kan inte komma")
            
        if len(self.customers) == 0 and self.current_time.hour >= self.closing_hour:
            self.open = False
            self.message += (f"STATISTIK: {self.served_customers} kunder betj??nades och v??ntetiden var {self.total_waiting_time} min"+
            f" med en genomsnittlig betj??ningstid p?? {round(self.handled_errands*self.minutes_per_errand/self.served_customers, 1)} min")

        # Exponentialfunktion som g??r att pr-bonusen konvergerar mot 0
        self.current_pr *= 0.99 