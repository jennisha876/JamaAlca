import tkinter as tk
from tkinter import messagebox

class SoilScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f3f0")
        self.controller = controller

        nav_frame = tk.Frame(self, bg="#e8f5e9", height=50)
        nav_frame.pack(side="bottom", fill="x")
        tk.Button(nav_frame, text="🏠 Home", bg="#c8e6c9", command=lambda: controller.show_frame("HomeScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌿 Plant Detection", bg="#c8e6c9", command=lambda: controller.show_frame("PlantScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌤 Weather", bg="#c8e6c9", command=lambda: controller.show_frame("WeatherScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="👤 Profile", bg="#c8e6c9", command=lambda: controller.show_frame("ProfileScreen")).pack(side="left", expand=True, fill="x")

        tk.Label(self, text="Soil Test", font=("Arial", 20, "bold"), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(15,5))

        form = tk.Frame(self, bg="#f5f3f0")
        form.pack(padx=20, pady=10)

        tk.Label(form, text="pH (0-14):", bg="#f5f3f0").grid(row=0, column=0, sticky="w", pady=5)
        self.ph_var = tk.DoubleVar(value=6.5)
        tk.Entry(form, textvariable=self.ph_var).grid(row=0, column=1, pady=5)

        tk.Label(form, text="Moisture (%):", bg="#f5f3f0").grid(row=1, column=0, sticky="w", pady=5)
        self.moist_var = tk.DoubleVar(value=30.0)
        tk.Entry(form, textvariable=self.moist_var).grid(row=1, column=1, pady=5)

        tk.Button(self, text="Run Soil Analysis", bg="#4a7c59", fg="white", command=self.run_analysis).pack(pady=10)

        self.result_frame = tk.Frame(self, bg="#f5f3f0")
        self.result_frame.pack(fill="x", padx=20, pady=(0,10))

    def run_analysis(self):
        ph = self.ph_var.get()
        moist = self.moist_var.get()

        recs = []
        if ph < 5.5:
            recs.append("Soil is acidic: consider lime application to raise pH.")
        elif ph > 7.5:
            recs.append("Soil is alkaline: consider sulfur or organic matter to lower pH.")
        else:
            recs.append("Soil pH is in the optimal range.")

        if moist < 20:
            recs.append("Soil moisture low: irrigate soon.")
        elif moist > 70:
            recs.append("Soil moisture high: improve drainage and avoid waterlogging.")
        else:
            recs.append("Soil moisture is adequate.")

        for w in self.result_frame.winfo_children():
            w.destroy()

        tk.Label(self.result_frame, text="Soil Analysis Results:", font=("Arial", 12, "bold"), bg="#f5f3f0").pack(anchor="w")
        for r in recs:
            tk.Label(self.result_frame, text=f"• {r}", bg="#f5f3f0").pack(anchor="w")
