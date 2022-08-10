# Author: Spencer Lynn Wahlstrom
# Date: 8/8/2022
# Description:Portfolio project plant list application to manage watering and fertilizing and get reminders
from tkinter import *
from time import *
import datetime
import time


class Plant:
    """Object for plant row, in my plant list"""
    def __init__(self, name, water, fertilize, last_water, last_fertilze):
        """Initializes plant row object instance in table row"""
        self.name = name
        self.water = water
        self.fertilize = fertilize
        self.last_water = last_water
        self.last_fertilize = last_fertilze

class ClocK:
    "Object for clock instance for displaying date and time"
    def __init__(self, window, root):
        self.root=root
        self.window=window
        self.date = Label(window, font=("Helvetica", "11", "bold italic"))
        self.date.grid(row=0, column=0, padx=5, pady=5)
        self.clock = Label(window, font=("Helvetica", "11", "bold italic") )
        self.clock.grid(row=2, column=0, padx=5, pady=5)

    def time_display(self):
        """Gets time for display"""
        instance = strftime('%H:%M:%S %p')
        self.clock.configure(text=instance)
        self.clock.after(1000, self.time_display)

    def get_date(self):
        """Gets date for display"""
        date = datetime.datetime.now()
        self.date.configure(text=f"{date:%A, %B %d, %Y}")
        self.date.after(1000, self.get_date)


class Table:
    """Class creates instance of my plant list"""
    def __init__(self, root, window):
        """Initializes plant list table widget"""
        self.window = window
        self.root = root
        self.plants = {}
        self.row_index = 6
        self.plant_list_label = Label(root, text="My Plant List", width=10, font=("Helvetica", "16", "bold italic"))
        self.plant_list_label.grid(row=2, column=1)
        self.exit_label = Label(root, text="Click Here To Exit My Plant List"
                                           " And Return To Main Menu", font=("Helvetica", "10", "bold italic"))
        self.exit_button = Button(self.root, text="Exit", command=self.go_back,font = ("Helvetica", "10", "bold italic"))
        self.exit_label.grid(row=0, column=0)
        self.exit_button.grid(row=1, column=0)
        self.make_headers(root)

    def make_headers(self, root):
        """Grids the headers for the my plant list table"""
        headers = ["Plant", "Next Water Date", "Next Fertilize Date", "Delete"]
        for i in range(len(headers)):
            self.i = Label(root,text= headers[i], width= 15, font = ("Helvetica", "10", "bold"), relief='ridge')
            self.i.grid(row=5, column=i, sticky ="nsew")

    def add_row(self, name, water, fertilize):
        """Adds plant to list"""
        dates = self.get_next_dates(water,fertilize)
        plant = Label(self.root, text = name, font = ("Helvetica", "9", "bold"))
        next_water = Label(self.root, text = dates[0], font = ("Helvetica", "9", "bold"))
        next_fertilize = Label(self.root, text = dates[1],font = ("Helvetica", "9", "bold") )
        plant.grid(row=self.row_index, column=0, sticky='nsew')
        next_water.grid(row=self.row_index, column=1, sticky='nsew')
        next_fertilize.grid(row=self.row_index, column=2, sticky='nsew')
        delete= self.make_delete(self.row_index - 2, name)
        plant_object = Plant(name,water, fertilize, datetime.date.today(), datetime.date.today())
        self.plants[self.row_index - 2]=[plant_object,(plant, delete, next_water, next_fertilize)]
        self.row_index += 1

    def make_delete(self, row, name):
        """Makes Delete Button for Plant row"""
        row = self.row_index - 2
        delete = Button(self.root, text=f'Delete {name}',
                        command=lambda: self.popup_delete(row, name), font=("Helvetica", "10", "bold"))
        delete.grid(row=self.row_index, column=3, sticky='nsew')
        return delete


    def get_next_dates(self,water,fertilize):
        """Takes in water and fertilize interval for plant, and returns next water, next fertilize date"""
        water_int = 7 if not water else int(water)
        fertilize_int = 7 if not fertilize else int(fertilize)
        date = datetime.date.today()
        next_water= date + datetime.timedelta(days=water_int)
        next_fertilize = date + datetime.timedelta(days=fertilize_int)
        return next_water, next_fertilize

    def popup_delete(self, row, name):
        """Creates confirmation window for deleting a plant row, with confirm and cancel"""
        popup = Toplevel(self.root)
        popup.wm_attributes('-toolwindow', 'True')
        popup.title('Plant Manager')
        popup.geometry("600x200")
        l = Label(popup, text=f'Are you sure to want to delete this plant,'
                              f' {name}? Click confirm to delete, and cancel to go back', font=("Helvetica", "9", "bold italic"))
        l.pack()
        confirm = Button(popup,text="Confirm", command=lambda: self.delete_row(row, popup))
        cancel = Button(popup, text="Cancel", command=popup.destroy)
        confirm.pack()
        cancel.pack()

    def delete_row(self, row_number, window):
        """Deletes current row, providing functionality for delete button"""
        if self.plants:
            row = self.plants[row_number][1]
            for item in row:
                item.destroy()
            del self.plants[row_number]
        window.destroy()

    def go_back(self):
        """Sets up functionality for button to return to initial window, and destroys instance of plant list"""
        self.window.quit()
        self.window.destroy()
        master = Tk()
        master.wm_attributes('-toolwindow', 'True')
        master.title('Plant Manager')
        master.geometry("600x600")
        start_label = Label(master, text="Click here to create a new "
                          "Plant List and start the Application",font=("Helvetica", "14", "bold italic"))
        open_table = Button(master, text="Click here", command=lambda: make_list(master), font=("Helvetica", "10", "bold"))
        start_label.pack()
        open_table.pack(padx=10, pady=10)

