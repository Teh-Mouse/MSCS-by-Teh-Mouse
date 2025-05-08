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
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex

# Load the KV file
kv_file = Builder.load_string("""
<CalendarLabel>:
    background_color: 0.7, 0.7, 0.7, 1
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size

<testGrid>:
    cols: 1
    rows: 1
    GridLayout:
        cols: 2
        padding: 50
        spacing: 25

        CalendarLabel:
            id: datenow
            text: "The date today is \\n"
            font_size: 32
        CalendarLabel:
            id: daynow
            text: "Today is: Day "
            font_size: 32
        Button:
            id: calbutton
            text: "Display Calendar"
            size_hint_x: 1
            size_hint_y: None
            height: 50
            background_color: 0.7, 0.7, 0.7, 1
""")


class CalendarLabel(Label):
    pass


date = datetime.datetime.now()


def fetchDay(month=None, day=None):
    """Function to find the corresponding school day to the current date."""
    global df
    global monthslice
    global dayslice
    use_month = month if month else date.month
    use_day = day if day else date.day

    df = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/e/2PACX-1vSEmrxJzhnV_wvnd2GkiyuVoBviY8kZOhGhBZd7EsraGpzn-9wmCycgWZXAr8tYXSJiBM2GQ-jeLvIt/pub?gid=0&single=true&output=csv',
        dtype={"MONTH": np.str_})
    rowseries = np.where(df["MONTH"] == str(use_month))
    monthslice = df.iloc[rowseries[0]]
    dayslice = df.iloc[rowseries[0] + 1]
    columnseries = np.where(monthslice.astype(np.str_) == str(use_day))
    if columnseries[0].size > 0 and columnseries[1].size > 0:
        abcdef = rowseries[0][0], columnseries[1][0]
        dayof = df.iloc[abcdef[0] + 1, abcdef[1]]
    else:
        dayof = "No Day Found"
    return dayof


class testGrid(Screen):
    """Main class to create the user interface."""

    def __init__(self, **kwargs):
        super(testGrid, self).__init__(**kwargs)
        formatted_date = f"{date.year}/{date.month}/{date.day}"
        self.datenow = self.ids.datenow
        self.datenow.text = f"The date today is \n{formatted_date}"
        self.daynow = self.ids.daynow
        self.daynow.text = f"Today is: Day {fetchDay()}"

        # Initialize calendar
        self.current_month = date.month
        self.calendarholder = GridLayout(cols=1, rows=2, size_hint_y=None, height=400)
        self.baton = Button(text="Select Month", size_hint_y=None, height=50, background_color=(0.7, 0.7, 0.7, 1))
        self.calendarholder.add_widget(self.baton)

        self.create_calendar_popup(self.current_month)
        self.create_month_dropdown()

        self.ids.calbutton.bind(on_release=self.monthdisplay.open)

    def format_day_value(self, value):
        """Format day values to handle NaN and convert to integers"""
        if pd.isna(value):
            return ""
        try:
            # Convert to integer if it's a number
            return str(int(float(value)))
        except (ValueError, TypeError):
            return str(value)

    def create_calendar_popup(self, month):
        """Create or update the calendar popup for the specified month."""
        self.current_month = month
        monthslice = self.get_month_data(month)
        dayslice = self.get_day_data(month)

        if hasattr(self, 'calendar_content'):
            self.calendarholder.remove_widget(self.calendar_content)

        # Create calendar grid with grey background
        self.calendar_content = GridLayout(cols=5, rows=8, spacing=5, padding=5)

        # Add weekday headers
        for day in ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]:
            day_label = CalendarLabel(text=day, bold=True, font_size=24)
            self.calendar_content.add_widget(day_label)

        # Add calendar days
        for i in range(len(monthslice.iloc[0]) - 1):
            day_num = self.format_day_value(monthslice.iloc[0][i + 1])
            day_value = self.format_day_value(dayslice.iloc[0][i + 1])

            # Skip if both day_num and day_value are empty
            if not day_num and not day_value:
                day_label = CalendarLabel(text="", font_size=20)
            else:
                day_text = f"{day_num}\nDay {day_value}" if day_value else str(day_num)
                day_label = CalendarLabel(text=day_text, font_size=20)

                # Highlight current day in red
                if month == date.month and day_num and str(int(float(monthslice.iloc[0][i + 1]))) == str(date.day):
                    day_label.color = get_color_from_hex('#FF0000')

            self.calendar_content.add_widget(day_label)

        # Update container
        self.calendarholder.add_widget(self.calendar_content)
        if self.baton in self.calendarholder.children:
            self.calendarholder.remove_widget(self.baton)
        self.calendarholder.add_widget(self.baton)

        # Update month name and popup
        month_name = datetime.date(1900, month, 1).strftime('%B')
        self.baton.text = f"Viewing: {month_name}"

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
        """Create month selection dropdown."""
        self.month_dropdown = DropDown()
        for month_num in [*range(9, 13), *range(1, 7)]:
            month_name = datetime.date(1900, month_num, 1).strftime('%B')
            btn = Button(text=month_name, size_hint_y=None, height=50, background_color=(0.7, 0.7, 0.7, 1))
            btn.bind(on_release=lambda btn, m=month_num: self.select_month(m))
            self.month_dropdown.add_widget(btn)
        self.baton.bind(on_release=self.month_dropdown.open)

    def select_month(self, month_num):
        """Handle month selection."""
        self.month_dropdown.dismiss()
        self.create_calendar_popup(month_num)
        self.monthdisplay.open()

    def get_month_data(self, month):
        df = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vSEmrxJzhnV_wvnd2GkiyuVoBviY8kZOhGhBZd7EsraGpzn-9wmCycgWZXAr8tYXSJiBM2GQ-jeLvIt/pub?gid=0&single=true&output=csv',
            dtype={"MONTH": np.str_})
        rowseries = np.where(df["MONTH"] == str(month))
        return df.iloc[rowseries[0]]

    def get_day_data(self, month):
        df = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vSEmrxJzhnV_wvnd2GkiyuVoBviY8kZOhGhBZd7EsraGpzn-9wmCycgWZXAr8tYXSJiBM2GQ-jeLvIt/pub?gid=0&single=true&output=csv',
            dtype={"MONTH": np.str_})
        rowseries = np.where(df["MONTH"] == str(month))
        return df.iloc[rowseries[0] + 1]


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(testGrid(name='test'))
        return sm


if __name__ == "__main__":
    MyApp().run()
