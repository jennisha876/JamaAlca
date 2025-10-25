"""
Data service for managing real vs placeholder data
This is like the app's memory - it keeps track of what the farmer has done and calculates their progress
Think of this as the app's way of remembering things and doing math to show how well the farmer is doing
"""
from config import Config
import random
from datetime import datetime, timedelta

class DataService:
    """
    Service for managing application data
    This class is like a smart calculator that keeps track of the farmer's progress
    It can show real data (if we have it) or fake data (for testing and demonstration)
    """
    
    def __init__(self):
        # Check if we should use real data or fake data
        # This is like a switch - you can turn it on or off
        self.use_real_data = Config.USE_REAL_DATA
        
        # This is where we store information about what the farmer has done
        # Think of this as the app's notebook where it writes down everything
        self.user_data = {
            "water_saved": 0,        # How much water the farmer has saved (in liters)
            "yield_increase": 0,     # How much more crops they're growing (in percentage)
            "chemicals_reduced": 0,  # How many fewer chemicals they're using (in percentage)
            "scans_today": 0,        # How many times they've checked their plants today
            "last_scan": None        # When they last checked their plants
        }
    
    def get_sustainability_metrics(self):
        """
        Get sustainability impact metrics
        This shows the farmer how much good they're doing for the environment
        Like a report card that shows how much water they've saved, how much more food they're growing, etc.
        """
        if self.use_real_data:
            # If we have real data, calculate it from what the farmer has actually done
            return self._calculate_real_metrics()
        else:
            # If we don't have real data, show some example numbers to demonstrate the feature
            return {
                "water_saved": "2,500 L",
                "yield_increase": "+12%",
                "chemicals_reduced": "-8%"
            }
    
    def _calculate_real_metrics(self):
        """
        Calculate real metrics from user data
        This does the math to figure out how much the farmer has improved
        Like adding up all the water they've saved and showing the total
        """
        # This would integrate with a real database in the future
        return {
            "water_saved": f"{self.user_data['water_saved']:,} L",
            "yield_increase": f"+{self.user_data['yield_increase']}%",
            "chemicals_reduced": f"-{self.user_data['chemicals_reduced']}%"
        }
    
    def get_crop_health_status(self):
        """
        Get current crop health status
        This tells the farmer how their crops are doing overall
        Like a health check that says "your crops look good" or "they need attention"
        """
        if self.use_real_data:
            # In real implementation, this would check actual crop data
            recent_scans = self.user_data.get("scans_today", 0)
            if recent_scans == 0:
                return "No recent scans"  # They haven't checked their plants lately
            elif recent_scans < 3:
                return "Good condition"   # They've checked a few times and everything looks good
            else:
                return "Needs attention"  # They've checked many times, maybe there are problems
        else:
            return "Good condition"  # Show a positive message for demonstration
    
    def get_weather_summary(self):
        """
        Get current weather summary
        This shows the farmer what the weather is like right now
        Like a quick weather report that says "it's sunny and warm"
        """
        if self.use_real_data:
            try:
                # Import here to avoid circular imports
                from services.weather_fetcher import WeatherFetcher
                weather_fetcher = WeatherFetcher()
                
                # Get coordinates and fetch weather data
                coords = weather_fetcher.get_coordinates()
                if coords[0] and coords[1]:
                    forecast = weather_fetcher.get_weather_forecast()
                    if forecast and len(forecast) > 0:
                        # Get today's weather (first day in forecast)
                        today = forecast[0]
                        temp = today.get("temp_max", "0°C").replace("°C", "")
                        condition = today.get("condition", "Unknown")
                        return f"{temp}°C, {condition}"
                
                # Fallback if weather fetch fails
                return "28°C, Sunny"
            except Exception as e:
                print(f"Error getting real weather data: {e}")
                return "28°C, Sunny"  # Fallback to example weather
        else:
            return "28°C, Sunny"  # Show example weather for demonstration
    
    def get_next_watering(self):
        """
        Get next watering schedule
        This tells the farmer when they should water their plants next
        Like a reminder that says "water your plants tomorrow"
        """
        if self.use_real_data:
            try:
                # Import here to avoid circular imports
                from services.weather_fetcher import WeatherFetcher
                weather_fetcher = WeatherFetcher()
                
                # Get weather data to make smart watering recommendations
                coords = weather_fetcher.get_coordinates()
                if coords[0] and coords[1]:
                    forecast = weather_fetcher.get_weather_forecast()
                    if forecast and len(forecast) > 1:
                        # Check tomorrow's weather to recommend watering
                        tomorrow = forecast[1]
                        rain_chance = tomorrow.get("rain_chance", "0%").replace("%", "")
                        
                        try:
                            rain_percentage = int(float(rain_chance))
                            # Smart watering recommendations based on rain forecast
                            if rain_percentage > 50:
                                return "Skip - Rain expected"  # Don't water if it's going to rain
                            elif rain_percentage > 30:
                                return "Maybe tomorrow"        # Maybe water, rain is possible
                            else:
                                return "Tomorrow"             # Safe to water, no rain expected
                        except (ValueError, TypeError):
                            return "Tomorrow"
                
                # Fallback if weather data unavailable
                return "Tomorrow"
            except Exception as e:
                print(f"Error getting watering recommendation: {e}")
                return "Tomorrow"
        else:
            return "Tomorrow"  # Show example schedule for demonstration
    
    def get_market_price(self):
        """
        Get current market price information
        This shows the farmer how much their crops are worth right now
        Like a stock market report but for farming
        """
        if self.use_real_data:
            # This would integrate with market data APIs to get real prices
            return "Corn: ↑ 12%"  # In the future, this would be real market data
        else:
            return "Corn: ↑ 12%"  # Show example prices for demonstration
    
    def update_scan_data(self, crop_type, disease_detected):
        """
        Update scan data when a new scan is performed
        This is like keeping a diary - every time the farmer checks their plants, we write it down
        We also update their progress based on what they found
        """
        # Count how many times they've checked their plants today
        self.user_data["scans_today"] += 1
        self.user_data["last_scan"] = datetime.now()
        
        # Update sustainability metrics based on scan results
        # If they found a healthy plant, they're doing something right
        if not disease_detected:
            self.user_data["water_saved"] += random.randint(50, 200)      # They saved some water
            self.user_data["yield_increase"] += random.randint(1, 3)      # Their crops are growing better
        else:
            # If they found a disease, they're learning to use fewer chemicals
            self.user_data["chemicals_reduced"] += random.randint(1, 5)   # They're using fewer chemicals
    
    def get_todays_tip(self):
        """
        Get today's farming tip
        This gives the farmer a helpful piece of advice every day
        Like a daily farming lesson that helps them grow better crops
        """
        # These are helpful tips that farmers can use to improve their farming
        tips = [
            "Mulch your soil to retain moisture and reduce water usage during dry seasons.",
            "Water your plants early in the morning to reduce evaporation loss.",
            "Rotate your crops annually to prevent soil depletion and disease buildup.",
            "Use companion planting to naturally deter pests and improve soil health.",
            "Check soil pH regularly and adjust as needed for optimal plant growth.",
            "Apply organic compost to boost soil carbon storage and fertility.",
            "Monitor weather forecasts to plan irrigation and planting schedules.",
            "Use drip irrigation systems for more efficient water delivery."
        ]
        
        # Use the date to get a consistent tip for the day
        # This means the same tip will show all day, but it changes each day
        day_of_year = datetime.now().timetuple().tm_yday
        tip_index = day_of_year % len(tips)
        return tips[tip_index]
