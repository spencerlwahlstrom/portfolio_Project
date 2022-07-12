# Author: Spencer Lynn Wahlstrom
# Date: 7/7/2022
# Description:
from tkinter import *

class Plant():
    def __init__(self, name, water, fert):
        self.name = name
        self.water = water
        self.fert = fert

class Table():
    def __init__(self, root, window):
        self.window= window
        self.root =root
        self.plants = {}
        self.row_index = 6
        self.e = Label(root, text = "My Plant List", width=10, font = ("Helvetica", "16", "bold italic"))
        self.e.grid(row=2, column=2)
        self.button= Button(self.root, text= "Click To Exit And Return To Main Menu", command=self.go_back,font = ("Helvetica", "8", "bold italic") )
        self.button.grid(row=0, column=0)
        headers = ["Plant", "Next Water Date", "Next Fertilize Date", "Mark Watered", "Mark Fertilized"]
        for i in range(len(headers)):
            self.e = Label(root,text= headers[i], width= 15, font = ("Helvetica", "10", "bold"), relief='ridge')
            self.e.grid(row=5, column=i, sticky ="sew")

    def add_row(self, name, water, fert):
        plant = Label(self.root, text = name )
        plant.grid(row=self.row_index, column=0, sticky='nsew')
        row = self.row_index-2
        delete= Button(self.root, text =  f'Delete {name}', command= lambda: self.delete_row(row), font = ("Helvetica", "10", "bold"))
        delete.grid(row=self.row_index, column=5, sticky='nsew')
        self.plants[row]=(plant, delete)
        self.row_index += 1

    def delete_row(self, row_number):
        """"""
        if self.plants:
            row = self.plants[row_number]
            for item in row:
                item.destroy()
            del self.plants[row_number]

    def go_back(self):
        self.window.destroy()
        master = Tk()
        master.geometry("600x600")
        f = Frame(master)
        l = Label(f, text="Click here to create a new Plant List and start the Application",
                  font=("Helvetica", "14", "bold italic"))
        open_table = Button(f, text="Click here", command=lambda: make_list(master), font=("Helvetica", "10", "bold"))
        f.pack(expand=True)
        l.pack()
        open_table.pack(padx=10, pady=10)




class Add_Plant():
    def __init__(self, root, plant_grid):
        self.plant_grid = plant_grid
        self.e = Label(root, text="Add Plant", font = ("Helvetica", "15", "bold italic"))
        self.e.pack(side=LEFT)
        self.e = Label(root, text="Enter Plant Name", anchor="w")
        self.plant_name = Entry(root, width =15)
        self.e.pack()
        self.plant_name.pack()
        self.e = Label(root, text="Enter Watering Interval in Days", anchor="w")
        self.watering = Entry(root, width =15)
        self.e.pack()
        self.watering.pack()
        self.e = Label(root, text="Enter Fertilizing Interval in Days", anchor="w")
        self.fertilizing = Entry(root, width=15)
        self.e.pack()
        self.fertilizing.pack()
        self.submit = Button(root,text="Submit", command = self.get_text, font=("Helvetica", "10", "bold"))
        self.submit.pack(padx = 10, pady =10)

    def get_text(self):
        name = self.plant_name.get()
        water = self.watering.get()
        fert = self.fertilizing.get()
        self.plant_grid.add_row(name, water, fert)
        self.plant_name.delete(0, END)
        self.watering.delete(0, END)
        self.fertilizing.delete(0, END)


def make_list(window):
    """"""
    window.destroy()
    root = Tk()
    root.wm_attributes('-toolwindow', 'True')
    root.title('Plant Manager')
    root.geometry("800x800")
    grid_frame = Frame(root)
    add_frame = Frame(root, highlightbackground="#698B69", highlightthickness=2, width= 300, height =300)
    t= Table(grid_frame, root)
    a = Add_Plant(add_frame, t)
    border = LabelFrame(root, bd = 5, relief = SUNKEN, bg= "#698B69")
    border.pack()
    grid_frame.pack()
    add_frame.pack(side=BOTTOM, fill=BOTH, padx = 10, pady =10)
    root.mainloop()
    return

master = Tk()
master.wm_attributes('-toolwindow', 'True')
master.title('Plant Manager')
master.geometry("600x600")
f = Frame(master)
l = Label(f, text="Click here to create a new Plant List and start the Application", font = ("Helvetica", "14", "bold italic"))
open_table = Button(f, text ="Click here", command=lambda: make_list(master), font = ("Helvetica", "10", "bold"))
f.pack(expand=True)
l.pack()
open_table.pack(padx=10,pady=10)
master.mainloop()