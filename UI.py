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
    def __init__(self, root):
        self.root =root
        self.plants = []
        self.row_index = 2
        self.e = Label(root, text = "My Plant List", width=10, font = ("Helvetica", "16", "bold italic"))
        self.e.grid(row=0, column=2)
        headers = ["Plant", "Next Water Date", "Next Fertilize Date", "Mark Watered", "Mark Fertilized"]
        for i in range(len(headers)):
            self.e = Label(root,text= headers[i], width= 15, font = ("Helvetica", "10", "bold"), relief='ridge')
            self.e.grid(row=1, column=i, sticky ="nsew")

    def add_row(self, name, water, fert):
        self.plants.append(Plant(name, water, fert))
        self.name = Label(self.root, text = name)
        self.name.grid(row=self.row_index, column=0, sticky='nsew')
        self.row_index+=2



class Add_Plant():
    def __init__(self, root, plant_grid):
        self.plant_grid = plant_grid
        self.e = Label(root, text="Add Plant", font = ("Helvetica", "16", "bold italic"))
        self.e.pack(side=LEFT)
        self.e = Label(root, text="Enter Plant Name")
        self.plant_name = Entry(root, width =15)
        self.e.pack()
        self.plant_name.pack()
        self.e = Label(root, text="Enter Watering Interval in Days")
        self.watering = Entry(root, width =15)
        self.e.pack()
        self.watering.pack()
        self.e = Label(root, text="Enter Fertilizing Interval in Days")
        self.fertilizing = Entry(root, width=15)
        self.e.pack()
        self.fertilizing.pack()
        self.submit = Button(root,text="Submit", command = self.get_text)
        self.submit.pack(padx = 10, pady =10)

    def get_text(self):
        name = self.plant_name.get()
        water = self.watering.get()
        fert = self.fertilizing.get()
        self.plant_grid.add_row(name, water, fert)
        self.plant_name.delete(0, END)
        self.watering.delete(0, END)
        self.fertilizing.delete(0, END)


def make_list():
    """"""
    master.destroy()
    root = Tk()
    root.geometry("700x700")
    grid_frame = Frame(root)
    add_frame = Frame(root, highlightbackground="#698B69", highlightthickness=2, width= 300, height =300)
    t= Table(grid_frame)
    a = Add_Plant(add_frame, t)
    border = LabelFrame(root, bd = 5, relief = SUNKEN, bg= "#698B69")
    border.pack()
    grid_frame.pack()
    add_frame.pack(side=BOTTOM, fill=BOTH, padx = 10, pady =10)
    root.mainloop()
    return

master = Tk()
master.geometry("400x400")
f = Frame(master)
l = Label(f, text="Click here to create a new Plant List and Start Application", font = ("Helvetica", "10", "bold italic"))
open_table = Button(f, text ="Click here", command=make_list, font = ("Helvetica", "10", "bold"))
f.pack(expand=True)
l.pack()
open_table.pack(padx=10,pady=10)
master.mainloop()