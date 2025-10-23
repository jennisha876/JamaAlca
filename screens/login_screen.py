import tkinter as tk
from tkinter import messagebox, ttk

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f3f0")
        self.controller = controller

        tk.Label(self, text="JamaAlca Farming App", font=("Arial", 24, "bold"), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(50, 10))
        tk.Label(self, text="Please log in to continue", font=("Arial", 12), fg="#6b7c6f", bg="#f5f3f0").pack(pady=(0, 20))

        # --- Phone Login ---
        self.phone_frame = tk.Frame(self, bg="#f5f3f0")
        self.phone_frame.pack(pady=10)

        tk.Label(self.phone_frame, text="Enter Phone Number:", bg="#f5f3f0", font=("Arial",12)).pack(pady=(0,5))
        self.phone_entry = tk.Entry(self.phone_frame, font=("Arial",12), bg="white", relief="solid", bd=1)
        self.phone_entry.pack(pady=(0,10), ipadx=50, ipady=5)

        tk.Button(self.phone_frame, text="Login with Phone Number", width=30, height=2,
                bg="#4a7c59", fg="white", font=("Arial",12,"bold"), command=self.phone_login).pack(pady=10)

        tk.Button(self.phone_frame, text="Continue as Guest / Sign Up", width=30, height=2,
                bg="#d4a373", fg="white", font=("Arial",12,"bold"), command=self.show_signup_form).pack(pady=10)

        # --- Signup Form ---
        self.signup_frame = tk.Frame(self, bg="#f5f3f0")
        tk.Label(self.signup_frame, text="Sign Up", font=("Arial", 20, "bold"), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(20, 10))

        tk.Label(self.signup_frame, text="Username:", font=("Arial",12), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(10,5))
        self.username_entry = tk.Entry(self.signup_frame, font=("Arial",12), bg="white", relief="solid", bd=1)
        self.username_entry.pack(pady=(0,10), ipadx=50, ipady=5)

        tk.Label(self.signup_frame, text="Password:", font=("Arial",12), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(10,5))
        self.password_entry = tk.Entry(self.signup_frame, show="*", font=("Arial",12), bg="white", relief="solid", bd=1)
        self.password_entry.pack(pady=(0,10), ipadx=50, ipady=5)

        tk.Label(self.signup_frame, text="Location:", font=("Arial",12), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(10,5))
        self.location_entry = tk.Entry(self.signup_frame, font=("Arial",12), bg="white", relief="solid", bd=1)
        self.location_entry.pack(pady=(0,10), ipadx=50, ipady=5)

        tk.Label(self.signup_frame, text="Farm Size:", font=("Arial",12), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(10,5))
        self.farm_size_entry = tk.Entry(self.signup_frame, font=("Arial",12), bg="white", relief="solid", bd=1)
        self.farm_size_entry.pack(pady=(0,10), ipadx=50, ipady=5)

        tk.Label(self.signup_frame, text="Main Crop:", font=("Arial",12), fg="#2c4a3a", bg="#f5f3f0").pack(pady=(10,5))
        self.crop_entry = tk.Entry(self.signup_frame, font=("Arial",12), bg="white", relief="solid", bd=1)
        self.crop_entry.pack(pady=(0,10), ipadx=50, ipady=5)

        tk.Button(self.signup_frame, text="Sign Up", bg="#4a7c59", fg="white", font=("Arial",12,"bold"),
                command=self.signup).pack(pady=(10,20), ipadx=20, ipady=5)

    def phone_login(self):
        phone_number = self.phone_entry.get()
        if phone_number:
            messagebox.showinfo("Login Success", f"Phone: {phone_number}")
            self.controller.show_frame("HomeScreen")
        else:
            messagebox.showerror("Login Failed", "Please enter your phone number.")

    def show_signup_form(self):
        self.phone_frame.pack_forget()
        self.signup_frame.pack(pady=10)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        location = self.location_entry.get()
        farm_size = self.farm_size_entry.get()
        crop = self.crop_entry.get()
        if username and password and location and farm_size and crop:
            messagebox.showinfo("Signup Success", f"Welcome, {username}!")
            self.controller.show_frame("HomeScreen")
        else:
            messagebox.showerror("Signup Failed", "Please fill in all fields.")