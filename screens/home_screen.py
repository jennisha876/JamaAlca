import tkinter as tk
from tkinter import messagebox

from utils.scrollable_frame import ScrollableFrame

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f9f9")

        scrollable = ScrollableFrame(self, bg="#f9f9f9")
        scrollable.pack(fill="both", expand=True)
        scrollable_frame = scrollable.get_frame()

        header_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        header_frame.pack(fill="x", pady=(10, 5), padx=10)

        tk.Label(header_frame, text="Welcome back, Farmer!",
                font=("Arial", 18, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(anchor="w")

        tk.Label(header_frame, text="Here's your farm overview for today.",
                font=("Arial", 11), fg="#6b7c6f", bg="#f9f9f9").pack(anchor="w")

        alert_btn = tk.Button(
            header_frame,
            text="🔔",
            font=("Arial", 16),
            bg="#f9f9f9",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=controller.open_notification_center
        )
        alert_btn.pack(side="right")

        # --- Dynamic Alerts Section ---
        from services.data_service import DataService
        data_service = DataService()
        # Drought alert: show only if next watering is 'Skip - Rain expected' or weather summary indicates drought
        next_watering = data_service.get_next_watering()
        weather_summary = data_service.get_weather_summary()
        if next_watering == "Skip - Rain expected" or "drought" in weather_summary.lower():
            drought_frame = tk.Frame(scrollable_frame, bg="#fff3e0",
                                    highlightbackground="#ffcc80", highlightthickness=2)
            drought_frame.pack(fill="x", padx=10, pady=5)
            tk.Label(drought_frame, text="⚠ Drought Warning!",
                    font=("Arial", 12, "bold"), fg="#e65100", bg="#fff3e0").pack(anchor="w", padx=10)
            tk.Label(drought_frame,
                    text="Low rainfall expected this week. Conserve water and schedule irrigation wisely.",
                    font=("Arial", 10), fg="#bf360c", bg="#fff3e0",
                    wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))

        # Disease alert: show only if crop health status is 'Needs attention' or last scan was 'Disease Detected'
        crop_health = data_service.get_crop_health_status()
        recent_scans = data_service.get_recent_scans(1)
        show_disease_alert = False
        if crop_health == "Needs attention":
            show_disease_alert = True
        elif recent_scans and recent_scans[0]["status"] == "Disease Detected":
            show_disease_alert = True
        if show_disease_alert:
            disease_frame = tk.Frame(scrollable_frame, bg="#ffebee",
                                    highlightbackground="#ef9a9a", highlightthickness=2)
            disease_frame.pack(fill="x", padx=10, pady=5)
            tk.Label(disease_frame, text="⚠ Disease Alert!",
                    font=("Arial", 12, "bold"), fg="#c62828", bg="#ffebee").pack(anchor="w", padx=10)
            tk.Label(disease_frame,
                    text="Recent scan or crop health indicates possible disease. Check affected crops.",
                    font=("Arial", 10), fg="#b71c1c", bg="#ffebee",
                    wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))

        # Quick Stats
        stats_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        stats_frame.pack(fill="x", padx=10, pady=(10,0))

        row1 = tk.Frame(stats_frame, bg="#f9f9f9")
        row1.pack(fill="x", pady=2)
        self._stat_card(row1, "🌿 Crop Health", "Good condition", "#a5d6a7", "PlantScreen", controller).pack(side="left", expand=True, fill="x", padx=5)
        self._stat_card(row1, "🌤 Weather", "28°C, Sunny", "#90caf9", "WeatherScreen", controller).pack(side="left", expand=True, fill="x", padx=5)

        row2 = tk.Frame(stats_frame, bg="#f9f9f9")
        row2.pack(fill="x", pady=2)
        self._stat_card(row2, "💧 Next Watering", "Tomorrow", "#b3e5fc", "IrrigationScreen", controller).pack(side="left", expand=True, fill="x", padx=5)
        self._stat_card(row2, "💰 Market Price", "Corn: ↑ 12%", "#fff59d", None, controller).pack(side="left", expand=True, fill="x", padx=5)

        # Sustainability Impact
        impact_frame = tk.LabelFrame(scrollable_frame, text="🌱 Sustainability Impact",
                                    bg="#f1f8e9", fg="#2c4a3a", font=("Arial", 12, "bold"))
        impact_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(impact_frame, text="💧 Water Saved: 2,500 L", font=("Arial", 11),
                bg="#f1f8e9", fg="#1565c0").pack(anchor="w", padx=10)
        tk.Label(impact_frame, text="📈 Yield Increase: +12%", font=("Arial", 11),
                bg="#f1f8e9", fg="#2e7d32").pack(anchor="w", padx=10)
        tk.Label(impact_frame, text="🍃 Chemicals Reduced: -8%", font=("Arial", 11),
                bg="#f1f8e9", fg="#00695c").pack(anchor="w", padx=10)

        # Quick Tip
        tip_frame = tk.LabelFrame(scrollable_frame, text="💡 Today's Tip",
                                bg="#fffde7", fg="#2c4a3a", font=("Arial", 12, "bold"))
        tip_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(tip_frame,
                text="Mulch your soil to retain moisture and reduce water usage during dry seasons.",
                font=("Arial", 10), fg="#6b7c6f", bg="#fffde7",
                wraplength=450, justify="left").pack(anchor="w", padx=10, pady=5)

        # Community
        community_frame = tk.LabelFrame(scrollable_frame, text="👩🏾‍🌾 Join the Community",
                                        bg="#f3e5f5", fg="#2c4a3a", font=("Arial", 12, "bold"))
        community_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(community_frame,
                text="Connect with other farmers, share insights, and discuss challenges.",
                font=("Arial", 10), fg="#6b7c6f", bg="#f3e5f5",
                wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(5,0))
        tk.Button(community_frame, text="Browse Discussions →",
                fg="#4a7c59", bg="#f3e5f5", font=("Arial", 10, "bold"),
                relief="flat", cursor="hand2",
                command=lambda: controller.show_frame("CommunityScreen")).pack(anchor="w", padx=10, pady=(0,5))

        nav_frame = tk.Frame(self, bg="#e8f5e9", height=50)
        nav_frame.pack(side="bottom", fill="x")

        tk.Button(nav_frame, text="🏠 Home", bg="#c8e6c9",
            command=lambda: controller.show_frame("HomeScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌿 Plant Detection",
            command=lambda: controller.show_frame("PlantScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌤 Weather",
            command=lambda: controller.show_frame("WeatherScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="👤 Profile",
            command=lambda: controller.show_frame("ProfileScreen")).pack(side="left", expand=True, fill="x")

    def _stat_card(self, parent, title, subtitle, color, screen_name, controller):
        frame = tk.Frame(parent, bg=color, bd=2, relief="ridge", cursor="hand2")
        tk.Label(frame, text=title, font=("Arial", 11, "bold"),
                fg="#2c4a3a", bg=color).pack(anchor="w", padx=10, pady=(5,0))
        tk.Label(frame, text=subtitle, font=("Arial", 10),
                fg="#4e5d52", bg=color).pack(anchor="w", padx=10, pady=(0,5))
        if screen_name:
            frame.bind("<Button-1>", lambda e: controller.show_frame(screen_name))
        return frame