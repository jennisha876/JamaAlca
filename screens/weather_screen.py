import tkinter as tk

class WeatherScreen(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#f5f3f0")
        self.controller = controller

        # --- Bottom Navigation ---
        nav_frame = tk.Frame(self, bg="#e8f5e9", height=50)
        nav_frame.pack(side="bottom", fill="x")
        tk.Button(nav_frame, text="🏠 Home", bg="#c8e6c9",
                  command=lambda: controller.show_frame("HomeScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌿 Plant Detection", bg="#c8e6c9",
                  command=lambda: controller.show_frame("PlantScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌤 Weather", bg="#c8e6c9",
                  command=lambda: controller.show_frame("WeatherScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="👤 Profile", bg="#c8e6c9",
                  command=lambda: controller.show_frame("ProfileScreen")).pack(side="left", expand=True, fill="x")

        # --- Scrollable Canvas ---
        canvas = tk.Canvas(self, bg="#f9f9f9", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # --- Dummy weather data ---
        self.forecast = [
            {"day": "Today", "temp": 28, "condition": "Sunny", "rain": 10},
            {"day": "Tomorrow", "temp": 26, "condition": "Partly Cloudy", "rain": 30},
            {"day": "Wednesday", "temp": 24, "condition": "Rainy", "rain": 80},
            {"day": "Thursday", "temp": 25, "condition": "Cloudy", "rain": 40},
            {"day": "Friday", "temp": 27, "condition": "Sunny", "rain": 5},
            {"day": "Saturday", "temp": 29, "condition": "Sunny", "rain": 5},
            {"day": "Sunday", "temp": 28, "condition": "Partly Cloudy", "rain": 20},
        ]

        total_rain = sum(day["rain"] for day in self.forecast)
        self.is_drought = total_rain < 100

        # --- Header ---
        tk.Label(scrollable_frame, text="Weather Forecast", font=("Arial", 22, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(pady=(15, 5))
        tk.Label(scrollable_frame, text="7-Day Forecast and Farming Recommendations",
                 font=("Arial", 12), fg="#6b7c6f", bg="#f9f9f9").pack(pady=(0, 10))

        # --- Current Weather Section ---
        self._create_card(scrollable_frame,
            title="Current Weather",
            data=[
                ("Temperature", "28°C"),
                ("Condition", "Sunny"),
                ("Humidity", "65%"),
                ("Wind", "12 km/h"),
                ("Rain Chance", "10%"),
            ],
            color="#d4c5b0"
        )

        # --- Drought Alert (if needed) ---
        if self.is_drought:
            self._create_alert(scrollable_frame,
                "⚠ Drought Warning",
                "Low rainfall is expected this week. Conserve water and monitor crops closely.",
                bg="#ffe6e6",
                border="#ffcccc",
                fg="#cc0000"
            )

        # --- Heavy Rain Alert ---
        self._create_alert(scrollable_frame,
            "⚠ Heavy Rain Alert",
            "Periods of heavy rainfall may occur mid-week. Secure loose soil and drainage areas.",
            bg="#fff2cc",
            border="#ffdd99",
            fg="#cc6600"
        )

        # --- 7-Day Forecast ---
        tk.Label(scrollable_frame, text="7-Day Forecast", font=("Arial", 14, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(pady=(15, 5))
        forecast_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        forecast_frame.pack(pady=5)
        for day in self.forecast:
            self._create_forecast_card(forecast_frame, day)

        # --- Recommendations ---
        self._create_recommendations(scrollable_frame)

    # -----------------------
    # Helper: Info Card
    # -----------------------
    def _create_card(self, parent, title, data, color):
        card = tk.Frame(parent, bg="white", highlightbackground=color, highlightthickness=2, padx=15, pady=10)
        card.pack(pady=10, fill="x", padx=20)
        tk.Label(card, text=title, font=("Arial", 14, "bold"), fg="#2c4a3a", bg="white").pack(anchor="w", pady=(0, 5))
        for label, value in data:
            row = tk.Frame(card, bg="white")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{label}:", font=("Arial", 11, "bold"), fg="#6b7c6f", bg="white").pack(side="left")
            tk.Label(row, text=value, font=("Arial", 11), fg="#2c4a3a", bg="white").pack(side="right")

    # -----------------------
    # Helper: Alert Card
    # -----------------------
    def _create_alert(self, parent, title, message, bg, border, fg):
        alert = tk.Frame(parent, bg=bg, highlightbackground=border, highlightthickness=2, padx=15, pady=10)
        alert.pack(pady=8, fill="x", padx=20)
        tk.Label(alert, text=title, font=("Arial", 13, "bold"), fg=fg, bg=bg).pack(anchor="w")
        tk.Label(alert, text=message, font=("Arial", 11), fg=fg, bg=bg, wraplength=400, justify="left").pack(anchor="w", pady=(3, 0))

    # -----------------------
    # Helper: Forecast Row
    # -----------------------
    def _create_forecast_card(self, parent, day):
        frame = tk.Frame(parent, bg="white", highlightbackground="#d4c5b0", highlightthickness=2, padx=10, pady=8)
        frame.pack(fill="x", padx=20, pady=4)
        tk.Label(frame, text=day["day"], font=("Arial", 11, "bold"), fg="#2c4a3a", bg="white").pack(side="left")
        tk.Label(frame, text=f"{day['temp']}°C", font=("Arial", 11), fg="#2c4a3a", bg="white").pack(side="left", padx=(15, 0))
        tk.Label(frame, text=day["condition"], font=("Arial", 10), fg="#6b7c6f", bg="white").pack(side="left", padx=10)
        tk.Label(frame, text=f"{day['rain']}% Rain", font=("Arial", 10), fg="#4a7c59", bg="white").pack(side="right")

    # -----------------------
    # Helper: Recommendations
    # -----------------------
    def _create_recommendations(self, parent):
        bg = "#fff7e6" if self.is_drought else "#eaffea"
        border = "#ffdd99" if self.is_drought else "#c5e1a5"
        card = tk.Frame(parent, bg=bg, highlightbackground=border, highlightthickness=2, padx=15, pady=10)
        card.pack(pady=15, fill="x", padx=20)

        tk.Label(card, text="Farming Recommendations", font=("Arial", 14, "bold"), fg="#2c4a3a", bg=bg).pack(anchor="w", pady=(0, 5))

        recommendations = []
        if self.is_drought:
            recommendations = [
                ("⚠", "Conserve water wherever possible."),
                ("⚠", "Reduce watering frequency to essential levels."),
                ("✓", "Apply mulch to retain soil moisture."),
            ]
        else:
            recommendations = [
                ("✓", "Maintain proper irrigation."),
                ("✓", "Apply fertilizers as scheduled."),
                ("⚠", "Delay new planting during rainfall."),
            ]

        for icon, text in recommendations:
            row = tk.Frame(card, bg=bg)
            row.pack(anchor="w", pady=2)
            tk.Label(row, text=icon, font=("Arial", 11, "bold"), fg="#2c4a3a", bg=bg, width=2).pack(side="left")
            tk.Label(row, text=text, font=("Arial", 11), fg="#2c4a3a", bg=bg, wraplength=400, justify="left").pack(side="left")