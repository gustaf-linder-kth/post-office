from textwrap import fill
import tkinter as tk
from tkinter import StringVar, Variable, ttk 
import tkinter.scrolledtext as st
from turtle import width # Onödvändig
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class View(tk.Tk):

    def __init__(self, controller):
        
        super().__init__()
        self.controller = controller

        self.title("Señora Francos Post Office")        
        
        self._create_output_box()
        self._create_tree_view()
        self._create_settings()
        self._create_stats_box()

    def append_output(self, message):
        """ Appends a line to general output box """
        self.general_output_box.configure(state="normal")
        self.general_output_box.insert(tk.INSERT, message)
        self.general_output_box.see(tk.END)
        self.general_output_box.configure(state="disabled")

    def append_tree_view(self, index, errands, arrival):
        self.tree_view.insert('', tk.END, values=[index, errands, arrival])

    def append_stats_box(self, message):
        self.stats_box.insert(tk.INSERT, message + "\n")

    def clear_stats_box(self):
        self.stats_box.delete(1.0, tk.END)


    def _create_output_box(self):
        self.general_output_box = st.ScrolledText(self,
        width=70, height=15, font=("Consolas", 11), bg="black", fg="#64d86b", state="normal")
        self.general_output_box.grid(column=0, row=0, columnspan=2, sticky=tk.W, pady=10, padx=10)
        

    def _create_tree_view(self):
        columns = ('index', 'errands', 'arrival')
        self.tree_view = ttk.Treeview(self, columns=columns, show="headings")

        self.tree_view.heading('index', text='Place in queue')
        self.tree_view.column(0, width=85)
        self.tree_view.column(1, width=120)
        self.tree_view.column(2, width=120)
        self.tree_view.heading('errands', text='Amount of errands')
        self.tree_view.heading('arrival', text='Time of arrival')
        self.tree_view.grid(row=1, column = 0, sticky=tk.W, pady=10, padx=10)

    def _create_stats_box(self):
        self.stats_box = st.ScrolledText(self,
        font = ("Lucida", 8), width=40, height=10, bg="black", fg="#64d86b")
        self.stats_box.grid(column=1, row=1)

    def create_chart(self, times, queue_lengths):
        """Creates line chart in new window"""
        plt.plot(times, queue_lengths)
        plt.title("Queue lengths Vs time")
        plt.xlabel("Minutes")
        plt.ylabel("People in queue")
        plt.show()

    def _create_settings(self):
        """
        Draws the setting widgets on the window
        """

        label_frame = ttk.LabelFrame(text="Settings")
        label_frame.grid(column=2, row = 0, rowspan=2, columnspan=2, sticky=tk.N, padx=10, pady=10)

        ttk.Label(label_frame, text = "Opening hour").grid(column=2, row=0, sticky=tk.N)
        self.opening_scale = tk.Scale(label_frame, from_=0, to = 23, orient=tk.HORIZONTAL)
        self.opening_scale.grid(column = 2, row=1)

        ttk.Label(label_frame, text = "Closing hour").grid(column=3, row=0, sticky=tk.N)
        self.closing_scale = tk.Scale(label_frame, from_=0, to = 23, orient=tk.HORIZONTAL)
        self.closing_scale.grid(column = 3, row=1)

        ttk.Label(label_frame, text = "Probability new customer").grid(column=2, row=2, sticky=tk.N, pady=10)
        self.p_new_customer_entry = ttk.Entry(label_frame)
        self.p_new_customer_entry.grid(column=3, row=2, sticky=tk.N, pady=10, padx=5)

        ttk.Label(label_frame, text = "Amount of errands").grid(column=2, row=3, sticky=tk.N, pady=10)
        self.option_list=("Low", "Medium", "High")
        self.amount_of_errands_option = StringVar()
        self.amount_of_errands_dropdown = tk.OptionMenu(label_frame, self.amount_of_errands_option,  "Low", "Medium", "High")
        self.amount_of_errands_dropdown.grid(column=3, row =3, pady=10)

        ttk.Label(label_frame, text = "Minutes per errand").grid(column=2, row=4, sticky=tk.N)
        self.minutes_per_errand_scale = tk.Scale(label_frame, from_=1, to = 4, orient=tk.HORIZONTAL)
        self.minutes_per_errand_scale.grid(column = 2, row=5)

        robber_frame = ttk.LabelFrame(label_frame, text="Robber settings")
        robber_frame.grid(column = 2, row = 6, columnspan=2, pady=10, padx=10)

        ttk.Label(robber_frame, text="Probability robber per customer").grid(column=2, row = 7)
        self.p_robber = ttk.Entry(robber_frame)
        self.p_robber.grid(column=3, row=7, padx=10, pady=5)

        ttk.Label(robber_frame, text="Probability robber fails").grid(column=2, row = 8)
        self.p_robber_fails_entry= ttk.Entry(robber_frame)
        self.p_robber_fails_entry.grid(column=3, row=8, padx=10, pady=5)

        ttk.Label(robber_frame, text="Potential PR-win").grid(column=2, row = 9)
        self.pr_win_entry = ttk.Entry(robber_frame)
        self.pr_win_entry.grid(column=3, row=9, padx=10, pady=5)

        ttk.Label(robber_frame, text="Potential PR-Loss").grid(column=2, row = 10)
        self.pr_loss_entry = ttk.Entry(robber_frame)
        self.pr_loss_entry.grid(column=3, row=10, padx=10, pady=5)

        self.start_simulation_button = tk.Button(self, text="Start Simulation", width=20, height=2, command=self.controller.init_simulation)
        self.start_simulation_button.grid(column = 2, row = 1, sticky=tk.SW, padx=10, pady=10)

        self.time_label = ttk.Label(self, text = "00:00", font = ("Consolas", 24))
        self.time_label.grid(column=3, row=1, sticky=tk.SE, padx=25, pady=25)

    def show_controll_buttons(self):
        """
        Shows forward, fast forward buttons on window
        """
        self.simulate_minute_button = tk.Button(self,text=">", font=("Consolas", 18), command=self.controller.simulate_minute)
        self.simulate_minute_button.grid(column=2, row =1, sticky=tk.SW, padx=10, pady=10)

        self.simulate_10_minute_button = tk.Button(self,text=">>", font=("Consolas", 18), command=self.controller.simulate_10_minutes)
        self.simulate_10_minute_button.grid(column=2, row =1, sticky=tk.S, padx=10, pady=10)

        self.simulate_day_button = tk.Button(self,text=">|", font=("Consolas", 18), command=self.controller.simulate_day)
        self.simulate_day_button.grid(column=2, row =1, sticky=tk.SE, padx=10, pady=10)

    def show_restart_button(self):
        """
        Shows restart button that restarts the program
        """
        self.simulate_minute_button.destroy()
        self.simulate_10_minute_button.destroy()
        self.simulate_day_button.destroy()
        self.restart_button = tk.Button(self, text="New simulation", width=20, height=2, command=self.controller.restart)
        self.restart_button.grid(column = 2, row = 1, sticky=tk.SW, padx=10, pady=10)

    def disable_settings(self):
        """
        Makes setting widgets readonly
        """
        self.opening_scale.configure(state="disabled")
        self.closing_scale.configure(state="disabled")
        self.p_new_customer_entry.configure(state="disabled")
        self.amount_of_errands_dropdown.configure(state="disabled")
        self.minutes_per_errand_scale.configure(state="disabled")
        self.p_robber.configure(state="disabled")
        self.p_robber_fails_entry.configure(state="disabled")
        self.pr_win_entry.configure(state="disabled")
        self.pr_loss_entry.configure(state="disabled")

    def main(self):
        self.mainloop()



