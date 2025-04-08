"""
ICS4U - Software Development Project
Merivale Secondary Calendar System
Formerly by Emin Suhonjic, Osaid El Dali, Justin Yuan
Now by Justin Yuan
Program to display the current school day and any special
events corresponding to the Merivale High School calendar.
"""

# Libraries #
import pandas as pd
import numpy as np
import datetime
import sys
import os.path
import kivy
# Kivy Modules #
from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown

date = datetime.datetime.now()

def fetchDay():
    """
    Function to find the corresponding school day to the current date.
    """
    global df
    global monthslice
    #global rowseries
    global slice2
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSEmrxJzhnV_wvnd2GkiyuVoBviY8kZOhGhBZd7EsraGpzn-9wmCycgWZXAr8tYXSJiBM2GQ-jeLvIt/pub?gid=0&single=true&output=csv',dtype={"MONTH" : np.str_})
    print(df)
    rowseries=np.where(df["MONTH"]==str(date.month))
    print(rowseries)
    monthslice=df[df["MONTH"]==str(date.month)]
    slice2=df.iloc[rowseries[0]+1] #next slice row
    print(monthslice) #loc or iloc are not viable as the indexing is via the month column not the dataframe itself's row indexing
    columnseries=np.where(monthslice.astype(np.str_)==str(date.day)) # must be compared as type str due to NaN values
    #print(date.day)
    #df[]
    #print(df.loc[[str(date.day)]])
    #columnseries=np.where(df.loc[[date.day]]==str(date.day))
    print(columnseries)
    abcdef=rowseries[0][0],columnseries[1][0]
    print(abcdef)
    dayof=df.iloc[abcdef[0]+1,abcdef[1]] # different row (1 under), same column

    return dayof

# Classes #

class testGrid(GridLayout):
    """
    Main class to create the user interface.
    """
    #global monthslice
    def __init__(self,**kwargs):
        formatted_date = str((str(date.year) + "/" + str(date.month) + "/" + str(date.day)))
       # fetchDay(datetime.date.month,datetime.date.day)
        super(testGrid,self).__init__(**kwargs)
        self.cols = 5 # how many columns the grid has
        self.rows=2

        self.datenow=Label(text="The date today is \n"+ formatted_date)
        self.add_widget(self.datenow)

        auugh=fetchDay()
        #print(auugh)
        self.daynow = Label(text=f"Today is: day {auugh}") # Multiline false so you cant add new lines
        self.add_widget(self.daynow)
        
        self.calendarholder=GridLayout(cols=5,rows=8)
        templist="MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"
        for x in templist:
            self.calendarholder.add_widget(Label(text=x))
        #self.calendarholder.add_widget(Label(text='Hello world'))
        #for i in range(30-1+1):
        #    self.calendarholder.add_widget(Label(text=f"Date {i+1}"))
        for i in range(len(monthslice.iloc[0])-1): #1st row is the month
            self.calendarholder.add_widget(Label(text=f"{monthslice.iloc[0][i+1]}\nDay {slice2.iloc[0][i+1]}"))
        self.monthdisplay=Popup(title=f'Test calendar popup for the month of {monthslice.iloc[0][0]}', content=self.calendarholder, size_hint=(None, None), size=(1000, 500))
        self.calbutton=Button(text="click here",size_hint_y=0.25)
        #self.calbutton.bind(on_press=self.monthdisplay.open)
        self.displaydropdown=DropDown()
        #self.displaydropdown.bind(on_release=self.monthdisplay.open)
        for i in range(3):
            btn=Button(text=f"Button {i}",size_hint=(None,None),height=50)
            btn.bind(on_release=lambda btn:self.displaydropdown.select(btn.text))
            btn.bind(on_release=self.monthdisplay.open)
            self.displaydropdown.add_widget(btn)
        #self.anotherbutton=Button(text="auugh")
        #self.anotherbutton.bind(on_release=self.displaydropdown.open)
        self.displaydropdown.bind(on_select=lambda instance,x:setattr(self.calbutton,"text",f"{x} selected")) #changes display of calbutton
        #self.add_widget(self.anotherbutton)
        self.calbutton.bind(on_press=self.displaydropdown.open)
        self.add_widget(self.calbutton)

        self.add_widget(TextInput(text="Text Box:"))
        for i in range(3):
            self.add_widget(Label(text="Placeholder"))
        #self.displaydropdown=Spinner(text="clikc me!",values=("Display by Day",'Display by Week',"Display by Month"),size_hint=(None,None))
        #self.displaydropdown.bind(text=show_selected_value)

        #self.displaydropdown.bind(on_press=stupid(self.displaydropdown,self.displaydropdown.text))
        #stupid()

 
# App Runtime #

class MyApp(App):
    """
    App builder
    """
    def build(self):
        return testGrid()

if __name__ == "__main__":
    #fetchDay()
    MyApp().run()
