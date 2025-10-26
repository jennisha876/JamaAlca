import tkinter as tk
from tkinter import messagebox
from services.data_service import DataService

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f9f9")
        self.data_service = DataService()

        main_frame = tk.Frame(self, bg="#f9f9f9")
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame, bg="#f9f9f9", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout for scroll area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Make mouse wheel scroll the canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        header_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        header_frame.pack(fill="x", pady=(10, 5), padx=10)

        tk.Label(header_frame, text="Welcome back, Farmer!",
                font=("Arial", 18, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(anchor="w")

        tk.Label(header_frame, text="Here's your farm overview for today.",
                font=("Arial", 11), fg="#6b7c6f", bg="#f9f9f9").pack(anchor="w")

        # Create notification button with badge
        self.notification_btn = self._create_notification_button(header_frame, controller)
        self.notification_btn.pack(side="right")
        
        # Set up the notification badge callback
        controller.notif_manager.badge_callback = self.update_notification_badge
        
        # Update the badge immediately when the screen loads
        self.update_notification_badge(controller.notif_manager.unread_count())
        
        # Store reference to controller for badge updates
        self.controller = controller

        # Drought Warning Banner
        drought_frame = tk.Frame(scrollable_frame, bg="#fff3e0",
                                highlightbackground="#ffcc80", highlightthickness=2)
        drought_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(drought_frame, text="⚠ Drought Warning!",
                font=("Arial", 12, "bold"), fg="#e65100", bg="#fff3e0").pack(anchor="w", padx=10)
        tk.Label(drought_frame,
                text="Low rainfall expected this week. Conserve water and schedule irrigation wisely.",
                font=("Arial", 10), fg="#bf360c", bg="#fff3e0",
                wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))

        # Disease Alert Banner
        disease_frame = tk.Frame(scrollable_frame, bg="#ffebee",
                                highlightbackground="#ef9a9a", highlightthickness=2)
        disease_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(disease_frame, text="⚠ Disease Alert!",
                font=("Arial", 12, "bold"), fg="#c62828", bg="#ffebee").pack(anchor="w", padx=10)
        tk.Label(disease_frame,
                text="Possible leaf spot detected in your region. Check affected crops.",
                font=("Arial", 10), fg="#b71c1c", bg="#ffebee",
                wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))

        # Quick Stats
        stats_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        stats_frame.pack(fill="x", padx=10, pady=(10,0))

        row1 = tk.Frame(stats_frame, bg="#f9f9f9")
        row1.pack(fill="x", pady=2)
        self._stat_card(row1, "🌿 Crop Health", self.data_service.get_crop_health_status(), "#a5d6a7", "PlantScreen", controller).pack(side="left", expand=True, fill="x", padx=5)
        self._stat_card(row1, "🌤 Weather", self.data_service.get_weather_summary(), "#90caf9", "WeatherScreen", controller).pack(side="left", expand=True, fill="x", padx=5)

        row2 = tk.Frame(stats_frame, bg="#f9f9f9")
        row2.pack(fill="x", pady=2)
        self._stat_card(row2, "💧 Next Watering", self.data_service.get_next_watering(), "#b3e5fc", "IrrigationScreen", controller).pack(side="left", expand=True, fill="x", padx=5)
        self._stat_card(row2, "💰 Market Price", self.data_service.get_market_price(), "#fff59d", None, controller).pack(side="left", expand=True, fill="x", padx=5)

        # Sustainability Impact
        impact_frame = tk.LabelFrame(scrollable_frame, text="🌱 Sustainability Impact",
                                    bg="#f1f8e9", fg="#2c4a3a", font=("Arial", 12, "bold"))
        impact_frame.pack(fill="x", padx=10, pady=10)
        
        sustainability_metrics = self.data_service.get_sustainability_metrics()
        tk.Label(impact_frame, text=f"💧 Water Saved: {sustainability_metrics['water_saved']}", font=("Arial", 11),
                bg="#f1f8e9", fg="#1565c0").pack(anchor="w", padx=10)
        tk.Label(impact_frame, text=f"📈 Yield Increase: {sustainability_metrics['yield_increase']}", font=("Arial", 11),
                bg="#f1f8e9", fg="#2e7d32").pack(anchor="w", padx=10)
        tk.Label(impact_frame, text=f"🍃 Chemicals Reduced: {sustainability_metrics['chemicals_reduced']}", font=("Arial", 11),
                bg="#f1f8e9", fg="#00695c").pack(anchor="w", padx=10)

        # Quick Tip
        tip_frame = tk.LabelFrame(scrollable_frame, text="💡 Today's Tip",
                                bg="#fffde7", fg="#2c4a3a", font=("Arial", 12, "bold"))
        tip_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(tip_frame,
                text=self.data_service.get_todays_tip(),
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

    def _create_notification_button(self, parent, controller):
        """
        Create a notification button with a badge showing unread count
        This creates a bell icon with a red badge that shows how many unread notifications there are
        """
        # Create a frame to hold the bell icon and badge
        btn_frame = tk.Frame(parent, bg="#f9f9f9", bd=0, relief="flat")
        
        # Create the bell button
        bell_btn = tk.Button(
            btn_frame,
            text="🔔",
            font=("Arial", 16),
            bg="#f9f9f9",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=controller.open_notification_center
        )
        bell_btn.pack()
        
        # Create the badge (initially hidden)
        self.badge_label = tk.Label(
            btn_frame,
            text="",
            font=("Arial", 8, "bold"),
            bg="#ff4444",
            fg="white",
            bd=0,
            relief="flat"
        )
        # Position the badge in the top-right corner of the bell
        self.badge_label.place(relx=0.7, rely=0.1, anchor="center")
        
        # Store reference to the button for updates
        self.bell_btn = bell_btn
        
        return btn_frame

    def update_notification_badge(self, unread_count):
        """
        Update the notification badge to show the number of unread notifications
        This is called whenever new notifications arrive or are read
        """
        if unread_count > 0:
            # Show the badge with the count
            self.badge_label.config(text=str(unread_count))
            self.badge_label.place(relx=0.7, rely=0.1, anchor="center")
        else:
            # Hide the badge if no unread notifications
            self.badge_label.place_forget()

    def refresh_notification_badge(self):
        """
        Refresh the notification badge when the screen is shown
        This ensures the badge is always up-to-date when the user returns to the home screen
        """
        if hasattr(self, 'controller') and self.controller:
            self.update_notification_badge(self.controller.notif_manager.unread_count())