class Reminder():
    """Class creates the reminder form, to start reminder cycle"""
    def __init__(self, root, plants, clock_frame):
        """Initializes reminder class form, for the reminder form"""
        self.clock_frame = clock_frame
        self.root = root
        self.plant_table= plants
        self.reminder_interval = 1
        self.reminder_water = []
        self.reminder_fertilize = []
        self.start_label= Label(root, text="Click here to set "
                                           "and start reminders", font=("Helvetica", "10", "bold italic"))
        self.popup_button = Button(root, text="Click Here", command=self.popup )
        self.start_label.grid(row=0,column=0)
        self.popup_button.grid(row=1, column=0)

    def popup(self):
        """Popup window for setting and starting reminders"""
        window = Toplevel(self.root)
        self.reminder_setup(window)
        self.hours_label = Label(window, text="hours")
        self.hours = Entry(window, width=15)
        self.start_button = Button(window, text="Start Reminders", command= lambda: self.start_reminders(window))
        self.cancel_button = Button(window, text="Cancel", command= window.destroy)
        self.hours.grid(row=3, column=1)
        self.hours_label.grid(row=3, column=2, padx=5)
        self.cancel_button.grid(row=5, column=0)
        self.start_button.grid(row=4, column=0, pady=10)


    def reminder_setup(self, window):
        """Sets up reminder window information and labels"""
        self.reminder_label = Label(window, text="Start Reminders", font=("Helvetica", "15", "bold italic"))
        self.reminder_info = Label(window, text="Enter how often in hours you would like to receive reminders. It will "
                                                "default to one.", font=("Helvetica", "10", "bold"))
        self.example = Label(window, text="Example:  enter '2' and receive"
                                          " reminders every 2 hours", font=("Helvetica", "10", "bold italic"))
        self.reminder_label.grid(row=0, column=0)
        self.reminder_info.grid(row=1, column=0)
        self.example.grid(row=2, column=0)

    def start_reminders(self, window):
        """Start reminder cycle sends request to microservice, and sets up scheduled requests"""
        self.reminder_interval = self.hours.get()
        window.destroy()
        self.view_reminders()
        self.send_request()
        time.sleep(2)
        self.receive_response()
        self.erase()

    def get_reminder_schedule(self):
        """"""

    def view_reminders(self):
        """Creates button for viewing reminders once it has been started"""
        view_frame =  Frame(self.clock_frame,highlightbackground="#698B69", highlightthickness=2, width=500, height=300)
        view_frame.grid(row=4, column=16)
        self.view_reminders_label = Label(view_frame, text="Click here to view "
                                                          "reminder for today", font=("Helvetica", "10", "bold italic"))
        self.view_reminders_button = Button(view_frame, text="Click here", command=self.reminder_popup)
        self.view_reminders_label.grid(row=0,column=6)
        self.view_reminders_button.grid(row=1, column=6)

    def reminder_popup(self):
        """Generates popup reminder window"""
        row =2
        window = Toplevel(self.root, height = 800, width =800)
        window.wm_attributes('-toolwindow', 'True')
        window.title('Reminder')
        window.geometry("300x300")
        title_label = Label(window, text="Reminder!", font=("Helvetica", "16", "bold italic"))
        title_label.grid(row=0, column=0)
        self.water_reminder(row,window)

    def water_reminder(self, row, window):
        """Generates plants to water for popup"""
        water_label = Label(window, text="Plants to water today", font=("Helvetica", "12", "bold italic"))
        water_label.grid(row=1, column=0)
        for plant in self.reminder_water:
            plant.strip()
            name = plant[1:len(plant) - 2]
            self.plant = Label(window, text=name, font=("Helvetica", "10", "bold"))
            self.plant.grid(row=row, column=0)
            row += 1
        row += 1
        self.fertilize_reminder(row,window)

    def fertilize_reminder(self, row, window):
        """Generates plants to fertilize for popup"""
        fertilize_label = Label(window, text="Plants to Fertilize today", font=("Helvetica", "12", "bold italic"))
        fertilize_label.grid(row=row, column=0)
        row += 1
        for plant in self.reminder_fertilize:
            plant.strip()
            name = plant[1:len(plant) - 2]
            self.plant = Label(window, text=name, font=("Helvetica", "10", "bold"))
            self.plant.grid(row=row, column=0)
            row += 1

    def send_request(self):
        """Sends request to microservice to update plants to water, and plants to fertilize"""
        plants = self.plant_table.plants
        with open('schedule.txt', 'w') as f:
            for entry in plants.values():
                plant= entry[0]
                f.write(f"'{plant.name}' {plant.water} {plant.fertilize} '{plant.last_water}' '{plant.last_fertilize}'\n")
        with open('run.txt', 'w') as f:
            f.write("run\n")

    def receive_response(self):
        """Gets response from microservice"""
        self.reminder_water, self.reminder_fertilize = [], []
        with open('water.txt', 'r') as f:
            current = f.readline()
            while current:
                self.reminder_water.append(current)
                current = f.readline()
        with open('fertilizer.txt', 'r') as f:
            current = f.readline()
            while current:
                self.reminder_fertilize.append(current)
                current = f.readline()

    def erase(self):
        """Erases pipeline"""
        open('fertilizer.txt','w').close()
        open('water.txt', 'w').close()
        open('run.txt', 'w').close()


