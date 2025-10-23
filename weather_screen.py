import tkinter as tk
from weather_fetcher import WeatherFetcher
from tkinter import messagebox

class WeatherScreen(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#f5f3f0")
        self.controller = controller
        self.weather_fetcher = WeatherFetcher()

        # Nav bar
        nav_frame = tk.Frame(self, bg="#e8f5e9", height=50)
        nav_frame.pack(side="bottom", fill="x")
        tk.Button(nav_frame, text="🏠 Home", bg="#c8e6c9", command=lambda: controller.show_frame("HomeScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌿 Plant Detection", bg="#c8e6c9", command=lambda: controller.show_frame("PlantScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌤 Weather", bg="#c8e6c9", command=lambda: controller.show_frame("WeatherScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="👤 Profile", command=lambda: controller.show_frame("ProfileScreen")).pack(side="left", expand=True, fill="x")

        # Scroll frame
        self.canvas = tk.Canvas(self, bg="#f9f9f9", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f9f9f9")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_weather()

    def load_weather(self):
        try:
            self.forecast = self.weather_fetcher.get_weather_forecast()
            self.render_forecast()
        except Exception as e:
            messagebox.showerror("Weather Error", str(e))

    def refresh_weather(self):
        self.weather_fetcher.latitude = None
        self.weather_fetcher.longitude = None
        self.load_weather()

    def render_forecast(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tk.Label(self.scrollable_frame, text="Weather Forecast", font=("Arial", 22, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(pady=(15,5))

        today = self.forecast[0]
        self._create_card(self.scrollable_frame, "Current Weather", [
            ("Temperature", f"{today['temp_max']} / {today['temp_min']}"),
            ("Condition", today["condition"]),
            ("Humidity", today["humidity"]),
            ("Wind", today["wind_speed"]),
            ("Rain Chance", today["rain_chance"]),
        ], "#d4c5b0")

        # 7-day
        tk.Label(self.scrollable_frame, text="7-Day Forecast", font=("Arial", 14, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(pady=(15,5))
        for day in self.forecast:
            self._create_forecast_card(self.scrollable_frame, day)

    def _create_card(self, parent, title, data, color):
        card = tk.Frame(parent, bg="white", highlightbackground=color, highlightthickness=2, padx=15, pady=10)
        card.pack(pady=10, fill="x", padx=20)
        tk.Label(card, text=title, font=("Arial", 14, "bold"), fg="#2c4a3a", bg="white").pack(anchor="w", pady=(0,5))
        for label, value in data:
            row = tk.Frame(card, bg="white")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{label}:", font=("Arial", 11, "bold"), fg="#6b7c6f", bg="white").pack(side="left")
            tk.Label(row, text=value, font=("Arial", 11), fg="#2c4a3a", bg="white").pack(side="right")

    def _create_forecast_card(self, parent, day):
        frame = tk.Frame(parent, bg="white", highlightbackground="#d4c5b0", highlightthickness=2, padx=10, pady=8)
        frame.pack(fill="x", padx=20, pady=4)
        tk.Label(frame, text=day["day"], font=("Arial", 11, "bold"), fg="#2c4a3a", bg="white").pack(side="left")
        tk.Label(frame, text=f"{day['temp_max']} / {day['temp_min']}", font=("Arial", 11), fg="#2c4a3a", bg="white").pack(side="left", padx=(15,0))
        tk.Label(frame, text=day["condition"], font=("Arial", 10), fg="#6b7c6f", bg="white").pack(side="left", padx=10)
        tk.Label(frame, text=f"{day['rain_chance']} ({day['rain_mm']} mm)", font=("Arial", 10), fg="#4a7c59", bg="white").pack(side="right")