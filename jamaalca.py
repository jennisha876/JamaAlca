#import list
import tkinter as tk
import threading
import random

#From list
from notifications import NotificationManager, NotificationCenter
from tkinter import filedialog, messagebox, ttk, simpledialog
from predict_disease import predict_disease
from PIL import Image, ImageTk
from treatment_recommendation import get_treatment_recommendation
from weather_screen import WeatherScreen

plant_classes = ["Tomato Healthy", "Tomato Late Blight", "Potato Healthy", "Corn Healthy"]
'''
def predict_disease(image_path):
    return random.choice(plant_classes)
'''
def suggest_crops(season, soil):
    return ["Tomato", "Corn", "Potato"]

def get_weather_alert():
    return random.choice(["No alerts", "Drought warning", "Heavy rainfall expected"])

class JamaAlca(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JamaAlca")
        self.geometry("700x600")

        # Create a NotificationManager instance here:
        self.notif_manager = NotificationManager(self)

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

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f9f9")

        main_frame = tk.Frame(self, bg="#f9f9f9")
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame, bg="#f9f9f9", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout for scroll area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Make mouse wheel scroll the canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)


        header_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        header_frame.pack(fill="x", pady=(10, 5), padx=10)

        tk.Label(header_frame, text="Welcome back, Farmer!",
                font=("Arial", 18, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(anchor="w")

        tk.Label(header_frame, text="Here’s your farm overview for today.",
                font=("Arial", 11), fg="#6b7c6f", bg="#f9f9f9").pack(anchor="w")
        '''
        alert_btn = tk.Button(header_frame, text="🔔",font=("Arial", 16), bg="#f9f9f9", bd=0, relief="flat", cursor="hand2",
        command=lambda: controller.show_frame("AlertsScreen"))
        '''
        alert_btn = tk.Button(
            header_frame,
            text="🔔",
            font=("Arial", 16),
            bg="#f9f9f9",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=controller.open_notification_center
        )

        alert_btn.pack(side="right")

        # Drought Warning Banner
        drought_frame = tk.Frame(scrollable_frame, bg="#fff3e0",
                                highlightbackground="#ffcc80", highlightthickness=2)
        drought_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(drought_frame, text="⚠ Drought Warning!",
                font=("Arial", 12, "bold"), fg="#e65100", bg="#fff3e0").pack(anchor="w", padx=10)
        tk.Label(drought_frame,
                text="Low rainfall expected this week. Conserve water and schedule irrigation wisely.",
                font=("Arial", 10), fg="#bf360c", bg="#fff3e0",
                wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))

        # Disease Alert Banner
        disease_frame = tk.Frame(scrollable_frame, bg="#ffebee",
                                highlightbackground="#ef9a9a", highlightthickness=2)
        disease_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(disease_frame, text="⚠ Disease Alert!",
                font=("Arial", 12, "bold"), fg="#c62828", bg="#ffebee").pack(anchor="w", padx=10)
        tk.Label(disease_frame,
                text="Possible leaf spot detected in your region. Check affected crops.",
                font=("Arial", 10), fg="#b71c1c", bg="#ffebee",
                wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0,5))

        # Quick Stats
        stats_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        stats_frame.pack(fill="x", padx=10, pady=(10,0))

        def _stat_card(parent, title, value, color, show_frame, controller):
            card = tk.Frame(parent, bg=color, bd=2, relief="ridge")
            tk.Label(card, text=title, bg=color, font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(5,0))

        row1 = tk.Frame(stats_frame, bg="#f9f9f9")
        row1.pack(fill="x", pady=2)
        self._stat_card(row1, "🌿 Crop Health", "Good condition", "#a5d6a7", "PlantScreen", controller).pack(side="left", expand=True, fill="x", padx=5)
        self._stat_card(row1, "🌤 Weather", "28°C, Sunny", "#90caf9", "WeatherScreen", controller).pack(side="left", expand=True, fill="x", padx=5)

        row2 = tk.Frame(stats_frame, bg="#f9f9f9")
        row2.pack(fill="x", pady=2)
        self._stat_card(row2, "💧 Next Watering", "Tomorrow", "#b3e5fc", "IrrigationScreen", controller).pack(side="left", expand=True, fill="x", padx=5)
        self._stat_card(row2, "💰 Market Price", "Corn: ↑ 12%", "#fff59d", None, controller).pack(side="left", expand=True, fill="x", padx=5)

        # Sustainability Impact
        impact_frame = tk.LabelFrame(scrollable_frame, text="🌱 Sustainability Impact",
                                    bg="#f1f8e9", fg="#2c4a3a", font=("Arial", 12, "bold"))
        impact_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(impact_frame, text="💧 Water Saved: 2,500 L", font=("Arial", 11),
                bg="#f1f8e9", fg="#1565c0").pack(anchor="w", padx=10)
        tk.Label(impact_frame, text="📈 Yield Increase: +12%", font=("Arial", 11),
                bg="#f1f8e9", fg="#2e7d32").pack(anchor="w", padx=10)
        tk.Label(impact_frame, text="🍃 Chemicals Reduced: -8%", font=("Arial", 11),
                bg="#f1f8e9", fg="#00695c").pack(anchor="w", padx=10)

        # Quick Tip
        tip_frame = tk.LabelFrame(scrollable_frame, text="💡 Today's Tip",
                                bg="#fffde7", fg="#2c4a3a", font=("Arial", 12, "bold"))
        tip_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(tip_frame,
                text="Mulch your soil to retain moisture and reduce water usage during dry seasons.",
                font=("Arial", 10), fg="#6b7c6f", bg="#fffde7",
                wraplength=450, justify="left").pack(anchor="w", padx=10, pady=5)

        # Community
        community_frame = tk.LabelFrame(scrollable_frame, text="👩🏾‍🌾 Join the Community",
                                        bg="#f3e5f5", fg="#2c4a3a", font=("Arial", 12, "bold"))
        community_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(community_frame,
                text="Connect with other farmers, share insights, and discuss challenges.",
                font=("Arial", 10), fg="#6b7c6f", bg="#f3e5f5",
                wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(5,0))
        tk.Button(community_frame, text="Browse Discussions →",
                fg="#4a7c59", bg="#f3e5f5", font=("Arial", 10, "bold"),
                relief="flat", cursor="hand2",
                command=lambda: controller.show_frame("CommunityScreen")).pack(anchor="w", padx=10, pady=(0,5))

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

    def _stat_card(self, parent, title, subtitle, color, screen_name, controller):
        frame = tk.Frame(parent, bg=color, bd=2, relief="ridge", cursor="hand2")
        tk.Label(frame, text=title, font=("Arial", 11, "bold"),
                fg="#2c4a3a", bg=color).pack(anchor="w", padx=10, pady=(5,0))
        tk.Label(frame, text=subtitle, font=("Arial", 10),
                fg="#4e5d52", bg=color).pack(anchor="w", padx=10, pady=(0,5))
        if screen_name:
            frame.bind("<Button-1>", lambda e: controller.show_frame(screen_name))
        return frame



class PlantScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f9f9")

        # --- Bottom Navigation ---
        nav_frame = tk.Frame(self, bg="#e8f5e9", height=50)
        nav_frame.pack(side="bottom", fill="x")
        tk.Button(nav_frame, text="🏠 Home", bg="#c8e6c9",
                  command=lambda: controller.show_frame("HomeScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌿 Plant Detection", bg="#c8e6c9",
                  command=lambda: controller.show_frame("PlantScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌤 Weather", bg="#c8e6c9",
                  command=lambda: controller.show_frame("WeatherScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="👤 Profile", bg="#c8e6c9",
                  command=lambda: controller.show_frame("ProfileScreen")).pack(side="left", expand=True, fill="x")


        # --- Scrollable area ---
        canvas = tk.Canvas(self, bg="#f9f9f9", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Scroll with mouse
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # --- Header ---
        tk.Label(
            scrollable_frame,
            text="🌿 Crop Disease Detection",
            font=("Arial", 20, "bold"),
            fg="#2c4a3a",
            bg="#f9f9f9"
        ).pack(anchor="w", padx=15, pady=(10, 2))

        # Crop selection
        tk.Label(
            scrollable_frame,
            text="Select Crop:",
            font=("Arial", 12),
            fg="#2c4a3a",
            bg="#f9f9f9"
        ).pack(anchor="w", padx=15, pady=(5, 0))

        self.selected_crop = tk.StringVar(value="Select Crop")
        crop_dropdown = ttk.Combobox(
            scrollable_frame,
            textvariable=self.selected_crop,
            values=["Tomato", "Corn", "Potato", "Wheat"],
            state="readonly",
            font=("Arial", 11)
        )
        crop_dropdown.pack(fill="x", padx=15, pady=(0, 10))

        tk.Label(
            scrollable_frame,
            text="Take or upload a photo to check crop health",
            font=("Arial", 11),
            fg="#6b7c6f",
            bg="#f9f9f9"
        ).pack(anchor="w", padx=15, pady=(0, 10))

        # --- Image area ---
        self.image_frame = tk.Frame(scrollable_frame, bg="#e8f5e9", bd=2, relief="ridge")
        self.image_frame.pack(fill="x", padx=15, pady=5)
        self.image_label = tk.Label(self.image_frame, text="📷 No image captured", font=("Arial", 12), bg="#e8f5e9", height=15)
        self.image_label.pack(fill="both", expand=True)

        # --- Buttons ---
        self.capture_btn = tk.Button(
            scrollable_frame,
            text="📸 Capture / Upload Image",
            bg="#4a7c59", fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            relief="flat",
            command=self.upload_image
        )
        self.capture_btn.pack(fill="x", padx=15, pady=8)

        self.retake_btn = tk.Button(
            scrollable_frame,
            text="🔁 Retake Photo",
            bg="#fff",
            fg="#2c4a3a",
            font=("Arial", 12, "bold"),
            height=2,
            relief="groove",
            command=self.reset_screen
        )
        self.retake_btn.pack(fill="x", padx=15, pady=(0, 8))
        self.retake_btn.pack_forget()

        self.result_frame = None

        # --- Recent Scans section ---
        tk.Label(scrollable_frame, text="🕒 Recent Scans", font=("Arial", 14, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(anchor="w", padx=15, pady=(15, 5))

        self.recent_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        self.recent_frame.pack(fill="x", padx=15, pady=(0, 20))
        self._add_recent_scan("Corn", "Healthy", "Today")
        self._add_recent_scan("Tomato", "Leaf Spot", "Yesterday")
        self._add_recent_scan("Wheat", "Healthy", "3 days ago")

            # --- Upload Image ---
    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not path:
            return

        img = Image.open(path)
        self.img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.img_tk, text="")
        self.image_label.file_path = path

        self.capture_btn.pack_forget()
        self.retake_btn.pack(fill="x", padx=15, pady=8)
        self._simulate_analysis()

    # --- Simulate AI analysis ---
    def _simulate_analysis(self):
        self.overlay = tk.Label(self.image_frame, text="🔍 Analyzing...", bg="black", fg="white", font=("Arial", 14, "bold"))
        self.overlay.place(relx=0.5, rely=0.5, anchor="center")

        def analyze():
            # Get uploaded image path
            image_path = getattr(self.image_label, "file_path", None)
            if not image_path:
                return

            # Check crop selection
            crop_name = self.selected_crop.get()
            if crop_name == "Select Crop":
                messagebox.showerror("Error", "Please select a crop before analysis.")
                return

            # Pass both crop_name & image_path to predict_disease
            disease, confidence = predict_disease(image_path, crop_name)

            healthy = "healthy" in disease.lower()

            # Get treatment advice if not healthy
            treatment = []
            if not healthy:
                suggestion_text = get_treatment_recommendation(disease)
                treatment = suggestion_text.split("\n")

            self.overlay.destroy()

            self._show_result({
                "crop": crop_name,
                "healthy": healthy,
                "disease": None if healthy else disease,
                "confidence": confidence,
                "treatment": treatment
            })

        threading.Thread(target=analyze, daemon=True).start()

    # --- Display result card ---
    def _show_result(self, result):
        if self.result_frame:
            self.result_frame.destroy()

        self.result_frame = tk.Frame(self.image_frame, bg="#fff3f3" if not result["healthy"] else "#e8f5e9", bd=2, relief="ridge")
        self.result_frame.pack(fill="x", pady=10)

        status = "Healthy Crop 🌿" if result["healthy"] else "Disease Detected ⚠"
        color = "#2e7d32" if result["healthy"] else "#b71c1c"
        tk.Label(self.result_frame, text=status, fg=color, bg=self.result_frame["bg"], font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        tk.Label(self.result_frame, text=f"Crop: {result['crop']}", fg=color, bg=self.result_frame["bg"], font=("Arial", 11)).pack(anchor="w", padx=10)
        tk.Label(self.result_frame, text=f"Confidence: {result['confidence']}%", fg=color, bg=self.result_frame["bg"], font=("Arial", 10)).pack(anchor="w", padx=10, pady=(0, 5))

        if not result["healthy"]:
            tk.Label(self.result_frame, text=f"Disease: {result['disease']}", fg="#d32f2f", bg=self.result_frame["bg"], font=("Arial", 11, "bold")).pack(anchor="w", padx=10)
            tk.Label(self.result_frame, text="Treatment Recommendations:", fg="#4a7c59", bg=self.result_frame["bg"], font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            for i, step in enumerate(result["treatment"], start=1):
                tk.Label(self.result_frame, text=f"{i}. {step}", fg="#2c4a3a", bg=self.result_frame["bg"], font=("Arial", 10), wraplength=450, justify="left").pack(anchor="w", padx=20)

        tk.Button(
            self.result_frame,
            text="💾 Save Result",
            bg="#d4a373",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat"
        ).pack(fill="x", padx=10, pady=(10, 10))

    # --- Reset view for retake ---
    def reset_screen(self):
        self.image_label.config(image="", text="📷 No image captured")
        if self.result_frame:
            self.result_frame.destroy()
        self.capture_btn.pack(fill="x", padx=15, pady=8)
        self.retake_btn.pack_forget()

    # --- Recent Scans card ---
    def _add_recent_scan(self, crop, status, date):
        bg = "#e8f5e9" if status == "Healthy" else "#fff3e0"
        color = "#2e7d32" if status == "Healthy" else "#e65100"
        frame = tk.Frame(self.recent_frame, bg=bg, bd=2, relief="ridge")
        frame.pack(fill="x", pady=3)
        tk.Label(frame, text=crop, font=("Arial", 11, "bold"), fg="#2c4a3a", bg=bg).pack(anchor="w", padx=10)
        tk.Label(frame, text=date, font=("Arial", 9), fg="#6b7c6f", bg=bg).pack(anchor="w", padx=10)
        tk.Label(frame, text=status, font=("Arial", 10, "bold"), fg=color, bg=bg).pack(anchor="e", padx=10, pady=(0,5))


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

'''
class WeatherScreen(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#f5f3f0")
        self.controller = controller

        # --- Bottom Navigation ---
        nav_frame = tk.Frame(self, bg="#e8f5e9", height=50)
        nav_frame.pack(side="bottom", fill="x")
        tk.Button(nav_frame, text="🏠 Home", bg="#c8e6c9",
                  command=lambda: controller.show_frame("HomeScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌿 Plant Detection", bg="#c8e6c9",
                  command=lambda: controller.show_frame("PlantScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌤 Weather", bg="#c8e6c9",
                  command=lambda: controller.show_frame("WeatherScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="👤 Profile", bg="#c8e6c9",
                  command=lambda: controller.show_frame("ProfileScreen")).pack(side="left", expand=True, fill="x")

        # --- Scrollable Canvas ---
        canvas = tk.Canvas(self, bg="#f9f9f9", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # --- Dummy weather data ---
        self.forecast = [
            {"day": "Today", "temp": 28, "condition": "Sunny", "rain": 10},
            {"day": "Tomorrow", "temp": 26, "condition": "Partly Cloudy", "rain": 30},
            {"day": "Wednesday", "temp": 24, "condition": "Rainy", "rain": 80},
            {"day": "Thursday", "temp": 25, "condition": "Cloudy", "rain": 40},
            {"day": "Friday", "temp": 27, "condition": "Sunny", "rain": 5},
            {"day": "Saturday", "temp": 29, "condition": "Sunny", "rain": 5},
            {"day": "Sunday", "temp": 28, "condition": "Partly Cloudy", "rain": 20},
        ]

        total_rain = sum(day["rain"] for day in self.forecast)
        self.is_drought = total_rain < 100

        # --- Header ---
        tk.Label(scrollable_frame, text="Weather Forecast", font=("Arial", 22, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(pady=(15, 5))
        tk.Label(scrollable_frame, text="7-Day Forecast and Farming Recommendations",
                 font=("Arial", 12), fg="#6b7c6f", bg="#f9f9f9").pack(pady=(0, 10))

        # --- Current Weather Section ---
        self._create_card(scrollable_frame,
            title="Current Weather",
            data=[
                ("Temperature", "28°C"),
                ("Condition", "Sunny"),
                ("Humidity", "65%"),
                ("Wind", "12 km/h"),
                ("Rain Chance", "10%"),
            ],
            color="#d4c5b0"
        )

        # --- Drought Alert (if needed) ---
        if self.is_drought:
            self._create_alert(scrollable_frame,
                "⚠ Drought Warning",
                "Low rainfall is expected this week. Conserve water and monitor crops closely.",
                bg="#ffe6e6",
                border="#ffcccc",
                fg="#cc0000"
            )

        # --- Heavy Rain Alert ---
        self._create_alert(scrollable_frame,
            "⚠ Heavy Rain Alert",
            "Periods of heavy rainfall may occur mid-week. Secure loose soil and drainage areas.",
            bg="#fff2cc",
            border="#ffdd99",
            fg="#cc6600"
        )

        # --- 7-Day Forecast ---
        tk.Label(scrollable_frame, text="7-Day Forecast", font=("Arial", 14, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(pady=(15, 5))
        forecast_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        forecast_frame.pack(pady=5)
        for day in self.forecast:
            self._create_forecast_card(forecast_frame, day)

        # --- Recommendations ---
        self._create_recommendations(scrollable_frame)

    # -----------------------
    # Helper: Info Card
    # -----------------------
    def _create_card(self, parent, title, data, color):
        card = tk.Frame(parent, bg="white", highlightbackground=color, highlightthickness=2, padx=15, pady=10)
        card.pack(pady=10, fill="x", padx=20)
        tk.Label(card, text=title, font=("Arial", 14, "bold"), fg="#2c4a3a", bg="white").pack(anchor="w", pady=(0, 5))
        for label, value in data:
            row = tk.Frame(card, bg="white")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{label}:", font=("Arial", 11, "bold"), fg="#6b7c6f", bg="white").pack(side="left")
            tk.Label(row, text=value, font=("Arial", 11), fg="#2c4a3a", bg="white").pack(side="right")

    # -----------------------
    # Helper: Alert Card
    # -----------------------
    def _create_alert(self, parent, title, message, bg, border, fg):
        alert = tk.Frame(parent, bg=bg, highlightbackground=border, highlightthickness=2, padx=15, pady=10)
        alert.pack(pady=8, fill="x", padx=20)
        tk.Label(alert, text=title, font=("Arial", 13, "bold"), fg=fg, bg=bg).pack(anchor="w")
        tk.Label(alert, text=message, font=("Arial", 11), fg=fg, bg=bg, wraplength=400, justify="left").pack(anchor="w", pady=(3, 0))

    # -----------------------
    # Helper: Forecast Row
    # -----------------------
    def _create_forecast_card(self, parent, day):
        frame = tk.Frame(parent, bg="white", highlightbackground="#d4c5b0", highlightthickness=2, padx=10, pady=8)
        frame.pack(fill="x", padx=20, pady=4)
        tk.Label(frame, text=day["day"], font=("Arial", 11, "bold"), fg="#2c4a3a", bg="white").pack(side="left")
        tk.Label(frame, text=f"{day['temp']}°C", font=("Arial", 11), fg="#2c4a3a", bg="white").pack(side="left", padx=(15, 0))
        tk.Label(frame, text=day["condition"], font=("Arial", 10), fg="#6b7c6f", bg="white").pack(side="left", padx=10)
        tk.Label(frame, text=f"{day['rain']}% Rain", font=("Arial", 10), fg="#4a7c59", bg="white").pack(side="right")

    # -----------------------
    # Helper: Recommendations
    # -----------------------
    def _create_recommendations(self, parent):
        bg = "#fff7e6" if self.is_drought else "#eaffea"
        border = "#ffdd99" if self.is_drought else "#c5e1a5"
        card = tk.Frame(parent, bg=bg, highlightbackground=border, highlightthickness=2, padx=15, pady=10)
        card.pack(pady=15, fill="x", padx=20)

        tk.Label(card, text="Farming Recommendations", font=("Arial", 14, "bold"), fg="#2c4a3a", bg=bg).pack(anchor="w", pady=(0, 5))

        recommendations = []
        if self.is_drought:
            recommendations = [
                ("⚠", "Conserve water wherever possible."),
                ("⚠", "Reduce watering frequency to essential levels."),
                ("✓", "Apply mulch to retain soil moisture."),
            ]
        else:
            recommendations = [
                ("✓", "Maintain proper irrigation."),
                ("✓", "Apply fertilizers as scheduled."),
                ("⚠", "Delay new planting during rainfall."),
            ]

        for icon, text in recommendations:
            row = tk.Frame(card, bg=bg)
            row.pack(anchor="w", pady=2)
            tk.Label(row, text=icon, font=("Arial", 11, "bold"), fg="#2c4a3a", bg=bg, width=2).pack(side="left")
            tk.Label(row, text=text, font=("Arial", 11), fg="#2c4a3a", bg=bg, wraplength=400, justify="left").pack(side="left")
'''

class CommunityScreen(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#f5f3f0")
        self.controller = controller

        nav_frame = tk.Frame(self, bg="#e8f5e9", height=50)
        nav_frame.pack(side="bottom", fill="x")
        tk.Button(nav_frame, text="🏠 Home", bg="#c8e6c9",
                command=lambda: controller.show_frame("HomeScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌿 Plant Detection", bg="#c8e6c9",
                command=lambda: controller.show_frame("PlantScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="🌤 Weather", bg="#c8e6c9",
                command=lambda: controller.show_frame("WeatherScreen")).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="👤 Profile", bg="#c8e6c9",
                command=lambda: controller.show_frame("ProfileScreen")).pack(side="left", expand=True, fill="x")

        # Sample posts data
        self.posts = [
            {
                "id": 1,
                "author": "Marcus Brown",
                "avatar": "MB",
                "topic": "Best time to apply nitrogen fertilizer for corn?",
                "content": "I have 10 acres of corn and wondering when is the optimal time to apply nitrogen fertilizer...",
                "category": "Fertilizer",
                "likes": 24,
                "replies": [
                    {"author": "Sarah Johnson", "content": "Apply before light rain, heavy rain causes runoff.", "likes": 12},
                    {"author": "James Wilson", "content": "Split application works best.", "likes": 8},
                ],
            },
            {
                "id": 2,
                "author": "Lisa Chen",
                "avatar": "LC",
                "topic": "Dealing with fall armyworm infestation",
                "content": "My corn field is showing signs of armyworm damage. Any organic solutions?",
                "category": "Pest Control",
                "likes": 31,
                "replies": [],
            },
        ]

        self.expanded_post = None

        # Header
        tk.Label(self, text="👩🏾‍🌾 Community Forum", font=("Arial", 18, "bold"), bg="#f5f3f0", fg="#2c4a3a").pack(pady=10)
        tk.Label(self, text="Share tips and learn from fellow farmers", font=("Arial", 12), bg="#f5f3f0", fg="#6b7c6f").pack()

        # Search
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=self.search_var, width=50)
        search_entry.pack(pady=10)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_posts())

        # Categories
        self.categories = ["All", "Fertilizer", "Pest Control", "Irrigation", "Soil Health", "Market", "Weather"]
        self.selected_category = tk.StringVar(value="All")
        category_frame = tk.Frame(self, bg="#f5f3f0")
        category_frame.pack(pady=5)
        for cat in self.categories:
            btn = tk.Radiobutton(category_frame, text=cat, variable=self.selected_category, value=cat,
                                indicatoron=0, command=self.refresh_posts, width=12)
            btn.pack(side="left", padx=2)

        # Start new discussion button
        tk.Button(self, text="Start a Discussion", bg="#4a7c59", fg="white", width=20,
                command=self.create_new_post).pack(pady=10)

        # Posts frame (scrollable)
        canvas = tk.Canvas(self, bg="#f5f3f0")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.post_frame = tk.Frame(canvas, bg="#f5f3f0")
        self.post_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0,0), window=self.post_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_posts()

    def refresh_posts(self):
        # Clear current posts
        for widget in self.post_frame.winfo_children():
            widget.destroy()

        search = self.search_var.get().lower()
        selected_cat = self.selected_category.get()

        for post in self.posts:
            if search not in post["topic"].lower() and search not in post["content"].lower():
                continue
            if selected_cat != "All" and post["category"] != selected_cat:
                continue

            card = tk.Frame(self.post_frame, bg="white", bd=2, relief="groove")
            card.pack(fill="x", padx=10, pady=5)

            tk.Label(card, text=f"{post['author']} ({post['category']})", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", padx=5, pady=2)
            tk.Label(card, text=post["topic"], bg="white", font=("Arial", 11)).pack(anchor="w", padx=5)
            tk.Label(card, text=post["content"], bg="white", font=("Arial", 10), wraplength=450, justify="left").pack(anchor="w", padx=5, pady=2)

            action_frame = tk.Frame(card, bg="white")
            action_frame.pack(fill="x", padx=5, pady=5)
            tk.Button(action_frame, text=f"👍 {post['likes']}", command=lambda p=post: self.like_post(p)).pack(side="left")
            tk.Button(action_frame, text=f"💬 {len(post['replies'])} Replies", command=lambda p=post: self.toggle_replies(p)).pack(side="left", padx=5)

            # Replies
            if self.expanded_post == post["id"]:
                for reply in post["replies"]:
                    reply_frame = tk.Frame(card, bg="#f0f0f0", bd=1, relief="solid")
                    reply_frame.pack(fill="x", padx=10, pady=2)
                    tk.Label(reply_frame, text=f"{reply['author']}: {reply['content']} (👍 {reply['likes']})", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=5, pady=2)

                # Add reply input
                reply_var = tk.StringVar()
                tk.Entry(card, textvariable=reply_var, width=50).pack(side="left", padx=5)
                tk.Button(card, text="Post", command=lambda v=reply_var, p=post: self.post_reply(p, v)).pack(side="left", padx=2)

    def toggle_replies(self, post):
        self.expanded_post = None if self.expanded_post == post["id"] else post["id"]
        self.refresh_posts()

    def like_post(self, post):
        post["likes"] += 1
        self.refresh_posts()

    def post_reply(self, post, var):
        reply_text = var.get().strip()
        if reply_text:
            post["replies"].append({"author": "You", "content": reply_text, "likes": 0})
            var.set("")
            self.refresh_posts()

    def create_new_post(self):
        title = simpledialog.askstring("New Discussion", "Enter topic/question:")
        if not title:
            return
        content = simpledialog.askstring("New Discussion", "Enter description:")
        if not content:
            return
        category = simpledialog.askstring("New Discussion", f"Enter category ({', '.join(self.categories[1:])}):")
        if not category:
            category = "Other"

        self.posts.append({
            "id": len(self.posts) + 1,
            "author": "You",
            "avatar": "Y",
            "topic": title,
            "content": content,
            "category": category,
            "likes": 0,
            "replies": [],
        })
        self.refresh_posts()
        messagebox.showinfo("Success", "Discussion posted!")
'''
class AlertsScreen(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#f5f3f0")
        self.alerts = AlertsScreen
        self.controller = controller

        def create_ui(self):
            tk.Label(self, text="🚨 Alerts", font=("Arial", 22, "bold"), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(15, 5))
            tk.Label(self, text="Stay updated with the latest farming alerts", font=("Arial", 12), fg="#6b7c6f", bg="#f5f3f0").pack(pady=(0, 10))

            notif_frame = tk.Frame(self, bg="#f5f3f0")
            notif_frame.pack(fill="both", expand=True, padx=15, pady=10)

            tk.Label(notif_frame, text="Notifications", font=("Arial", 14, "bold"), bg="#f5f3f0", fg="#2c4a3a").pack(anchor="w", pady=(0, 5))

            self.create_switch(notif_frame, "Severe Weather Alerts", True)
            self.create_switch(notif_frame, "Pest Outbreak Notifications", True)
            self.create_switch(notif_frame, "Market Price Alerts", False)

            alerts_frame = tk.Frame(self, bg="#f5f3f0")
            alerts_frame.pack(fill="both", expand=True, padx=15, pady=10)

            top_frame = tk.Frame(alerts_frame, bg="#f5f3f0")
            top_frame.pack(fill="x")
            tk.Label(top_frame, text="Recent Alerts", font=("Arial", 14, "bold"), bg="#f5f3f0", fg="#2c4a3a").pack(side="left", pady=(0, 5))
            tk.Button(top_frame, text="Mark All as Read", bg="#4a7c59", fg="white", command=self.mark_all_read).pack(side="right")
            self.alerts_list_frame = tk.Frame(alerts_frame, bg="#f5f3f0")
            self.alerts_list_frame.pack(fill="both", expand=True)
            self.refresh_alerts()
'''
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

# --- Run standalone window for testing ---
if __name__ == "__main__":
    app = JamaAlca()
    app.mainloop()
#    root.mainloop()