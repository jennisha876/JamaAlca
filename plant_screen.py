import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from PIL import Image, ImageTk
from predict_disease import predict_disease
from treatment_recommendation import get_treatment_recommendation


class PlantScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f9f9")
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
        tk.Label(scrollable_frame, text="🌿 Crop Disease Detection", font=("Arial", 20, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(anchor="w", padx=15, pady=(10, 2))

        # Crop selection
        tk.Label(scrollable_frame, text="Select Crop:", font=("Arial", 12), fg="#2c4a3a", bg="#f9f9f9").pack(anchor="w", padx=15, pady=(5, 0))

        self.selected_crop = tk.StringVar(value="Select Crop")
        crop_dropdown = ttk.Combobox(scrollable_frame, textvariable=self.selected_crop, values=["Tomato", "Corn", "Potato", "Wheat"], state="readonly", font=("Arial", 11))
        crop_dropdown.pack(fill="x", padx=15, pady=(0, 10))

        tk.Label(scrollable_frame, text="Take or upload a photo to check crop health", font=("Arial", 11), fg="#6b7c6f", bg="#f9f9f9").pack(anchor="w", padx=15, pady=(0, 10))

        # --- Image area ---
        self.image_frame = tk.Frame(scrollable_frame, bg="#e8f5e9", bd=2, relief="ridge")
        self.image_frame.pack(fill="x", padx=15, pady=5)
        self.image_label = tk.Label(self.image_frame, text="📷 No image captured", font=("Arial", 12), bg="#e8f5e9")
        self.image_label.pack(fill="both", expand=True)

        # --- Buttons ---
        self.capture_btn = tk.Button(scrollable_frame, text="📸 Capture / Upload Image", bg="#4a7c59", fg="white", font=("Arial", 12, "bold"), height=2, relief="flat", command=self.upload_image)
        self.capture_btn.pack(fill="x", padx=15, pady=8)

        self.retake_btn = tk.Button(scrollable_frame, text="🔁 Retake Photo", bg="#fff", fg="#2c4a3a", font=("Arial", 12, "bold"), height=2, relief="groove", command=self.reset_screen)
        self.retake_btn.pack(fill="x", padx=15, pady=(0, 8))
        self.retake_btn.pack_forget()

        self.result_frame = None

        # --- Recent Scans section ---
        tk.Label(scrollable_frame, text="🕒 Recent Scans", font=("Arial", 14, "bold"), fg="#2c4a3a", bg="#f9f9f9").pack(anchor="w", padx=15, pady=(15, 5))

        self.recent_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
        self.recent_frame.pack(fill="x", padx=15, pady=(0, 20))
        # recent scans will be populated from controller.recent_scans when returning to Home

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

    def _simulate_analysis(self):
        self.overlay = tk.Label(self.image_frame, text="🔍 Analyzing...", bg="black", fg="white", font=("Arial", 14, "bold"))
        self.overlay.place(relx=0.5, rely=0.5, anchor="center")

        def analyze():
            image_path = getattr(self.image_label, "file_path", None)
            if not image_path:
                return

            crop_name = self.selected_crop.get()
            if crop_name == "Select Crop":
                messagebox.showerror("Error", "Please select a crop before analysis.")
                return

            disease, confidence = predict_disease(image_path, crop_name)

            healthy = "healthy" in disease.lower()

            treatment = []
            if not healthy:
                suggestion_text = get_treatment_recommendation(disease)
                treatment = suggestion_text.split("\n")

            try:
                saved = self.controller.scan_store.save_scan(
                    image_path=image_path,
                    crop=crop_name,
                    disease=(disease if not healthy else "Healthy"),
                    confidence=confidence,
                    treatment_text="\n".join(treatment),
                    user_id=getattr(self.controller, "user_id", 0)
                )
                # add to controller's recent scans list
                try:
                    controller_recent = getattr(self.controller, "recent_scans", None)
                    if controller_recent is not None:
                        controller_recent.append(saved)
                    # notify other screens to refresh
                    try:
                        if hasattr(self.controller, "trigger_refresh"):
                            self.controller.trigger_refresh()
                    except Exception:
                        pass
                except Exception:
                    pass
            except Exception as e:
                print("[Scan Save Error]", e)

            self.overlay.destroy()

            self._show_result({
                "crop": crop_name,
                "healthy": healthy,
                "disease": None if healthy else disease,
                "confidence": confidence,
                "treatment": treatment
            })

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
            # sanitize disease/treatment display: remove markdown backticks and trim
            disease_text = str(result.get("disease", "")).strip().replace("```", "")
            tk.Label(self.result_frame, text=f"Disease: {disease_text}", fg="#d32f2f", bg=self.result_frame["bg"], font=("Arial", 11, "bold")).pack(anchor="w", padx=10)
            tk.Label(self.result_frame, text="Treatment Recommendations:", fg="#4a7c59", bg=self.result_frame["bg"], font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            # split recommendations into clean lines and display
            for i, step in enumerate(result.get("treatment", []), start=1):
                step_text = str(step).strip().replace("```", "")
                # remove leading markdown bullets if present
                if step_text.startswith("- ") or step_text.startswith("* "):
                    step_text = step_text[2:].strip()
                tk.Label(self.result_frame, text=f"{i}. {step_text}", fg="#2c4a3a", bg=self.result_frame["bg"], font=("Arial", 10), wraplength=450, justify="left").pack(anchor="w", padx=20)

        tk.Button(self.result_frame, text="💾 Save Result", bg="#d4a373", fg="white", font=("Arial", 11, "bold"), relief="flat").pack(fill="x", padx=10, pady=(10, 10))

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
