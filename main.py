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
from kivy.uix.boxlayout import BoxLayout  # Import BoxLayout

# Load the KV file
kv_file = Builder.load_string("""
<testGrid>:
    cols: 1
    rows: 1
    GridLayout:
        cols: 2
        padding: 50
        spacing: 25

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
        Button:
            id: calbutton
            text: "click here"
            size_hint_x: 1
            size_hint_y: None
            height: 50
""")

date = datetime.datetime.now()


def fetchDay(month=None, day=None):
    """
    Function to find the corresponding school day to the current date.
    Can optionally take a specific month and day.
    """
    global df
    global monthslice
    global dayslice
    use_month = month if month else date.month
    use_day = day if day else date.day

    df = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/e/2PACX-1vSEmrxJzhnV_wvnd2GkiyuVoBviY8kZOhGhBZd7EsraGpzn-9wmCycgWZXAr8tYXSJiBM2GQ-jeLvIt/pub?gid=0&single=true&output=csv',
        dtype={"MONTH": np.str_})
    print(df)
    rowseries = np.where(df["MONTH"] == str(use_month))
    print(f"rowseries:{rowseries}")
    monthslice = df.iloc[rowseries[0]]
    dayslice = df.iloc[rowseries[0] + 1]
    print(monthslice)
    print(dayslice)
    columnseries = np.where(
        monthslice.astype(np.str_) == str(use_day))
    print(f"columnseries: {columnseries}")
    if columnseries[0].size > 0 and columnseries[1].size > 0:  # check to avoid error if no match
        abcdef = rowseries[0][0], columnseries[1][0]
        print(abcdef)
        dayof = df.iloc[abcdef[0] + 1, abcdef[1]]
    else:
        dayof = "No Day Found"  # Default Value
    return dayof


class testGrid(Screen):
    """
    Main class to create the user interface.
    """

    def __init__(self, **kwargs):
        formatted_date = str((str(date.year) + "/" + str(date.month) + "/" + str(date.day)))
        super(testGrid, self).__init__(**kwargs)

        self.datenow = self.ids.datenow  # Get the instance using ID
        self.datenow.text = "The date today is \n" + formatted_date

        auugh = fetchDay()
        self.daynow = self.ids.daynow
        self.daynow.text = f"Today is: Day {auugh}"

        # Initialize the calendar holder and baton button
        self.calendarholder = GridLayout(cols=1, rows=2, size_hint_y=None, height=400)
        self.baton = Button(text="Select Month", size_hint_y=None, height=50)
        self.calendarholder.add_widget(self.baton)

        # Create initial calendar popup for current month
        self.current_month = date.month
        self.create_calendar_popup(self.current_month)

        # Create dropdown with school year months
        self.create_month_dropdown()

        self.calbutton = self.ids.calbutton
        self.calbutton.bind(on_release=self.monthdisplay.open)

    def create_calendar_popup(self, month):
        """Create or update the calendar popup for the specified month"""
        self.current_month = month

        # Fetch data for the specified month
        monthslice = self.get_month_data(month)
        dayslice = self.get_day_data(month)

        # Clear previous calendar content if it exists
        if hasattr(self, 'calendar_content'):
            self.calendarholder.remove_widget(self.calendar_content)

        # Create new calendar content
        self.calendar_content = GridLayout(cols=5, rows=8)
        templist = "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"
        for x in templist:
            self.calendar_content.add_widget(Label(text=x))

        for i in range(len(monthslice.iloc[0]) - 1):
            self.calendar_content.add_widget(
                Label(text=f"{monthslice.iloc[0][i + 1]}\nDay {dayslice.iloc[0][i + 1]}"))

        # Add the calendar content above the baton button
        self.calendarholder.add_widget(self.calendar_content)
        self.calendarholder.remove_widget(self.baton)
        self.calendarholder.add_widget(self.baton)

        # Update baton button text
        month_name = datetime.date(1900, month, 1).strftime('%B')
        self.baton.text = f"Viewing: {month_name}"

        # Create or update the popup
        if not hasattr(self, 'monthdisplay'):
            self.monthdisplay = Popup(
                title=f'Calendar for {month_name}',
                content=self.calendarholder,
                size_hint=(None, None),
                size=(1000, 500))
        else:
            self.monthdisplay.title = f'Calendar for {month_name}'
            self.monthdisplay.content = self.calendarholder

    def create_month_dropdown(self):
        """Create dropdown menu for school year months"""
        self.month_dropdown = DropDown()

        # School year months: September (9) to December (12), then January (1) to June (6)
        school_year_months = list(range(9, 13)) + list(range(1, 7))

        for month_num in school_year_months:
            month_name = datetime.date(1900, month_num, 1).strftime('%B')
            btn = Button(text=month_name, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn, m=month_num: self.select_month(m))
            self.month_dropdown.add_widget(btn)

        # Bind the dropdown to the baton button
        self.baton.bind(on_release=self.month_dropdown.open)

    def select_month(self, month_num):
        """Handle month selection from dropdown"""
        self.month_dropdown.dismiss()
        self.create_calendar_popup(month_num)
        # Re-open the popup to show the updated calendar
        self.monthdisplay.open()

    def get_month_data(self, month):
        """Get month data from spreadsheet"""
        df = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vSEmrxJzhnV_wvnd2GkiyuVoBviY8kZOhGhBZd7EsraGpzn-9wmCycgWZXAr8tYXSJiBM2GQ-jeLvIt/pub?gid=0&single=true&output=csv',
            dtype={"MONTH": np.str_})
        rowseries = np.where(df["MONTH"] == str(month))
        return df.iloc[rowseries[0]]

    def get_day_data(self, month):
        """Get day data from spreadsheet"""
        df = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vSEmrxJzhnV_wvnd2GkiyuVoBviY8kZOhGhBZd7EsraGpzn-9wmCycgWZXAr8tYXSJiBM2GQ-jeLvIt/pub?gid=0&single=true&output=csv',
            dtype={"MONTH": np.str_})
        rowseries = np.where(df["MONTH"] == str(month))
        return df.iloc[rowseries[0] + 1]


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