class Add_Plant():
    """Class creates the add plant form for adding a plant to my plant list"""
    def __init__(self, root, plant_grid):
        """initializes Add_Plant class for the add plant form"""
        self.root= root
        self.plant_grid = plant_grid
        self.set_up_plant_name(root)
        self.set_up_intervals(root)
        self.submit = Button(root,text="Submit", command = self.get_text, font=("Helvetica", "10", "bold"))
        self.submit.grid(row=5, column=6, pady=5)

    def set_up_plant_name(self, root):
        """Sets up the add plant part of the form and info for use by init method"""
        self.add_plant_label = Label(root, text="Add Plant", font=("Helvetica", "15", "bold italic"))
        self.add_plant_label.grid(row=0, column=0)
        self.info = Label(root,text="Add a plant to My Plant List, \n to set watering and fertilizing \n intervals and to "
                               "automatically \nreceive reminders however often\n  you choose! "
                               "Intervals will default\n to one week if left blank.",font=("Helvetica", "8", "bold italic"))
        self.info.grid(row=1, column = 0)
        self.enter_plant_name = Label(root, text="Enter Plant Name", anchor="w")
        self.plant_name = Entry(root, width=15)
        self.enter_plant_name.grid(row=2, column=6,pady=5)
        self.plant_name.grid(row=2, column=7, pady=5)

    def set_up_intervals(self, root):
        """Sets up interval portion of the add plant form"""
        self.enter_water = Label(root, text="Enter Watering Interval in Days", anchor="w")
        self.watering = Entry(root, width=15)
        self.enter_water.grid(row=3, column=6, pady=5)
        self.watering.grid(row=3, column=7, pady=5)
        self.enter_fertilize = Label(root, text="Enter Fertilizing Interval in Days", anchor="w")
        self.fertilizing = Entry(root, width=15)
        self.enter_fertilize.grid(row=4, column=6, pady=5)
        self.fertilizing.grid(row=4, column=7, pady=5)

    def get_text(self):
        """Adds text from add_plant form to plant list. """
        name = self.plant_name.get()
        water = self.watering.get() if self.watering.get() else 7
        fertilize = self.fertilizing.get() if self.fertilizing.get() else 7
        self.plant_grid.add_row(name, water, fertilize)
        self.plant_name.delete(0, END)
        self.watering.delete(0, END)
        self.fertilizing.delete(0, END)
        self.root.destroy()


