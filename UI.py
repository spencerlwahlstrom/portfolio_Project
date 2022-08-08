# Author: Spencer Lynn Wahlstrom
# Date: 8/8/2022
# Description:Portfolio project plant list application to manage watering and fertilizing and get reminders
from tkinter import *
from time import *
import datetime


class Plant:
    """Object for plant row, in my plant list"""
    def __init__(self, name, water, fertilize):
        """Initializes plant row object instance in table row"""
        self.name = name
        self.water = water
        self.fertilize = fertilize

class ClocK:
    "Object for clock instance for displaying date and time"
    def __init__(self, window, root):
        self.root=root
        self.window=window
        self.date = Label(window, font=("Helvetica", "12", "bold italic"))
        self.date.grid(row=0, column=0, padx=5, pady=5)
        self.clock = Label(window, font=("Helvetica", "12", "bold italic") )
        self.clock.grid(row=2, column=0, padx=5, pady=5)


    def time(self):
        instance = strftime('%H:%M:%S %p')
        self.clock.configure(text=instance)
        self.clock.after(1000, self.time)

    def get_date(self):
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
        self.plant_list_label.grid(row=2, column=2)
        self.exit_label = Label(root, text="Click Here To Exit My Plant List"
                                           " And Return To Main Menu", font=("Helvetica", "8", "bold italic"))
        self.exit_button = Button(self.root, text="Exit", command=self.go_back,font = ("Helvetica", "10", "bold italic"))
        self.exit_label.grid(row=0, column=0)
        self.exit_button.grid(row=1, column=0)
        self.make_headers(root)

    def make_headers(self, root):
        """Grids the headers for the my plant list table"""
        headers = ["Plant", "Next Water Date", "Next Fertilize Date", "Mark Watered", "Mark Fertilized"]
        for i in range(len(headers)):
            self.i = Label(root,text= headers[i], width= 15, font = ("Helvetica", "10", "bold"), relief='ridge')
            self.i.grid(row=5, column=i, sticky ="nsew")

    def add_row(self, name, water, fertilize):
        """Adds plant to list"""
        plant = Label(self.root, text = name )
        plant.grid(row=self.row_index, column=0, sticky='nsew')
        row = self.row_index-2
        delete= Button(self.root, text =  f'Delete {name}',
                       command= lambda: self.popup_delete(row, name), font = ("Helvetica", "10", "bold"))
        delete.grid(row=self.row_index, column=5, sticky='nsew')
        self.plants[row]=(plant, delete)
        self.row_index += 1

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
            row = self.plants[row_number]
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


class Add_Plant():
    """Class creates the add plant form for adding a plant to my plant list"""
    def __init__(self, root, plant_grid):
        """initializes Add_Plant class for the add plant form"""
        self.plant_grid = plant_grid
        self.set_up_plant_name(root)
        self.set_up_intervals(root)
        self.submit = Button(root,text="Submit", command = self.get_text, font=("Helvetica", "10", "bold"))
        self.submit.pack(padx = 10, pady =10)

    def set_up_plant_name(self, root):
        """Sets up the add plant part of the form and info for use by init method"""
        self.add_plant_label = Label(root, text="Add Plant", font=("Helvetica", "15", "bold italic"))
        self.add_plant_label.pack(side=LEFT)
        self.info = Label(root,text="Add a plant to My Plant List, \n to set watering and fertilizing \n intervals and to "
                               "automatically \nreceive reminders however often\n  you choose!",font=("Helvetica", "8", "bold italic"))
        self.info.pack(side=LEFT)
        self.enter_plant_name = Label(root, text="Enter Plant Name", anchor="w")
        self.plant_name = Entry(root, width=15)
        self.enter_plant_name.pack()
        self.plant_name.pack()

    def set_up_intervals(self, root):
        """Sets up interval portion of the add plant form"""
        self.enter_water = Label(root, text="Enter Watering Interval in Days", anchor="w")
        self.watering = Entry(root, width=15)
        self.enter_water.pack()
        self.watering.pack()
        self.enter_fertilize = Label(root, text="Enter Fertilizing Interval in Days", anchor="w")
        self.fertilizing = Entry(root, width=15)
        self.enter_fertilize.pack()
        self.fertilizing.pack()

    def get_text(self):
        """Adds text from add_plant form to plant list. """
        name = self.plant_name.get()
        water = self.watering.get()
        fertilize = self.fertilizing.get()
        self.plant_grid.add_row(name, water, fertilize)
        self.plant_name.delete(0, END)
        self.watering.delete(0, END)
        self.fertilizing.delete(0, END)


def make_list(window):
    """Function starts application, and opens my plant list"""
    root = set_up_root(window)
    set_up_frames(root)
    root.mainloop()
    return

def set_up_frames(root):
    """sets up frames for plant list"""
    grid_frame = Frame(root)
    add_frame = Frame(root, highlightbackground="#698B69", highlightthickness=2, width=300, height=300)
    clock_frame = Frame(add_frame, highlightbackground="#698B69", highlightthickness=2)
    plant_list = Table(grid_frame, root)
    add_plant_form = Add_Plant(add_frame, plant_list)
    clock = ClocK(clock_frame, root)
    add_frame.pack(side=TOP, fill=BOTH, padx=10, pady=10)
    clock_frame.pack(side=RIGHT)
    clock.time()
    clock.get_date()
    grid_frame.pack()


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
    master.geometry("600x600")
    start_label = Label(master, text="Click here to create a new "
                           "Plant List and start the Application", font = ("Helvetica", "14", "bold italic"))
    open_table = Button(master, text ="Click here", command=lambda: make_list(master), font = ("Helvetica", "10", "bold"))
    start_label.pack()
    open_table.pack(padx=10,pady=10)
    master.mainloop()

if __name__ == '__main__':
    main()