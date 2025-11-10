import tkinter as tk
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.profile_screen import ProfileScreen
from screens.plant_screen import PlantScreen
from screens.weather_screen import WeatherScreen
from screens.community_screen import CommunityScreen
from screens.alerts_screen import AlertsScreen
from screens.irrigation_sreen import IrrigationScreen
from utils.notifications import NotificationManager, NotificationCenter

class JamaAlca(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JamaAlca")
        self.geometry("490x700")

        # Create a NotificationManager instance
        self.notif_manager = NotificationManager(self)

        self.frames = {}
        for F in (LoginScreen, HomeScreen, ProfileScreen, PlantScreen, WeatherScreen, CommunityScreen, AlertsScreen, IrrigationScreen):
            frame = F(parent=self, controller=self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)
        self.show_frame("LoginScreen")

    def show_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()
        else:
            from tkinter import messagebox
            messagebox.showerror("Navigation Error", f"Screen not found: {frame_name}")

    def open_notification_center(self):
        NotificationCenter(self, self.notif_manager)

if __name__ == "__main__":
    app = JamaAlca()
    app.mainloop()