def make_list(window):
    """Function starts application, and opens my plant list"""
    root = set_up_root(window)
    set_up_frames(root)
    root.mainloop()
    return

def set_up_frames(root):
    """sets up frames for plant list"""
    grid_frame = Frame(root)
    plant_list = Table(grid_frame, root)
    set_up_top_frames(root,plant_list)
    grid_frame.pack()

def set_up_top_frames(root, plant_list):
    """Sets up top portion"""
    clock_frame = Frame(root, highlightbackground="#698B69", highlightthickness=2, width=500)
    add_frame = Frame(clock_frame, highlightbackground="#698B69", highlightthickness=2, width=500, height=300)
    add_button(add_frame, plant_list)
    reminder_frame = Frame(clock_frame,highlightbackground="#698B69", highlightthickness=2, width=500, height=300)
    reminder_form = Reminder(reminder_frame, plant_list, clock_frame)
    clock = ClocK(clock_frame, root)
    clock_frame.pack(side=TOP, fill=X, padx=10)
    add_frame.grid(row=4, column=8)
    reminder_frame.grid(row=4, column=12)
    clock.time_display()
    clock.get_date()

def add_button(root, plant_list):
    """makes add_button for add plant form"""
    add_label = Label(root, text = "Click here to add a plant", font=("Helvetica", "10", "bold italic"))
    add = Button(root, text = "Add plant", command=lambda : add_plant_popup(add_label, plant_list))
    add_label.grid(row=0, column=0)
    add.grid(row=1, column=0)

def add_plant_popup(root, plant_list):
    """popup to add plant"""
    window = Toplevel(root)
    window.wm_attributes('-toolwindow', 'True')
    window.title('Add a plant')
    window.geometry("500x400")
    add_frame= Frame(window)
    add_plant_form = Add_Plant(window, plant_list)
    add_frame.grid(row=0, column=0)

def set_up_root(window):
    """Sets up tk root for my plant list"""
    window.destroy()
    root = Tk()
    root.wm_attributes('-toolwindow', 'True')
    root.title('Plant Manager')
    root.geometry("900x800")
    return root

def main():
    """Main function opens initial window of GUI, and starts application"""
    master = Tk()
    master.wm_attributes('-toolwindow', 'True')
    master.title('Plant Manager')
    master.geometry("600x400")
    start_label = Label(master, text="Click here to create a new "
                           "Plant List and start the Application", font = ("Helvetica", "14", "bold italic"))
    open_table = Button(master, text ="Click here", command=lambda: make_list(master), font = ("Helvetica", "10", "bold"))
    start_label.pack()
    open_table.pack(padx=10,pady=10)
    master.mainloop()

if __name__ == '__main__':
    main()