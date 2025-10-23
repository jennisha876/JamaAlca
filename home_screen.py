import tkinter as tk
from tkinter import ttk


class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f9f9")

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

        tk.Label(header_frame, text="Here’s your farm overview for today.",
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

        # Unread badge
        self._notif_badge = tk.Label(header_frame, text="", bg="#f44336", fg="white", font=("Arial", 9, "bold"))
        self._notif_badge.place_forget()

        def _update_badge(count):
            if count and count > 0:
                self._notif_badge.config(text=str(count))
                alert_btn.pack(side="right")
                self._notif_badge.place(in_=alert_btn, relx=1.0, x=-6, rely=0.0, y=0)
            else:
                self._notif_badge.config(text="")
                self._notif_badge.place_forget()

        try:
            controller.register_badge_callback(_update_badge)
        except Exception:
            pass

        alert_btn.pack(side="right")

        # Drought Warning Banner (placeholder)
        drought_frame = tk.Frame(scrollable_frame, bg="#fff3e0",
                                highlightbackground="#ffcc80", highlightthickness=2)
        drought_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(drought_frame, text="⚠ Drought Warning!",
                font=("Arial", 12, "bold"), fg="#e65100", bg="#fff3e0").pack(anchor="w", padx=10)
        tk.Label(drought_frame,
                text="Low rainfall expected this week. Conserve water and schedule irrigation wisely.",
                font=("Arial", 10), fg="#bf360c", bg="#fff3e0",
                wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))

        # Alerts area (computed)
        self.alerts_container = tk.Frame(scrollable_frame, bg="#f9f9f9")
        self.alerts_container.pack(fill="x", padx=10, pady=5)

        # Determine drought from weather screen if available
        drought_warning = False
        drought_message = ""
        try:
            weather_frame = controller.frames.get("WeatherScreen")
            forecast = getattr(weather_frame, "forecast", None)
            if forecast and len(forecast) >= 3:
                # simple heuristic: low total precipitation next 3 days
                total_rain = 0
                for day in forecast[:3]:
                    # try keys used by WeatherFetcher
                    rain = 0
                    if isinstance(day.get("rain_mm"), str):
                        try:
                            rain = float(str(day.get("rain_mm").replace(" mm", "")))
                        except Exception:
                            rain = 0
                    else:
                        rain = float(day.get("rain_mm", 0)) if day.get("rain_mm") is not None else 0
                    total_rain += rain
                if total_rain < 5:  # mm threshold
                    drought_warning = True
                    drought_message = "Low rainfall expected soon. Consider conserving water and scheduling irrigation."
        except Exception:
            pass

        if drought_warning:
            dframe = tk.Frame(self.alerts_container, bg="#fff3e0", highlightbackground="#ffcc80", highlightthickness=2)
            dframe.pack(fill="x", pady=(0, 5))
            tk.Label(dframe, text="⚠ Drought Warning!", font=("Arial", 12, "bold"), fg="#e65100", bg="#fff3e0").pack(anchor="w", padx=10)
            tk.Label(dframe, text=drought_message, font=("Arial", 10), fg="#bf360c", bg="#fff3e0", wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))

        # Disease alert: if recent scans show disease within last N scans
        disease_found = False
        disease_msg = ""
        try:
            recent = getattr(controller, "recent_scans", [])
            for scan in recent[-3:]:
                if scan.get("disease") and scan.get("disease") != "Healthy":
                    disease_found = True
                    disease_msg = f"Recent scan detected {scan.get('disease')} for {scan.get('crop')}. Inspect affected fields."
                    break
        except Exception:
            recent = []

        if disease_found:
            af = tk.Frame(self.alerts_container, bg="#fff8e1", highlightbackground="#ffe082", highlightthickness=2)
            af.pack(fill="x", pady=(0, 5))
            tk.Label(af, text="⚠ Disease Alert", font=("Arial", 12, "bold"), fg="#bf360c", bg="#fff8e1").pack(anchor="w", padx=10)
            tk.Label(af, text=disease_msg, font=("Arial", 10), fg="#bf360c", bg="#fff8e1", wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))
        # Quick Stats area (simplified)
        stats_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        stats_frame.pack(fill="x", padx=10, pady=(10,0))

        def _stat_card(parent, title, value, color, command=None):
            card = tk.Frame(parent, bg=color, bd=2, relief="ridge", padx=8, pady=6)
            tk.Label(card, text=title, bg=color, font=("Arial", 11, "bold")).pack(anchor="w")
            value_lbl = tk.Label(card, text=value, bg=color, font=("Arial", 10))
            value_lbl.pack(anchor="w", pady=(4,0))
            if command:
                tk.Button(card, text="Open", command=command, bg=color, relief="flat").pack(anchor="e", pady=(6,0))
            return card, value_lbl

        row1 = tk.Frame(stats_frame, bg="#f9f9f9")
        row1.pack(fill="x", pady=2)

        # Crop Health summary (simple heuristic based on recent scans)
        crop_health = "No data"
        try:
            recent = getattr(controller, "recent_scans", [])
            if not recent:
                crop_health = "No scans"
            else:
                # if any recent diseased -> Unhealthy, else Good
                any_disease = any(s.get("disease") and s.get("disease") != "Healthy" for s in recent[-5:])
                crop_health = "Unhealthy" if any_disease else "Good"
        except Exception:
            crop_health = "Unknown"

        card, self.crop_health_val = _stat_card(row1, "🌿 Crop Health", crop_health, "#a5d6a7", command=lambda: controller.show_frame("PlantScreen"))
        card.pack(side="left", expand=True, fill="x", padx=5)

        # Weather summary from WeatherScreen if available
        weather_summary = "No data"
        try:
            w = controller.frames.get("WeatherScreen")
            if getattr(w, "forecast", None):
                today = w.forecast[0]
                weather_summary = f"{today.get('condition', '')} {today.get('temp_max','') }"
        except Exception:
            weather_summary = "Unknown"

        card, self.weather_val = _stat_card(row1, "🌤 Weather", weather_summary, "#90caf9", command=lambda: controller.show_frame("WeatherScreen"))
        card.pack(side="left", expand=True, fill="x", padx=5)

        # Market price tile (placeholder; can be wired later)
        market_price = "--"
        card, self.market_val = _stat_card(row1, "💲 Market Price", market_price, "#ffe082", command=None)
        card.pack(side="left", expand=True, fill="x", padx=5)

        # Secondary row: irrigation + today's tips
        row2 = tk.Frame(stats_frame, bg="#f9f9f9")
        row2.pack(fill="x", pady=6)

        # Irrigation status: based on drought heuristic
        irrigation = "Normal"
        if drought_warning:
            irrigation = "Conserve"
        card, self.irrigation_val = _stat_card(row2, "💧 Irrigation", irrigation, "#b2dfdb", command=None)
        card.pack(side="left", expand=True, fill="x", padx=5)

        # Today's tips: heuristic based on weather
        tips = "No tips available"
        try:
            if drought_warning:
                tips = "Reduce watering; mulch to conserve soil moisture."
            elif weather_summary and "Rain" in weather_summary:
                tips = "Delay new planting; check drainage."
            else:
                tips = "Monitor for pests after warm, humid days."
        except Exception:
            tips = "General: monitor crops daily."

        card, self.tips_val = _stat_card(row2, "📋 Today's Tips", tips, "#fff9c4", command=None)
        card.pack(side="left", expand=True, fill="x", padx=5)
        # Alerts quick tile (shows unread count)
        card, self.alerts_val = _stat_card(row2, "🚨 Alerts", "0", "#ffccbc", command=controller.open_notification_center)
        card.pack(side="left", expand=True, fill="x", padx=5)

        # --- Recent Scans section ---
        self.recent_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        self.recent_frame.pack(fill="x", padx=15, pady=(10, 20))
        # placeholder lambdas replaced by actual updaters below
        self._update_tiles = lambda: None
        self._update_recent_scans = lambda: None
        self._update_alerts_area = lambda: None
        # initialize update functions
        self._update_tiles = lambda: self._internal_update_tiles(controller)
        self._update_recent_scans = lambda: self._internal_update_recent(controller)
        self._update_alerts_area = lambda: self._internal_update_alerts(controller)
        # initial population
        self._update_alerts_area()
        self._update_tiles()
        self._update_recent_scans()

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

        # Bottom nav kept minimal; navigation handled by controller
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
        
        # register refresh callback so this screen updates when scans/weather change
        try:
            controller.register_refresh_callback(self.refresh)
        except Exception:
            pass
    
    def refresh(self):
        """Re-render dynamic parts of the Home screen: alerts, tiles, and recent scans."""
        try:
            self._update_alerts_area()
        except Exception:
            pass
        try:
            self._update_tiles()
        except Exception:
            pass
        try:
            self._update_recent_scans()
        except Exception:
            pass

    # --- internal helper implementations ---
    def _internal_update_tiles(self, controller):
        # update crop health based on recent scans
        try:
            recent = getattr(controller, "recent_scans", []) or []
            if not recent:
                crop_health = "No scans"
            else:
                any_disease = any(s.get("disease") and s.get("disease") != "Healthy" for s in recent[-5:])
                crop_health = "Unhealthy" if any_disease else "Good"
            self.crop_health_val.config(text=crop_health)
        except Exception:
            pass

        # weather
        try:
            w = controller.frames.get("WeatherScreen")
            weather_summary = "No data"
            if getattr(w, "forecast", None):
                today = w.forecast[0]
                weather_summary = f"{today.get('condition', '')} {today.get('temp_max','') }"
            self.weather_val.config(text=weather_summary)
        except Exception:
            pass

        # update unread alerts badge number on the alerts tile
        try:
            count = 0
            try:
                count = controller.notif_manager.unread_count()
            except Exception:
                count = 0
            self.alerts_val.config(text=str(count))
        except Exception:
            pass

    def _internal_update_recent(self, controller):
        # rebuild recent scans area simply (small number of items)
        for w in self.recent_frame.winfo_children():
            w.destroy()
        recent = getattr(controller, "recent_scans", []) or []
        if not recent:
            tk.Label(self.recent_frame, text="No scans yet.", fg="#6b7c6f", bg="#f9f9f9").pack(anchor="w", padx=10, pady=5)
            return
        for scan in reversed(recent[-5:]):
            self._add_recent_scan(scan.get("crop", "Unknown"), scan.get("disease", "Unknown"), scan.get("created_at", ""))

    def _internal_update_alerts(self, controller):
        # rebuild the alerts area with recent important alerts (drought/disease)
        for w in self.alerts_container.winfo_children():
            w.destroy()
        # drought
        try:
            weather_frame = controller.frames.get("WeatherScreen")
            forecast = getattr(weather_frame, "forecast", None)
            drought_warning = False
            drought_message = ""
            if forecast and len(forecast) >= 3:
                total_rain = 0
                for day in forecast[:3]:
                    rain = 0
                    if isinstance(day.get("rain_mm"), str):
                        try:
                            rain = float(str(day.get("rain_mm").replace(" mm", "")))
                        except Exception:
                            rain = 0
                    else:
                        rain = float(day.get("rain_mm", 0)) if day.get("rain_mm") is not None else 0
                    total_rain += rain
                if total_rain < 5:
                    drought_warning = True
                    drought_message = "Low rainfall expected soon. Consider conserving water and scheduling irrigation."
            if drought_warning:
                dframe = tk.Frame(self.alerts_container, bg="#fff3e0", highlightbackground="#ffcc80", highlightthickness=2)
                dframe.pack(fill="x", pady=(0, 5))
                tk.Label(dframe, text="⚠ Drought Warning!", font=("Arial", 12, "bold"), fg="#e65100", bg="#fff3e0").pack(anchor="w", padx=10)
                tk.Label(dframe, text=drought_message, font=("Arial", 10), fg="#bf360c", bg="#fff3e0", wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))
        except Exception:
            pass

        # disease alerts from recent scans
        try:
            recent = getattr(controller, "recent_scans", []) or []
            for scan in recent[-3:]:
                if scan.get("disease") and scan.get("disease") != "Healthy":
                    af = tk.Frame(self.alerts_container, bg="#fff8e1", highlightbackground="#ffe082", highlightthickness=2)
                    af.pack(fill="x", pady=(0, 5))
                    tk.Label(af, text="⚠ Disease Alert", font=("Arial", 12, "bold"), fg="#bf360c", bg="#fff8e1").pack(anchor="w", padx=10)
                    tk.Label(af, text=f"Recent scan detected {scan.get('disease')} for {scan.get('crop')}. Inspect affected fields.",
                             font=("Arial", 10), fg="#bf360c", bg="#fff8e1", wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))
                    break
        except Exception:
            pass
