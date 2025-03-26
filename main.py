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

date = datetime.datetime.now()

def fetchDay():
    """
    Function to find the corresponding school day to the current date.
    """
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSEmrxJzhnV_wvnd2GkiyuVoBviY8kZOhGhBZd7EsraGpzn-9wmCycgWZXAr8tYXSJiBM2GQ-jeLvIt/pub?gid=0&single=true&output=csv',dtype={"MONTH" : np.str_})
    print(df)
    rowseries=np.where(df["MONTH"]==str(date.month))
    print(rowseries)
    rowslice=df[df["MONTH"]==str(date.month)]
    print(rowslice)
    columnseries=np.where(rowslice.astype(np.str_)==str(date.day)) # must be compared as type str due to NaN values
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
        self.calendarholder.add_widget(Label(text='Hello world'))
        for i in range(30-1+1):
            self.calendarholder.add_widget(Label(text=f"Date {i+1}"))
        self.hello=Popup(title='Test calendar popup (month)', content=self.calendarholder, size_hint=(None, None), size=(1000, 500))
        self.calbutton=Button(text="click here")
        self.calbutton.bind(on_press=self.hello.open)
        self.add_widget(self.calbutton)

        self.add_widget(TextInput(text="Text Box:"))
        for i in range(3):
            self.add_widget(Label(text="Placeholder"))
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
