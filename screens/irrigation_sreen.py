import tkinter as tk
from tkinter import messagebox, ttk

class IrrigationScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # --- Bottom Navigation ---
        nav_frame = tk.Frame(self, bg="#e8f5e9", height=50)
        nav_frame.pack(side="bottom", fill="x")
        tk.Button(nav_frame, text="🏠 Home", bg="#c8e6c9", command=lambda: controller.show_frame("HomeScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌿 Plant Detection", bg="#c8e6c9", command=lambda: controller.show_frame("PlantScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌤 Weather", bg="#c8e6c9", command=lambda: controller.show_frame("WeatherScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="👤 Profile", bg="#c8e6c9", command=lambda: controller.show_frame("ProfileScreen")).pack(side="left", expand=True, fill="x")

        # Header
        header_frame = tk.Frame(self, bg="#f5f3f0")
        header_frame.pack(pady=(20, 10))
        tk.Label(header_frame, text="Irrigation Schedule", font=("Arial", 22, "bold"), fg="#2c4a3a", bg="#f5f3f0").pack()
        tk.Label(header_frame, text="Monitor and manage your watering plan efficiently.", font=("Arial", 12), fg="#6b7c6f", bg="#f5f3f0").pack()

        # Next Watering Schedule
        tk.Label(header_frame, text="💧 Next Watering", font=("Arial", 16, "bold"), fg="#2c4a3a", bg=header_frame["bg"]).pack(anchor="w")
        tk.Label(header_frame, text="Tomorrow, 6:00 AM", font=("Arial", 13), fg="#6b7c6f", bg=header_frame["bg"]).pack(anchor="w")
        ttk.Separator(header_frame, orient="horizontal").pack(fill="x", pady=8)
        tk.Label(header_frame, text="Reduced Amount (Drought Mode)", font=("Arial", 14, "bold"), fg="#2c4a3a", bg=header_frame["bg"]).pack(anchor="w")
        tk.Label(header_frame, text="3 Liters per plant", font=("Arial", 13), fg="#6b7c6f", bg=header_frame["bg"]).pack(anchor="w", pady=(0,10))
        tk.Label(header_frame, text="Duration: 30 minutes", font=("Arial", 13), fg="#6b7c6f", bg=header_frame["bg"]).pack(anchor="w", pady=(0,10))
        tk.Label(header_frame, text="Soil Moisture: 25% (Low)", font=("Arial", 13), fg="#d32f2f", bg=header_frame["bg"]).pack(anchor="w", pady=(0,10))
        tk.Button(header_frame, text="Set Reminder", bg="#4a7c59", fg="white", font=("Arial", 12, "bold"), height=2, relief="flat").pack(fill="x", padx=15, pady=10)
        ttk.Separator(header_frame, orient="horizontal").pack(fill="x", pady=8)

        # Water Saved this month
        tk.Label(header_frame, text="💧 Water Saved This Month", font=("Arial", 16, "bold"), fg="#2c4a3a", bg=header_frame["bg"]).pack(anchor="w")
        tk.Label(header_frame, text="Goal: 3,200 Liters", font=("Arial", 13), fg="#6b7c6f", bg=header_frame["bg"]).pack(anchor="w", pady=(0,10))
        tk.Label(header_frame, text="Achieved: 2,500 Liters", font=("Arial", 13), fg="#6b7c6f", bg=header_frame["bg"]).pack(anchor="w", pady=(0,10))
        ttk.Separator(header_frame, orient="horizontal").pack(fill="x", pady=8)
        tk.Label(header_frame, text="VS Last Month: +15%", font=("Arial", 13), fg="#2e7d32", bg=header_frame["bg"]).pack(anchor="w", pady=(0,10))
        tk.Label(header_frame, text="Cost Saved: $45.00", font=("Arial", 13), fg="#2e7d32", bg=header_frame["bg"]).pack(anchor="w", pady=(0,10))
        ttk.Separator(header_frame, orient="horizontal").pack(fill="x", pady=8)
        tk.Label(header_frame, text="📅 Upcoming Waterings", font=("Arial", 16, "bold"), fg="#2c4a3a", bg=header_frame["bg"]).pack(anchor="w")

        # Schedule cards
        self._stat_card(header_frame, "Monday", "6:00 AM - 30 mins", "#bbdefb", None, controller).pack(fill="x", pady=2)
        self._stat_card(header_frame, "Thursday", "6:00 AM - 30 mins", "#bbdefb", None, controller).pack(fill="x", pady=2)

        # Water saving tips
        tips_frame = tk.LabelFrame(self, text="💡 Water Saving Tips", bg="#e3f2fd", fg="#2c4a3a", font=("Arial", 12, "bold"))
        tips_frame.pack(fill="x", padx=15, pady=10)

    # 🧱 Define _stat_card properly here
    def _stat_card(self, parent, day, time, color, screen_name, controller):
        card = tk.Frame(parent, bg=color, bd=2, relief="ridge")
        tk.Label(card, text=day, bg=color, font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(5,0))
        tk.Label(card, text=time, bg=color, font=("Arial", 10)).pack(anchor="w", padx=10, pady=(0,5))
        return card
