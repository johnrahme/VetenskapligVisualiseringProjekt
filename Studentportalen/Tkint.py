# -*- coding: utf-8 -*-
"""
Created on Sat Oct 08 13:55:36 2016

@author: Muhrbeck
"""

import Tkinter
import time

global variablemax, variablemin
variablemax = 8
variablemin = 0


class app_tk(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.running = None
        self.initialize()           
        
    def initialize(self):
        self.grid()
        
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0, row=0)
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here")
        
        self.EndMagnitude = Tkinter.DoubleVar()
        Magmax = Tkinter.Scale(self,label="Maximum magnitude", variable = self.EndMagnitude ,from_=variablemax,to=0,tickinterval=1,resolution=0.01, orient ='vertical')
        Magmax.set(variablemax)
        Magmax.pack()
        Magmax.grid(column=3, row=0)
        
        self.StartMagnitude = Tkinter.DoubleVar()
        Magmin = Tkinter.Scale(self,label="Lowest magnitude",variable = self.StartMagnitude, from_=10,to=0,tickinterval=1,resolution=0.01,orient ='vertical')
        Magmin.set(0)
        Magmin.pack()
        Magmin.grid(column=2, row=0)
        
        self.StartTime = Tkinter.DoubleVar()
        t1 = Tkinter.Scale(self,label="Start time",variable = self.StartTime, from_=0,to=300,tickinterval=50, length=300, orient = 'horizontal')
        t1.set(0)
        t1.pack()
        t1.grid(column=1, row=0)
        
        self.EndTime = Tkinter.DoubleVar()
        t2 = Tkinter.Scale(self,label="End time",variable = self.EndTime, from_=0,to=300,tickinterval=50, length=300, orient = 'horizontal')
        t2.set(300)
        t2.pack()
        t2.grid(column=1, row=1)
        
        
        button1 = Tkinter.Button(self,text="Toggle Map on/off", 
                                 command=self.OnMapClick)
        button1.grid(column=1, row=2)
        
        
        button2 = Tkinter.Button(self,text="Toggle between 2D/3D map", 
                                 command=self.OnToggleClick)
        button2.grid(column=1, row=3)
        
        
        button3 = Tkinter.Button(self,text="Toggle colorbars on/off", 
                                 command=self.OnColorbarClick)
        button3.grid(column=1, row=4)
        
        
        button4 = Tkinter.Button(self,text="Slider for time on/off", 
                                 command=self.OnTimeClick)
        button4.grid(column=1, row=5)
        
        
        button5 = Tkinter.Button(self,text="Slider for magnitude on/off", 
                                 command=self.OnMagnitudeClick)
        button5.grid(column=1, row=6)
        
        
        button6 = Tkinter.Button(self,text="Want other colors?", 
                                 command=self.OnColorblindClick)
        button6.grid(column=1, row=7)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable = self.labelVariable, 
                              anchor="w", fg="white", bg="black")
        label.grid(column=0, row=1, columnspan=2, sticky='W')
        self.labelVariable.set(u"Hello")
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
    def OnMapClick(self):
        self.labelVariable.set("(Map)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
        
    def OnToggleClick(self):
        self.labelVariable.set("(Toggle)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
    
    def OnColorbarClick(self):
        self.labelVariable.set("(Colorbar)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
    
    def OnTimeClick(self):
        self.labelVariable.set(str(self.StartTime.get()) + str(",") + str(self.EndTime.get()) + "(Time)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
    
    def OnMagnitudeClick(self):
        #self.labelVariable.set(variablemin, variablemax, "(Magnitude)")
        self.labelVariable.set(str(self.StartMagnitude.get()) + str(",") + str(self.EndMagnitude.get()) + "(Magnitude (min,max))")      
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
        
    def OnColorblindClick(self):
        self.labelVariable.set("(Colorblind)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
        
    def OnPressEnter(self,event):
        self.labelVariable.set(self.entryVariable.get()+ "(You pressed Enter)")
        #self.entry.focus_set()
        #self.entry.selection_range(0,Tkinter.END)

        
    
if __name__ == "__main__":
    app = app_tk(None)
    app.title('GUI')
    app.mainloop()
    