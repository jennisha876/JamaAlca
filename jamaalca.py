"""
JamaAlca - AI-Powered Farming Application
Main application entry point that sets up the GUI and manages screen navigation
"""

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
    """
    Main application class that manages the entire JamaAlca farming app
    This is like the brain of the app - it controls which screen you see and handles notifications
    """
    
    def __init__(self):
        super().__init__()
        
        # Set up the main window properties - this is what the user sees first
        self.title("JamaAlca")
        self.geometry("490x700")  # Mobile-like size for easy use on different devices

        # Create the notification system - this handles all the alerts and messages
        # Think of this as the app's way of talking to the farmer
        self.notif_manager = NotificationManager(self)

        # Set up all the different screens (pages) in the app
        # Each screen is like a different room in a house - they all exist but you only see one at a time
        self.frames = {}
        screen_classes = (LoginScreen, HomeScreen, ProfileScreen, PlantScreen, WeatherScreen, CommunityScreen, AlertsScreen, IrrigationScreen)
        
        for ScreenClass in screen_classes:
            # Create each screen and store it in our frames dictionary
            # The controller=self part lets each screen talk back to the main app
            frame = ScreenClass(parent=self, controller=self)
            self.frames[ScreenClass.__name__] = frame
            frame.place(relwidth=1, relheight=1)  # Make each screen fill the whole window
        
        # Start the app by showing the login screen first
        self.show_frame("LoginScreen")

    def show_frame(self, frame_name):
        """
        Switch between different screens in the app
        This is like changing channels on TV - you can only see one screen at a time
        """
        frame = self.frames[frame_name]
        frame.tkraise()  # Bring the requested screen to the front
        
        # Refresh notification badge when home screen is shown
        if frame_name == "HomeScreen" and hasattr(frame, 'refresh_notification_badge'):
            frame.refresh_notification_badge()

    def open_notification_center(self):
        """
        Open the notification center where farmers can see all their alerts
        This is like opening your inbox to see all your messages
        """
        NotificationCenter(self, self.notif_manager)

# This is where the app actually starts running
# When someone double-clicks the jamaalca.py file, this code runs
if __name__ == "__main__":
    app = JamaAlca()  # Create the main app
    app.mainloop()   # Start the app and keep it running until the user closes it