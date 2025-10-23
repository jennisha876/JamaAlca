import tkinter as tk

class AlertsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f3f0")
        self.controller = controller

        tk.Label(self, text="🚨 Alerts", font=("Arial", 22, "bold"), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(15, 5))

        self.alerts_list_frame = tk.Frame(self, bg="#f5f3f0")
        self.alerts_list_frame.pack(fill="both", expand=True, padx=15, pady=10)
        self.refresh_alerts()

    def refresh_alerts(self):
        for widget in self.alerts_list_frame.winfo_children():
            widget.destroy()

        for notif in reversed(self.controller.notif_manager.notifications):
            frame = tk.Frame(self.alerts_list_frame, bg="white", bd=1, relief="solid")
            frame.pack(fill="x", pady=3)
            tk.Label(frame, text=notif.title, font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=(3,0))
            tk.Label(frame, text=notif.message, font=("Arial", 10), bg="white", wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))
            tk.Label(frame, text=notif.timestamp, font=("Arial", 9), fg="#777", bg="white").pack(anchor="e", padx=10)