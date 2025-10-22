import tkinter as tk
from tkinter import ttk
import threading, time, random
from datetime import datetime

#Notification Object
class Notification:
    def __init__(self, title, message, category="General"):
        self.title = title
        self.message = message
        self.category = category
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.read = False


#Notification Manager
class NotificationManager:
    """Handles posting, storing, and displaying toast notifications."""
    def __init__(self, root):
        self.root = root
        self.notifications = []
        self.running = True
        #Demo auto-generate alerts
        threading.Thread(target=self._auto_generate_demo, daemon=True).start()

    def post(self, title, message, category="General"):
        notif = Notification(title, message, category)
        self.notifications.append(notif)
        self._show_toast(notif)

    def _show_toast(self, notif):
        """Popup toast message."""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        toast.configure(bg="#333")
        toast.update_idletasks()
        w, h = 260, 100
        x = toast.winfo_screenwidth() - w - 30
        y = toast.winfo_screenheight() - h - 70
        toast.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(toast, text=notif.title, font=("Segoe UI", 10, "bold"),
                fg="white", bg="#333").pack(pady=(8,0))
        tk.Label(toast, text=notif.message, fg="#ddd", bg="#333",
                wraplength=240, justify="left").pack(pady=(0,5))
        toast.after(4000, toast.destroy)

    def _auto_generate_demo(self):
        """Simulate alerts periodically for demo."""
        examples = [
            ("💧 Water Reminder", "Time to irrigate your crops", "Water"),
            ("🌦 Weather Alert", "Rain expected this afternoon", "Weather"),
            ("🚨 Disease Warning", "Possible fungal infection detected", "Disease"),
            ("🪴 Tip", "Apply compost for better soil retention", "Tips"),
        ]
        while self.running:
            time.sleep(random.randint(15, 25))
            title, msg, cat = random.choice(examples)
            self.post(title, msg, cat)

    def stop(self):
        self.running = False


#Notification Center Window
class NotificationCenter(tk.Toplevel):
    """Displays full list of all notifications."""
    def __init__(self, root, manager: NotificationManager):
        super().__init__(root)
        self.title("Notification Center")
        self.geometry("420x500")
        self.configure(bg="white")
        self.manager = manager

        tk.Label(self, text="Notifications", font=("Segoe UI", 14, "bold"),
                bg="white").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Title","Message","Time"), show="headings", height=20)
        self.tree.heading("Title", text="Title")
        self.tree.heading("Message", text="Message")
        self.tree.heading("Time", text="Time")
        self.tree.column("Title", width=120)
        self.tree.column("Message", width=200)
        self.tree.column("Time", width=100)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(self, text="Close", command=self.destroy).pack(pady=5)
        self.populate()

    def populate(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for notif in reversed(self.manager.notifications):
            self.tree.insert("", "end",
                values=(notif.title, notif.message, notif.timestamp))