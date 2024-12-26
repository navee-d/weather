from tkinter import *
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from PIL import Image, ImageTk
from tkinter import messagebox
import sys
import os


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x400+325+150")
        self.root.title("Weather App")
        self.root.resizable(False, False)
        self.root.configure(bg="green")


        # Dynamically find paths to resources for compatibility with .exe
        if getattr(sys, 'frozen', False):  # If running as .exe
            self.base_path = sys._MEIPASS
        else:  # If running as a script
            self.base_path = os.path.abspath(".")

        # Load background image
        try:
            #background_path = os.path.join(self.base_path, "1111at 20.56.53_16f9cdc6.jpg")
            self.background_image = ImageTk.PhotoImage(file=background_path)
            background_label = Label(self.root, image=self.background_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Error", f"Background image not found: {e}")
            return

        # City input field
        self.var_city = StringVar()
        self.entry_city = Entry(self.root, textvariable=self.var_city, font=("Arial", 20), justify=CENTER,bg="#505454" , fg="black")
        self.entry_city.place(x=405, y=35, width=240)

        # Search button
        try:
            button_path = os.path.join(self.base_path, "next-buttonnavee.png")
            self.search_icon = PhotoImage(file=button_path)
            Button(self.root, image=self.search_icon, borderwidth=0, cursor="hand2",bg="#505454" ,command=self.get_weather).place(x=650, y=35)
        except Exception as e:
            messagebox.showerror("Error", f"Search button image not found: {e}")
            return

        # Weather information labels
        self.label_city = Label(self.root, text="", font=("times 20 bold"), bg="#137EA8", fg="black")
        self.label_city.place(x=20, y=70)

        self.label_temp = Label(self.root, text="", font=("times 35 bold"), bg="#137EA8", fg="black")
        self.label_temp.place(x=20, y=150)

        self.label_description = Label(self.root, text="", font=("times 14 bold"), bg="#505454", fg="black")
        self.label_description.place(x=130, y=335)

        self.label_wind = Label(self.root, text="", font=("times 14 bold"), bg="#505454", fg="black")
        self.label_wind.place(x=280, y=335)

        self.label_humidity = Label(self.root, text="", font=("times 14 bold"), bg="#505454", fg="black")
        self.label_humidity.place(x=390, y=335)

        self.label_pressure = Label(self.root, text="", font=("times 14 bold"), bg="#505454", fg="black")
        self.label_pressure.place(x=500, y=335)

        Label(self.root, text="DESCRIPTION", font=("times 13 bold"), bg="#505454", fg="white").place(x=130, y=310)
        Label(self.root, text="WIND", font=("times 13 bold"), bg="#505454", fg="white").place(x=280, y=310)
        Label(self.root, text="HUMIDITY", font=("times 13 bold"), bg="#505454", fg="white").place(x=390, y=310)
        Label(self.root, text="PRESSURE", font=("times 13 bold"), bg="#505454", fg="white").place(x=500, y=310)

    def get_weather(self):
        city = self.var_city.get()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        try:
            # Get location coordinates
            geolocator = Nominatim(user_agent="weatherApp")
            location = geolocator.geocode(city)
            if not location:
                messagebox.showerror("Error", "City not found. Try again.")
                return

            # Get timezone
            timezone_finder = TimezoneFinder()
            timezone = timezone_finder.timezone_at(lng=location.longitude, lat=location.latitude)
            local_time = datetime.now(pytz.timezone(timezone)).strftime("%I:%M %p")

            # Get weather data
            api_key = "7ac47ff3e33248167ddcb104ffd19acd"  # Replace with your actual OpenWeatherMap API key
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data["cod"] != 200:
                messagebox.showerror("Error", data["message"])
                return

            # Update UI with weather data
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            condition = data["weather"][0]["main"].lower()

            self.label_city.config(text=f"{city.upper()} | {local_time}")
            self.label_temp.config(text=f"{temp}°C")
            self.label_description.config(text=f"{description.capitalize()}")
            self.label_wind.config(text=f"{wind_speed} m/s")
            self.label_humidity.config(text=f"{humidity}%")
            self.label_pressure.config(text=f"{pressure} hPa")

            # Determine the weather image to display
            weather_image_file = None
            if "rain" in condition:
                weather_image_file = "heavy-rain.png"
            elif "cloud" in condition:
                weather_image_file = "cloudy.png"
            elif "clear" in condition:
                weather_image_file = "fog.png"
            elif "haze" in condition:
                weather_image_file = "haze.png"

            # Load, resize, and display the weather image
            if weather_image_file:
                try:
                    image_path = os.path.join(self.base_path, weather_image_file)
                    original_image = Image.open(image_path)
                    resized_image = original_image.resize((100, 100), Image.Resampling.LANCZOS)
                    self.weather_image = ImageTk.PhotoImage(resized_image)
                    Label(self.root, image=self.weather_image,bg="#3C3D3D").place(x=490, y=130)
                except Exception as e:
                    messagebox.showerror("Error", f"Weather image not found or cannot be loaded: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = Tk()
    WeatherApp(root)
    root.mainloop()
