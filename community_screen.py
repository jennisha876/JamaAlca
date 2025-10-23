import tkinter as tk
from tkinter import simpledialog, messagebox

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
