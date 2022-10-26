from msilib.schema import Error
from warnings import catch_warnings
from model import Model
from view import View
import datetime
import ctypes


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.assign_setting_variables()

    def main(self):
        self.view.main()

    def update_tree_view(self):
        self.view.tree_view.delete(*self.view.tree_view.get_children())
        i=1
        for customer in self.model.customers:
            self.view.append_tree_view(i, customer.errands, str(customer.arrival_time))
            i +=1
    
    def update_stats_box(self):
        self.view.clear_stats_box()
        self.view.append_stats_box("STATS")
        self.view.append_stats_box(f"Served customers: {str(self.model.served_customers)}")
        self.view.append_stats_box(f"Current PR: {str(round(self.model.current_pr, 2))}")
        self.view.append_stats_box(f"Sucessful robberies: {str(self.model.sucessful_robberies)}")
        self.view.append_stats_box(f"Failed robberies: {str(self.model.failed_robberies)}")
        self.view.append_stats_box(f"Longest queue: {str(self.model.longest_queue)}")
        self.view.append_stats_box(f"Handled errands: {str(self.model.handled_errands)}")
        # Prevents division with zero
        if self.model.served_customers>0:
            self.view.append_stats_box(
            f"Avg. errands per customer: {str(round(self.model.handled_errands/self.model.served_customers, 1))}")

    def assign_setting_variables(self):
        """
        Sets the widgets in View to what Model is.
        """
        self.view.opening_scale.set(self.model.opening_hour)
        self.view.closing_scale.set(self.model.closing_hour)
        self.view.p_new_customer_entry.insert(0, str(self.model.p_new_customer))
        self.view.amount_of_errands_option.set(self.model.level_of_errands)
        self.view.minutes_per_errand_scale.set(self.model.minutes_per_errand)
        self.view.p_robber.insert(0, str(self.model.p_robber))
        self.view.p_robber_fails_entry.insert(0, str(self.model.p_robber_fails))
        self.view.pr_win_entry.insert(0, str(self.model.pr_win))
        self.view.pr_loss_entry.insert(0, str(self.model.pr_loss))

    def init_simulation(self):
        """
        Takes the values from View and assigns them to Model
        """
        self.view.start_simulation_button.grid_remove()
        self.view.show_controll_buttons()
        self.view.disable_settings()

        try:
            self.model.opening_hour=int(self.view.opening_scale.get())
            self.model.closing_hour=int(self.view.closing_scale.get())

            if self.model.opening_hour >= self.model.closing_hour:
                raise Exception
            self.model.p_new_customer=float(self.view.p_new_customer_entry.get())
            self.model.minutes_per_errand=int(self.view.minutes_per_errand_scale.get())
            self.model.level_of_errands=self.view.amount_of_errands_option.get()
            self.model.p_robber=float(self.view.p_robber.get())
            self.model.p_robber_fails=float(self.view.p_robber_fails_entry.get())
            self.model.pr_win = float(self.view.pr_win_entry.get())
            self.model.pr_loss = float(self.view.pr_loss_entry.get())
            self.model.current_time = datetime.time(hour=self.model.opening_hour, minute=0, second=0)
            self.view.append_output("Simulationen har börjat \n")
        
        except:
            ctypes.windll.user32.MessageBoxW(0, 
            "Fel input. Regler: Använd siffror. Decimaltecken är punkt (.). Öppettiden måste var innan stängningstiden", "FEL", 1)
            self.restart()


    def simulate_minute(self):
        """
        Simulates one minute and prints suitable output to general output box
        """
        self.model.simulate_minute()
        self.view.append_output(self.model.message)
        self.model.message = ""
        self.update_tree_view() 
        self.update_stats_box()
        self.view.time_label.config(text=f"{str(self.model.current_time.hour)}:{str(self.model.current_time.minute)}")
        if self.model.open == False:
            self.view.create_chart(self.model.times, self.model.queue_lengths)
            self.view.show_restart_button()

    def simulate_10_minutes(self):
        for i in range(10):
            if self.model.open:
                self.simulate_minute()
    
    def restart(self):
        self.view.destroy()
        self.model = Model()
        self.view = View(self)
        self.assign_setting_variables()

    def simulate_day(self):
        while self.model.open:
            self.simulate_minute()
    

if __name__ == "__main__":
    post_office = Controller()
    post_office.main()