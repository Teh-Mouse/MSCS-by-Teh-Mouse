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
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout # Import BoxLayout

# Load the KV file
kv_file = Builder.load_string("""
<testGrid>:
    cols: 1
    rows: 1
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        GridLayout:  # 2x layout for datenow, daynow, textbox, placeholder
            cols: 2
            rows: 2
            size_hint_y: None
            height: 200

            Label:
                id: datenow
                text: "The date today is \\n"
            Label:
                id: daynow
                text: "Today is: day "
            Label:
                text: "Text Box:" # Changed from Label
            Label:
                text: "Placeholder"

        GridLayout: # Calendar
            id: calendarholder
            cols: 5
            rows: 8
            size_hint_y: None
            height: 400

        BoxLayout: # Button at the bottom
            size_hint_y: None
            height: 50
            Button:
                id: calbutton
                text: "click here"
                size_hint_x: 1
                size_hint_y: None
                height: 50

        GridLayout: # bottom placeholders
            cols: 2
            rows: 1
            size_hint_y: None
            height: 50
            Label:
                text: "Placeholder"
            Label:
                text: "Placeholder"
""")


date = datetime.datetime.now()

def fetchDay():
    """
    Function to find the corresponding school day to the current date.
    """
    global df
    global monthslice
    global slice2
    df = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/e/2PACX-1vSEmrxJzhnV_wvnd2GkiyuVoBviY8kZOhGhBZd7EsraGpzn-9wmCycgWZXAr8tYXSJiBM2GQ-jeLvIt/pub?gid=0&single=true&output=csv',
        dtype={"MONTH": np.str_})
    print(df)
    rowseries = np.where(df["MONTH"] == str(date.month))
    print(rowseries)
    monthslice = df[df["MONTH"] == str(date.month)]
    slice2 = df.iloc[rowseries[0] + 1]
    print(monthslice)
    columnseries = np.where(
        monthslice.astype(np.str_) == str(date.day))
    print(columnseries)
    if columnseries[0].size > 0 and columnseries[1].size > 0: #check to avoid error if no match
        abcdef = rowseries[0][0], columnseries[1][0]
        print(abcdef)
        dayof = df.iloc[abcdef[0] + 1, abcdef[1]]
    else:
        dayof = "No Day Found" # Default Value
    return dayof

class testGrid(Screen):
    """
    Main class to create the user interface.
    """
    def __init__(self, **kwargs):
        formatted_date = str((str(date.year) + "/" + str(date.month) + "/" + str(date.day)))
        super(testGrid, self).__init__(**kwargs)

        self.datenow = self.ids.datenow # Get the instance using ID
        self.datenow.text = "The date today is \n" + formatted_date

        auugh = fetchDay()
        self.daynow = self.ids.daynow
        self.daynow.text = f"Today is: day {auugh}"

        # Create a new GridLayout for the popup content.  This is used for the calendar popup
        calendar_popup_content = GridLayout(cols=5, rows=8)
        templist = "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"
        for x in templist:
            calendar_popup_content.add_widget(Label(text=x))

        for i in range(len(monthslice.iloc[0]) - 1):
            calendar_popup_content.add_widget(Label(text=f"{monthslice.iloc[0][i + 1]}\nDay {slice2.iloc[0][i + 1]}"))

        self.monthdisplay = Popup(title=f'Test calendar popup for the month of {monthslice.iloc[0][0]}', content=calendar_popup_content, size_hint=(None, None), size=(1000, 500))
        self.calbutton = self.ids.calbutton
        self.displaydropdown = DropDown()
        for i in range(3):
            btn = Button(text=f"Button {i}", size_hint=(None, None), height=50)
            btn.bind(on_release=lambda btn: self.displaydropdown.select(btn.text))
            btn.bind(on_release=self.monthdisplay.open)
            self.displaydropdown.add_widget(btn)
        self.displaydropdown.bind(on_select=lambda instance, x: setattr(self.calbutton, "text", f"{x} selected"))
        self.calbutton.bind(on_press=self.displaydropdown.open)

class MyApp(App):
    """
    App builder
    """

    def build(self):
        sm = ScreenManager()
        sm.add_widget(testGrid(name='test'))
        return sm

if __name__ == "__main__":
    MyApp().run()
