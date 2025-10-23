import tkinter as tk
from tkinter import ttk
import threading, time, random
from datetime import datetime
import os


#Notification Class
class Notification:
    def __init__(self, title, message, category="General", severity=None, extra=None):
        self.title = title
        self.message = message
        self.category = category
        self.severity = severity or "normal"
        self.extra = extra or {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.read = False


#Notification Manager
class NotificationManager:
    """Handles posting, storing, and displaying toast notifications."""
    def __init__(self, root, badge_callback=None):
        self.root = root
        self.notifications = []
        self.running = True
        self.badge_callback = badge_callback
        # Start demo generator only when enabled. Set NOTIF_DEMO=0 to disable in tests.
        try:
            demo_enabled = os.environ.get("NOTIF_DEMO", "1") != "0"
        except Exception:
            demo_enabled = True
        if demo_enabled:
            threading.Thread(target=self._auto_generate_demo, daemon=True).start()

    def post(self, title, message, category="General", severity=None, extra=None):
        notif = Notification(title, message, category, severity=severity, extra=extra)
        self.notifications.append(notif)
        # Ensure UI work happens on the main Tk thread.
        try:
            # schedule toast creation on main loop
            self.root.after(0, lambda n=notif: self._show_toast(n))
            # schedule badge update on main loop
            self.root.after(0, self._update_badge)
        except Exception:
            # fallback (if root is not available) — call directly
            try:
                self._show_toast(notif)
            except Exception:
                pass
            try:
                self._update_badge()
            except Exception:
                pass

    #Popup toast notification
    def _show_toast(self, notif):
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        toast.configure(bg="#333")

        toast.update_idletasks()
        w, h = 280, 110
        x = toast.winfo_screenwidth() - w - 40
        y = toast.winfo_screenheight() - h - 60
        toast.geometry(f"{w}x{h}+{x}+{y}")
        # Visual hint for severity
        sev_color = "#2e7d32" if notif.severity == "normal" else ("#ffa000" if notif.severity == "warning" else "#d32f2f")
        header = tk.Frame(toast, bg=sev_color)
        header.pack(fill="x")
        tk.Label(header, text=notif.title, font=("Segoe UI", 10, "bold"), fg="white", bg=sev_color).pack(pady=(6, 3), padx=6, anchor="w")
        tk.Label(toast, text=notif.message, fg="#ddd", bg="#333", wraplength=250, justify="left").pack(pady=(0, 5), padx=6)

        toast.after(4500, toast.destroy)

    #Demo farm notifications
    def _auto_generate_demo(self):
        examples = [
            ("☀️ Drought Warning", "Extended dry period expected. Monitor soil moisture closely.", "Weather"),
            ("🌧️ Extreme Rain Alert", "Heavy rainfall predicted tonight. Consider drainage checks.", "Weather"),
            ("🌩️ Monsoon Update", "Monsoon winds intensifying in northern regions.", "Weather"),
            ("💨 Wind Advisory", "High wind speeds detected, secure young seedlings.", "Weather"),

            ("💧 Next Watering", "Time to water your tomato crops.", "Watering"),
            ("🍇 Grape Irrigation Reminder", "Set irrigation timer for grape vines within 2 hours.", "Watering"),
            ("🌾 Morning Watering Tip", "Water early morning to reduce evaporation loss.", "Watering"),

            ("🍃 Leaf Spot Alert", "Possible leaf spot detected in nearby corn fields.", "Disease"),
            ("🌻 Wilt Disease Warning", "Early signs of fusarium wilt in regional crops.", "Disease"),
            ("🪱 Pest Risk", "Aphid concentration rising — inspect tomato plants.", "Disease"),
            ("🧬 Crop Health Update", "Your crops’ NDVI health index dropped 5%.", "Crop Health"),

            ("🌱 Water Usage", "You’ve saved 18L of water this week! Great job.", "Sustainability"),
            ("🚰 Drought Planning", "You have enough water for the next 3 days.", "Sustainability"),
            ("♻️ Eco Tip", "Use organic compost to boost soil carbon storage.", "Sustainability"),

            ("📈 Market Price Update", "Tomato prices up 6% in local markets.", "Market"),
            ("📉 Market Alert", "Rice prices dropped 4% — consider storage options.", "Market"),
            ("💰 Demand Surge", "High demand for organic lettuce this week.", "Market"),
        ]

        weights = {
            "Weather": 3,
            "Watering": 3,
            "Disease": 2,
            "Crop Health": 2,
            "Sustainability": 1,
            "Market": 1,
        }

        # Rate-limit demo notifications so they don't spam the user.
        # Only post new notifications when unread_count is below a small threshold
        # and avoid posting too-frequently (roughly ~60s between posts).
        while self.running:
            # sleep ~45-75s randomized to avoid strict periodicity
            time.sleep(random.randint(45, 75))
            # don't spam if user hasn't cleared notifications
            try:
                if self.unread_count() >= 6:
                    # skip this round and wait for next interval
                    continue
            except Exception:
                pass

            category = random.choices(list(weights.keys()), weights=list(weights.values()))[0]
            options = [n for n in examples if n[2] == category]
            if not options:
                continue

            title, msg, cat = random.choice(options)
            # Avoid posting the exact same title that is already recent
            recent_titles = [n.title for n in self.notifications[-12:]]
            if title in recent_titles:
                # pick a different one if possible
                alt = [o for o in options if o[0] not in recent_titles]
                if alt:
                    title, msg, cat = random.choice(alt)

            # Add more context to weather notifications
            if cat == "Weather":
                extra = {"forecast": random.choice(["Rain", "Sunny", "Windy", "Cloudy"]), "rain_chance": random.randint(0, 100)}
                sev = "warning" if extra["rain_chance"] > 70 else ("normal" if extra["rain_chance"] < 30 else "notice")
                message = f"{msg} Forecast: {extra['forecast']}. Rain chance: {extra['rain_chance']}%."
                self.post(title, message, cat, severity=sev, extra=extra)
            else:
                self.post(title, msg, cat)

    def stop(self):
        self.running = False

    #Counting unread notifications
    def unread_count(self):
        return sum(1 for n in self.notifications if not n.read)

    def _update_badge(self):
        if self.badge_callback:
            self.badge_callback(self.unread_count())

#Notification Center Window
class NotificationCenter(tk.Toplevel):
    """Displays all notifications in a window."""
    def __init__(self, root, manager: NotificationManager):
        super().__init__(root)
        self.title("Notification Center")
        self.geometry("460x520")
        self.configure(bg="white")
        self.manager = manager

        tk.Label(self, text="Notifications", font=("Segoe UI", 14, "bold"),
                 bg="white").pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("Title","Category","Severity","Message","Time"), show="headings", height=20)
        self.tree.heading("Title", text="Title")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Severity", text="Severity")
        self.tree.heading("Message", text="Message")
        self.tree.heading("Time", text="Time")
        self.tree.column("Title", width=120)
        self.tree.column("Category", width=80)
        self.tree.column("Severity", width=70)
        self.tree.column("Message", width=200)
        self.tree.column("Time", width=100)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        #Buttons
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Mark All as Read", command=self.mark_all_read).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Close", command=self.destroy).pack(side="left", padx=5)

        self.populate()
        # Mark displayed notifications as read and refresh the view/badge
        for n in self.manager.notifications:
            n.read = True
        self.manager._update_badge()
        self.populate()
    def populate(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for notif in reversed(self.manager.notifications):
            tag = notif.category.lower()
            sev = notif.severity
            self.tree.insert("", "end",
                values=(notif.title, notif.category, sev, notif.message, notif.timestamp),
                tags=(tag,))
        self.tree.tag_configure("weather", background="#e3f2fd")
        self.tree.tag_configure("watering", background="#e8f5e9")
        self.tree.tag_configure("disease", background="#ffebee")
        self.tree.tag_configure("crop health", background="#f3e5f5")
        self.tree.tag_configure("sustainability", background="#f1f8e9")
        self.tree.tag_configure("market", background="#fffde7")

    def mark_all_read(self):
        for notif in self.manager.notifications:
            notif.read = True
        self.manager._update_badge()
        self.populate()