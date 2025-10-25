import tkinter as tk
from tkinter import ttk
import threading, time, random
from datetime import datetime


#Notification Class
class Notification:
    def __init__(self, title, message, category="General"):
        self.title = title
        self.message = message
        self.category = category
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.read = False


#Notification Manager
class NotificationManager:
    """
    Handles posting, storing, and displaying toast notifications.
    This system only sends notifications after the user has logged in.
    """
    def __init__(self, root, badge_callback=None):
        self.root = root
        self.notifications = []
        self.running = False  # Start with notifications disabled
        self.badge_callback = badge_callback
        self.user_logged_in = False  # Track login status
        # Don't start auto-generating notifications until user logs in

    def start_notifications(self):
        """
        Start sending notifications after user logs in
        This ensures notifications only appear for logged-in users
        """
        if not self.running:
            self.running = True
            self.user_logged_in = True
            print("[Notifications] Starting notification system for logged-in user")
            threading.Thread(target=self._auto_generate_demo, daemon=True).start()

    def stop_notifications(self):
        """
        Stop sending notifications when user logs out
        This prevents notifications from appearing for non-logged-in users
        """
        self.running = False
        self.user_logged_in = False
        print("[Notifications] Stopping notification system - user logged out")

    def post(self, title, message, category="General"):
        # Only post notifications if user is logged in
        if not self.user_logged_in:
            print("[Notifications] Ignoring notification - user not logged in")
            return
            
        notif = Notification(title, message, category)
        self.notifications.append(notif)
        self._show_toast(notif)
        self._update_badge()

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

        tk.Label(toast, text=notif.title, font=("Segoe UI", 10, "bold"),
                 fg="white", bg="#333").pack(pady=(10, 0))
        tk.Label(toast, text=notif.message, fg="#ddd", bg="#333",
                 wraplength=250, justify="left").pack(pady=(0, 5))

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

        while self.running:
            time.sleep(random.randint(10, 25))
            category = random.choices(list(weights.keys()), weights=list(weights.values()))[0]
            options = [n for n in examples if n[2] == category]
            if options:
                title, msg, cat = random.choice(options)
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

        self.tree = ttk.Treeview(self, columns=("Title","Message","Time"), show="headings", height=20)
        self.tree.heading("Title", text="Title")
        self.tree.heading("Message", text="Message")
        self.tree.heading("Time", text="Time")
        self.tree.column("Title", width=130)
        self.tree.column("Message", width=220)
        self.tree.column("Time", width=100)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        #Buttons
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Mark All as Read", command=self.mark_all_read).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Close", command=self.destroy).pack(side="left", padx=5)

        self.populate()

    def populate(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for notif in reversed(self.manager.notifications):
            tag = notif.category.lower()
            self.tree.insert("", "end",
                values=(notif.title, notif.message, notif.timestamp),
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