import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import calendar
import time
import requests

BASE = 'http://api.aladhan.com/v1/calendarByAddress?address='
IP_URL = 'https://am.i.mullvad.net/json'

METHOD = 2

def get_times(location):
    month = int(time.strftime('%m'))
    year = int(time.strftime('%Y'))
    day = int(time.strftime('%d'))

    url = f'{BASE}{location}&method={METHOD}&month={month}&year={year}'
    try:
        prayer_data = requests.get(url).json()['data']
        fajr_today = prayer_data[day]["timings"]["Fajr"]
        maghrib = prayer_data[day]["timings"]["Maghrib"]

        if day == calendar.monthrange(year, month)[1]:
            fajr_month = ((month == 11) * 12) + ((month + 1) % 12)
            fajr_year = year + (month == 12)
            fajr_url = f'{BASE}{location}&method={METHOD}&month={fajr_month}&year={fajr_year}'
            fajr_tomorrow = requests.get(fajr_url).json()['data'][1]["timings"]["Fajr"]
        else:
            fajr_tomorrow = prayer_data[day+1]["timings"]["Fajr"]

        return f"Fajr [today]: {fajr_today}\nMaghrib: {maghrib}\nFajr [tomorrow]: {fajr_tomorrow}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_location():
    response = requests.get(IP_URL).json()
    return f'{response["latitude"]}, {response["longitude"]}'

def show_prayer_times():
    location = location_entry.get()
    if location:
        prayer_times = get_times(location)
        result_label.config(text=prayer_times)
    else:
        messagebox.showerror("Error", "Please enter a location.")

# GUI setup
root = tk.Tk()
root.title("BY Rayen ben ahmed ")

# Load and display background image
background_image = Image.open("ramadan 2022_0.jpeg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Custom font for the title
title_font = ("Helvetica", 20, "bold")

# Custom font for other text
text_font = ("Helvetica", 12)

location_label = tk.Label(root, text="Enter Location:", font=text_font)
location_label.pack()

location_entry = tk.Entry(root, font=text_font)
location_entry.pack()

get_times_button = tk.Button(root, text="Get Prayer Times", font=text_font, command=show_prayer_times)
get_times_button.pack()

result_label = tk.Label(root, text="", font=text_font)
result_label.pack()

root.mainloop()
