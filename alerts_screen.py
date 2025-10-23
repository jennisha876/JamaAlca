import tkinter as tk

class AlertsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f3f0")
        self.controller = controller

        header = tk.Frame(self, bg="#f5f3f0")
        header.pack(fill="x", pady=(8,4), padx=10)
        tk.Label(header, text="🚨 Alerts", font=("Arial", 22, "bold"), fg="#2c4a3a", bg="#f5f3f0").pack(side="left")
        tk.Button(header, text="← Back", command=lambda: controller.show_frame("HomeScreen"), bg="#f5f3f0", relief="flat", cursor="hand2").pack(side="right")

        self.alerts_list_frame = tk.Frame(self, bg="#f5f3f0")
        self.alerts_list_frame.pack(fill="both", expand=True, padx=15, pady=10)
        # register for refresh so the Alerts screen can be updated when manager changes
        try:
            controller.register_refresh_callback(self.refresh_alerts)
        except Exception:
            pass
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
        # Note: do NOT call _update_badge() here; the notification manager will
        # update the badge when notifications change. Calling it here previously
        # caused a recursive loop where creating the Alerts screen triggered
        # badge updates which recreated frames.
