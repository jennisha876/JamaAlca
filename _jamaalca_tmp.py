import tkinter as tk

from notifications import NotificationManager, NotificationCenter
from tkinter import filedialog, messagebox, ttk, simpledialog
from predict_disease import predict_disease
from PIL import Image, ImageTk
from treatment_recommendation import get_treatment_recommendation
from weather_screen import WeatherScreen
from scans import ScanStore
from db import DBHelper

# Extracted screen modules
from home_screen import HomeScreen
from plant_screen import PlantScreen
from profile_screen import ProfileScreen
from crop_screen import CropScreen
from community_screen import CommunityScreen
from alerts_screen import AlertsScreen


def suggest_crops(season, soil):
    return ["Tomato", "Corn", "Potato"]


class JamaAlca(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JamaAlca")
        self.geometry("700x600")
        self.resizable(True, True)

        # Services
        self._badge_update_callbacks = []
        self.notif_manager = NotificationManager(self, badge_callback=self._update_unread_count)
        self.db = DBHelper()
        self.scan_store = ScanStore(db_helper=self.db)
        self.user_id = None

        # Initialize frames
        self.frames = {}
        for F in (HomeScreen, ProfileScreen, PlantScreen, CropScreen, WeatherScreen, CommunityScreen, AlertsScreen):
            frame = F(parent=self, controller=self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)
        self.show_frame("HomeScreen")

    def register_badge_callback(self, cb):
        if cb not in self._badge_update_callbacks:
            self._badge_update_callbacks.append(cb)

    def _update_unread_count(self, count):
        for cb in list(self._badge_update_callbacks):
            try:
                cb(count)
            except Exception:
                pass

        # Recreate/refresh frames so UI can reflect notification changes
        self.frames = {}
        for F in (HomeScreen, ProfileScreen, PlantScreen, CropScreen, WeatherScreen, CommunityScreen, AlertsScreen):
            frame = F(parent=self, controller=self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)
        self.show_frame("HomeScreen")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def open_notification_center(self):
        NotificationCenter(self, self.notif_manager)


if __name__ == "__main__":
    app = JamaAlca()
    app.mainloop()
