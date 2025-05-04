import csv
import os
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown

#os.environ["SDL_VIDEODRIVER"] = "dummy"

"""try:
    from kivy.core.clipboard import Clipboard
except ImportError:
    # Replace with a mock Clipboard if needed
    class Clipboard:
        def copy(text):
            pass  # No operation

        def paste():
            return ""  # Return empty string"""

class CSVData(BoxLayout):
    def __init__(self,**kwargs):
        super(CSVData,self).__init__(**kwargs)
        #self.user_data=self.load_data()
        self.value_input=TextInput(hint_text="Enter text here: ",size_hint=(1,1))
        thing=DropDown()
        baton=Button(text="clack me pls",on_release=lambda baton:thing.select(baton.text))
        #baton.bind(on_release=lambda baton:self.thing.select(baton.text))
        btn=Button(text="pres 2 change",height=10,width=10,on_press= lambda btn:self.add_info("placeholder insert"))#,on_press=self.thing.select(btn.text))
        thing.add_widget(btn)
        thing.add_widget(baton)
        thing.bind(on_select=lambda instance, x: setattr(btn, 'text', x))
        #self.add_widget(thing)
        self.display=GridLayout(cols=5,rows=4)
        self.add_button=Button(text="Add Information?",height=50, width=50)
        self.add_button.bind(on_release=lambda instance:self.open_dropdown(thing))
        #print(self.load_data())
        internaldf=self.load_data()
        print(f"internal df:\n{internaldf}")
        self.save_button=Button(text="Confirm?",on_press=lambda instance:self.save_data(internaldf))
        #with open(self.data_file, "r", newline="") as f:
        #    reading=csv.reader(f)
        #    for row in reading:
        #        for value in row:
        #            self.display.add_widget(Label(text=value,size_hint=(0.5,0.5)))
                #self.display
        #layout=BoxLayout()
        #layout.add_widget(self.user_data)
        self.add_widget(self.value_input)
        self.add_widget(self.add_button)
        self.add_widget(self.display)
        self.add_widget(self.save_button)
        self.display_label=Label(text="lorem",size_hint=(1,1))
        self.add_widget(self.display_label)
        self.add_widget(Label(text="ipsum",size_hint=(1,1)))
        self.display.add_widget(Label(text="dolor",size_hint=(1,1)))



    def open_dropdown(self, instance):
        print("Dropdown open function called!")
        #thing = instance.parent.children[3] # Assuming self.add_button is the 4th child added
        self.open(instance)
        
    data_file="test.csv"
    header=["Bloack","Day 1", "Day 2","Day3","Day 4"]
    rows=["A","B","C","D"]
    def load_data(self):
        #data=pd.DataFrame({"Bloack","Day 1", "Day 2","Day3","Day 4"})
        #data=pd.DataFrame(columns=CSVData.header,index=CSVData.rows)
        data=pd.read_csv("test.csv",index_col="Bloack")
        """if os.path.exists(self.data_file):
            with open(self.data_file, "r", newline="") as f:
                reading=csv.reader(f)
                for row in reading:
                    #for value in row:
                    if len(row)==2:
                        data.append(row)"""

        return data

    def save_data(self, data):
        #with open(self.data_file, "w", newline="") as f:
        with open(self.data_file, "w") as f:

            writing=csv.writer(f)
            writing.writerow(self.header)
            writing.writerow(data)
            #***save "data" within the program (while being edited) as a 2d list instead of whatever im doing rn + or A DATAFRAME! wow
    def add_info(self,instance):
        pass
        #thing.open
        #newinfo=self.value_input.text
#        CSVData.internaldf=
    #value1=input("Enter 1st value: ")
    #value2=input("Enter 2nd value: ")
        #self.save_data(newinfo)
        #self.display_label.text=self.formatted_data()

    """def formatted_data(self):
        if not self.user_data:
            return "No data stored"
        output="Stored Data:\n"
        for value1,value2 in self.user_data:
            output+=f"Value 1: {value1}, Value 2 {value2}"
            return output"""

class Application(App):
    """stupid"""
    def build(self):
        return CSVData()
if __name__=="__main__":
    Application().run()
