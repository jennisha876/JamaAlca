# Screens Module

This directory contains all the UI screen components for the JamaAlca application.

## Available Screens

1. `login_screen.py` - User authentication screen
   ```python
   from screens.login_screen import LoginScreen
   ```

2. `home_screen.py` - Main dashboard screen
   ```python
   from screens.home_screen import HomeScreen
   ```

3. `plant_screen.py` - Plant disease detection screen
   ```python
   from screens.plant_screen import PlantScreen
   ```

4. `weather_screen.py` - Weather monitoring screen
   ```python
   from screens.weather_screen import WeatherScreen
   ```

5. `profile_screen.py` - User profile management
   ```python
   from screens.profile_screen import ProfileScreen
   ```

6. `community_screen.py` - Community forum screen
   ```python
   from screens.community_screen import CommunityScreen
   ```

7. `alerts_screen.py` - Notification and alerts screen
   ```python
   from screens.alerts_screen import AlertsScreen
   ```

## Screen Structure

Each screen follows a common structure:
```python
class ScreenName(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Screen-specific UI elements
```

## Navigation

To navigate between screens:
```python
controller.show_frame("ScreenName")
```

## Common UI Elements

- Navigation bar at the bottom of each screen
- Consistent color scheme and styling
- Scrollable content areas where needed