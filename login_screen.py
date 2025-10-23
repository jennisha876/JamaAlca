import tkinter as tk
from tkinter import messagebox

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f3f0")
        self.controller = controller
        
        # Create centered login form
        form_frame = tk.Frame(self, bg="#f5f3f0", padx=40, pady=40)
        form_frame.place(relx=0.5, rely=0.4, anchor="center")
        
        # Logo/Title
        tk.Label(form_frame, text="JamaAlca", font=("Arial", 24, "bold"), 
                fg="#2c4a3a", bg="#f5f3f0").pack(pady=(0, 20))
        
        # Username
        tk.Label(form_frame, text="Username", font=("Arial", 12), 
                fg="#2c4a3a", bg="#f5f3f0").pack(anchor="w")
        self.username = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.username.pack(pady=(0, 15))
        
        # Password
        tk.Label(form_frame, text="Password", font=("Arial", 12), 
                fg="#2c4a3a", bg="#f5f3f0").pack(anchor="w")
        self.password = tk.Entry(form_frame, font=("Arial", 12), width=30, show="•")
        self.password.pack(pady=(0, 20))
        
        # Login Button
        tk.Button(form_frame, text="Login", font=("Arial", 12, "bold"), 
                 bg="#4a7c59", fg="white", width=20,
                 command=self.login).pack(pady=(0, 10))
        
        # Register Link
        tk.Label(form_frame, text="New to JamaAlca? Register here", 
                font=("Arial", 10), fg="#4a7c59", bg="#f5f3f0",
                cursor="hand2").pack()

    def login(self):
        # For demo purposes, accept any non-empty username/password
        if self.username.get().strip() and self.password.get().strip():
            self.controller.show_frame("HomeScreen")
        else:
            messagebox.showerror("Error", "Please enter username and password")