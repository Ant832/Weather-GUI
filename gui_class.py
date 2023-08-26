import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as st
import tkinter.font as tkFont
import requests
import json
from datetime import datetime
import sys
from geopy.geocoders import Nominatim
import geocoder

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('1000x500')
        self.configure(background='lightblue')
        self.label = tk.Label(self, text="Enter Location", font=(20), background='lightblue')
        self.button1 = tk.Button(self, text="Use My Location", command=self.on_button1, background='lightyellow')
        self.entry =tk.Entry(self, width=40)
        self.button2 = tk.Button(self, text="Submit", command=self.on_button2, background='lightyellow')
        self.label.pack()
        self.entry.pack()
        self.button2.pack(pady=(5, 30))
        self.button1.pack()

    def restart(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry('1000x500')
        self.configure(background='lightblue')
        self.label = tk.Label(self, text="Enter Location", font=(20), background='lightblue')
        self.button1 = tk.Button(self, text="Use My Location", command=self.on_button1, background='lightyellow')
        self.entry =tk.Entry(self, width=40)
        self.button2 = tk.Button(self, text="Submit", command=self.on_button2, background='lightyellow')
        self.label.pack()
        self.entry.pack()
        self.button2.pack(pady=(5, 30))
        self.button1.pack()

    def callback(self):
        for widget in self.winfo_children():
            widget.destroy()
        invalid_label = tk.Label(self, text="Invalid Location", font=(20), background='lightblue')
        invalid_label.pack()
        continue_btn = tk.Button(self, text="Continue", command=self.restart, background='lightyellow')
        continue_btn.pack()

    def on_button1(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.weather_input()


    def on_button2(self):
        geolocator = Nominatim(user_agent='iasd93ad99ad90(FJ0)')
        self.location = geolocator.geocode(self.entry.get())
        if self.location == None:
            self.callback()
        else:
            self.weather_input(self.entry.get())

    
    def jprint(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        return text

    def weather_input(self, user_input='me'):
        if user_input == 'me':
            geo = geocoder.ip('me')
            location = geo.latlng
            geolocator = Nominatim(user_agent='new_agent')
            name = geolocator.reverse(str(location[0]) + ',' + str(location[1]))
            name = str(name).split(',')
            name = ','.join(name)
            response = requests.request("GET", f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location[0]}%2C%20{location[1]}?unitGroup=us&include=days&key=CT6WV6Q636CVFFCWJBB3FTBZB&contentType=json")
        else:
            geolocator = Nominatim(user_agent='new_agent')
            location = geolocator.geocode(self.entry.get())
            for widget in self.winfo_children():
                widget.destroy()
            name = geolocator.reverse(str(location.latitude) + ',' + str(location.longitude))
            address = name.raw['address']
            try:
                if 'town' in address:
                    name = f"{address['town']}, {address['state']}, {address['postcode']}, {address['country']}"
                elif 'suburb' in address:
                    name = f"{address['suburb']}, {address['state']}, {address['postcode']}, {address['country']}"
                elif 'city' in address:
                    name = f"{address['city']}, {address['state']}, {address['postcode']}, {address['country']}"
                else:
                    name = f"{address['village']}, {address['state']}, {address['postcode']}, {address['country']}"
            except:
                self.callback()
                return
                # ^ use if name wants to be rewritten to whatever in try blocks
                # pass
            response = requests.request("GET", f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location.latitude}%2C%20{location.longitude}?unitGroup=us&include=days&key=CT6WV6Q636CVFFCWJBB3FTBZB&contentType=json")
            
        
        if response.status_code!=200:
            for widget in self.winfo_children():
                widget.destroy()
            error = tk.Label(text=f'Unexpected Status code: {response.status_code}')
            error.pack()
            sys.exit()

        bigFont = tkFont.Font(family='Helvetica', size=13, weight='bold')
        smallFont = tkFont.Font(family='Helvetica', size=12)
        mylist = st.ScrolledText(self, height=20, background='lightblue')

        jsonData = response.json()
        # print(jprint(jsonData))
        location_label = tk.Label(self, text=f'Location: {name}', font=(20), background='lightblue')
        location_label.pack(pady=(10, 0))
        for item in jsonData['days']:
            day = str(item['datetime'])
            day = day.split('-')
            day = datetime(int(day[0]), int(day[1]), int(day[2])).ctime()[:-14] + datetime(int(day[0]), int(day[1]), int(day[2])).ctime()[-5:]
            desc = str(item['description'])
            # if 'Partly cloudy' in desc:
            #     desc += ('\U00026C5')
            temp = str(item['temp'])
            tempmax = str(item['tempmax'])
            tempmin = str(item['tempmin'])
            precip = str(item['precipprob'])
            
            # file.write(f'{day}:\n {desc} \n {tempmax} F {tempmin} F\n Precipitation Chance: {precip}%\n')
            mylist.insert(END, f'{day}\n', 'big')
            mylist.insert(END, f'\t{desc}\n', 'small')
            mylist.insert(END, f'\tTemperature: {temp}{chr(176)}F\n', 'small')
            mylist.insert(END, f'\tHigh: {tempmax}{chr(176)}F\n', 'small')
            mylist.insert(END, f'\tLow: {tempmin}{chr(176)}F\n', 'small')
            mylist.insert(END, f'\tPrecipitation: {precip}\n', 'small')
            
        mylist.tag_config('big', font=bigFont)
        mylist.tag_config('small', font=smallFont)
        mylist.pack( side = TOP, fill = BOTH , padx = 20 )
        mylist.configure(state ='disabled')

        back_btn = tk.Button(self, text="<-", command=self.restart, background='lightyellow')
        back_btn.pack()


def main():
    gui = GUI()
    gui.mainloop()
    

if __name__ == '__main__':
    main()
