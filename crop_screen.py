import tkinter as tk

def suggest_crops(season, soil):
    return ["Tomato", "Corn", "Potato"]

class CropScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Crop Suggestions", font=("Arial", 24)).pack(pady=10)
        self.season_var = tk.StringVar()
        self.soil_var = tk.StringVar()
        tk.OptionMenu(self, self.season_var, "Spring", "Summer", "Autumn", "Winter").pack(pady=5)
        tk.OptionMenu(self, self.soil_var, "Loamy", "Sandy", "Clay").pack(pady=5)
        tk.Button(self, text="Get Suggestions", command=self.show_suggestions).pack(pady=5)
        self.result_label = tk.Label(self, text="")
        self.result_label.pack(pady=5)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomeScreen")).pack(pady=10)

    def show_suggestions(self):
        season = self.season_var.get()
        soil = self.soil_var.get()
        suggestions = suggest_crops(season, soil)
        self.result_label.config(text=f"Suggested Crops: {', '.join(suggestions)}")
