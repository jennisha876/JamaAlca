import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class ProfileScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f3f0")
        self.controller = controller

        # Profile state
        self.is_editing = False
        self.profile_data = {
            "name": tk.StringVar(value="John Farmer"),
            "phone": tk.StringVar(value="+1 234 567 8900"),
            "location": tk.StringVar(value="Kingston, Jamaica"),
            "farm_size": tk.StringVar(value="Medium"),
            "main_crop": tk.StringVar(value="Corn")
        }
        self.notifications = {
            "push": tk.BooleanVar(value=True),
            "voice": tk.BooleanVar(value=True),
            "pest": tk.BooleanVar(value=True),
            "weather": tk.BooleanVar(value=True),
            "fertilizer": tk.BooleanVar(value=True),
            "market": tk.BooleanVar(value=False)
        }

        # --- Header ---
        tk.Label(self, text="My Account", font=("Arial", 22, "bold"), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(15, 2))
        tk.Label(self, text="Manage your profile and settings", font=("Arial", 12), fg="#6b7c6f", bg="#f5f3f0").pack(pady=(0, 10))

        # --- Profile Card ---
        self.card_frame = tk.Frame(self, bg="white", highlightbackground="#d4c5b0", highlightthickness=2, padx=20, pady=15)
        self.card_frame.pack(pady=10, fill="x", padx=15)

        self._render_profile_card()

        # --- Notification Settings ---
        self._render_notifications()

        # --- App Info and Logout ---
        info_frame = tk.Frame(self, bg="white", highlightbackground="#d4c5b0", highlightthickness=2, padx=15, pady=10)
        info_frame.pack(fill="x", padx=15, pady=(5, 5))
        tk.Label(info_frame, text="JamaAlca Farming App", bg="white", fg="#6b7c6f").pack()
        tk.Label(info_frame, text="Version 1.0.0", bg="white", fg="#6b7c6f").pack()

        tk.Button(self, text="Log Out", bg="white", fg="red", highlightbackground="red",
                  command=self.logout, relief="solid").pack(fill="x", padx=15, pady=(0, 10))

        # --- Bottom Navigation ---
        nav_frame = tk.Frame(self, bg="#e8f5e9", height=50)
        nav_frame.pack(side="bottom", fill="x")
        tk.Button(nav_frame, text="🏠 Home", bg="#c8e6c9",
                  command=lambda: controller.show_frame("HomeScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌿 Plant Detection",
                  command=lambda: controller.show_frame("PlantScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌤 Weather",
                  command=lambda: controller.show_frame("WeatherScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="👤 Profile",
                  command=lambda: controller.show_frame("ProfileScreen")).pack(side="left", expand=True, fill="x")

    def _render_profile_card(self):
        # Clear frame
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        tk.Label(self.card_frame, text=self.profile_data["name"].get(), font=("Arial", 16, "bold"), fg="#2c4a3a", bg="white").pack(anchor="w")
        tk.Label(self.card_frame, text=self.profile_data["phone"].get(), font=("Arial", 12), fg="#6b7c6f", bg="white").pack(anchor="w", pady=(0, 5))

        btn_text = "Cancel" if self.is_editing else "Edit Profile"
        tk.Button(self.card_frame, text=btn_text, bg="#4a7c59", fg="white", command=self.toggle_edit).pack(pady=(5,10))

        if self.is_editing:
            # Editable fields
            self._create_entry("Full Name", self.profile_data["name"])
            self._create_entry("Location", self.profile_data["location"])
            self._create_combobox("Farm Size", self.profile_data["farm_size"], ["Small", "Medium", "Large"])
            self._create_combobox("Main Crop", self.profile_data["main_crop"],
                                  ["Corn", "Wheat", "Rice", "Soybeans", "Cotton", "Vegetables", "Fruits", "Sugarcane"])
            tk.Button(self.card_frame, text="Save Changes", bg="#4a7c59", fg="white", command=self.save_profile).pack(pady=(10, 0))

    def _create_entry(self, label_text, var):
        tk.Label(self.card_frame, text=label_text, fg="#2c4a3a", bg="white").pack(anchor="w", pady=(5,0))
        tk.Entry(self.card_frame, textvariable=var, font=("Arial", 12), bg="white", relief="solid", bd=1).pack(fill="x", pady=(2,5))

    def _create_combobox(self, label_text, var, values):
        tk.Label(self.card_frame, text=label_text, fg="#2c4a3a", bg="white").pack(anchor="w", pady=(5,0))
        cb = ttk.Combobox(self.card_frame, textvariable=var, values=values, state="readonly", font=("Arial", 12))
        cb.pack(fill="x", pady=(2,5))

    def toggle_edit(self):
        self.is_editing = not self.is_editing
        self._render_profile_card()

    def save_profile(self):
        self.is_editing = False
        self._render_profile_card()
        messagebox.showinfo("Profile Saved", "Your profile has been updated.")

    def _render_notifications(self):
        notif_frame = tk.Frame(self, bg="white", highlightbackground="#d4c5b0", highlightthickness=2, padx=15, pady=10)
        notif_frame.pack(fill="x", padx=15, pady=(5,5))

        tk.Label(notif_frame, text="Notifications", font=("Arial", 14, "bold"), bg="white", fg="#2c4a3a").pack(anchor="w")
        for key, var in self.notifications.items():
            frame = tk.Frame(notif_frame, bg="white")
            frame.pack(fill="x", pady=2)
            tk.Label(frame, text=key.replace("_", " ").title(), bg="white", fg="#2c4a3a").pack(side="left")
            tk.Checkbutton(frame, variable=var, bg="white").pack(side="right")

    def logout(self):
        messagebox.showinfo("Logout", "You have been logged out.")
        self.controller.show_frame("LoginScreen")