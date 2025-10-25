"""
Plant Disease Detection Screen
This screen lets farmers take photos of their plants and get AI-powered disease detection
Think of this as a smart doctor for plants - you show it a photo and it tells you what's wrong
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from PIL import Image, ImageTk
from services.predict_disease import predict_disease
from services.treatment_recommendation import get_treatment_recommendation
from services.weather_fetcher import WeatherFetcher
from services.data_service import DataService

class PlantScreen(tk.Frame):
    """
    Plant Disease Detection Screen
    This is where farmers can check if their plants are healthy or sick
    It's like having a plant doctor in your pocket - just take a photo and get advice
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f9f9")
        # Set up the data service to track what the farmer is doing
        self.data_service = DataService()

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

    def upload_image(self):
        """
        Let the farmer choose a photo from their computer
        This is like opening a photo album and picking which picture to show the doctor
        """
        # Ask the farmer to pick a photo file from their computer
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not path:
            return  # They didn't pick anything, so we stop here

        # Load the photo and show it on the screen
        img = Image.open(path)
        self.img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.img_tk, text="")
        self.image_label.file_path = path  # Remember where the photo is stored

        # Hide the "take photo" button and show the "retake" button instead
        self.capture_btn.pack_forget()
        self.retake_btn.pack(fill="x", padx=15, pady=8)
        
        # Start analyzing the photo to see if there are any diseases
        self._simulate_analysis()

    def _simulate_analysis(self):
        """
        Start analyzing the plant photo to detect diseases
        This is like sending the photo to a plant doctor and waiting for their diagnosis
        """
        # Show a "thinking" message while the AI is working
        self.overlay = tk.Label(self.image_frame, text="🔍 Analyzing...", bg="black", fg="white", font=("Arial", 14, "bold"))
        self.overlay.place(relx=0.5, rely=0.5, anchor="center")

        def analyze():
            """
            This function runs in the background so the app doesn't freeze
            It's like having a separate worker do the hard work while you wait
            """
            try:
                # Get the photo that the farmer selected
                image_path = getattr(self.image_label, "file_path", None)
                if not image_path:
                    self.after(0, lambda: self._show_error("No image selected"))
                    return

                # Make sure they picked what type of plant it is
                crop_name = self.selected_crop.get()
                if crop_name == "Select Crop":
                    self.after(0, lambda: messagebox.showerror("Error", "Please select a crop before analysis."))
                    return

                # Send the photo to the AI to see if there are any diseases
                disease, confidence = predict_disease(image_path, crop_name)
                healthy = "healthy" in disease.lower()

                # If there's a disease, get advice on how to fix it
                treatment = []
                if not healthy:
                    suggestion_text = get_treatment_recommendation(disease)
                    treatment = suggestion_text.split("\n")

                # Remember that the farmer checked their plants today
                self.data_service.update_scan_data(crop_name, not healthy)
                
                # Show the results to the farmer
                self.after(0, lambda: self._show_result({
                    "crop": crop_name,
                    "healthy": healthy,
                    "disease": None if healthy else disease,
                    "confidence": confidence,
                    "treatment": treatment
                }))
                
            except Exception as e:
                # If something goes wrong, show an error message
                self.after(0, lambda: self._show_error(f"Analysis failed: {str(e)}"))

        # Start the analysis in a separate thread so the app doesn't freeze
        threading.Thread(target=analyze, daemon=True).start()

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

    def _show_error(self, error_message):
        """Show error message in the UI"""
        if self.overlay:
            self.overlay.destroy()
        
        if self.result_frame:
            self.result_frame.destroy()

        self.result_frame = tk.Frame(self.image_frame, bg="#ffebee", bd=2, relief="ridge")
        self.result_frame.pack(fill="x", pady=10)
        
        tk.Label(self.result_frame, text="❌ Analysis Error", fg="#c62828", bg="#ffebee", font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        tk.Label(self.result_frame, text=error_message, fg="#d32f2f", bg="#ffebee", font=("Arial", 10), wraplength=450, justify="left").pack(anchor="w", padx=10, pady=(0, 5))

    def reset_screen(self):
        self.image_label.config(image="", text="📷 No image captured")
        if self.result_frame:
            self.result_frame.destroy()
        self.capture_btn.pack(fill="x", padx=15, pady=8)
        self.retake_btn.pack_forget()

    def _add_recent_scan(self, crop, status, date):
        bg = "#e8f5e9" if status == "Healthy" else "#fff3e0"
        color = "#2e7d32" if status == "Healthy" else "#e65100"
        frame = tk.Frame(self.recent_frame, bg=bg, bd=2, relief="ridge")
        frame.pack(fill="x", pady=3)
        tk.Label(frame, text=crop, font=("Arial", 11, "bold"), fg="#2c4a3a", bg=bg).pack(anchor="w", padx=10)
        tk.Label(frame, text=date, font=("Arial", 9), fg="#6b7c6f", bg=bg).pack(anchor="w", padx=10)
        tk.Label(frame, text=status, font=("Arial", 10, "bold"), fg=color, bg=bg).pack(anchor="e", padx=10, pady=(0,5))