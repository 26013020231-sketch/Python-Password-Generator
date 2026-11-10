"""
Password Generator - Python Minor Project
GUI: Tkinter | Theme: Dark Professional

Run:
    python password_generator.py
"""

import tkinter as tk
from tkinter import messagebox
import secrets
import string


BG = "#111827"
PANEL = "#1f2937"
INPUT = "#0b1220"
TEXT = "#f9fafb"
MUTED = "#9ca3af"
ACCENT = "#38bdf8"
GREEN = "#34d399"
RED = "#fb7185"


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("600x590")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.root, text="PASSWORD GENERATOR",
            font=("Segoe UI", 22, "bold"), bg=BG, fg=TEXT
        ).pack(pady=(25, 5))

        tk.Label(
            self.root, text="Create a strong, random password in seconds",
            font=("Segoe UI", 10), bg=BG, fg=MUTED
        ).pack(pady=(0, 20))

        panel = tk.Frame(self.root, bg=PANEL, padx=25, pady=22)
        panel.pack(padx=28, fill="both")

        tk.Label(panel, text="PASSWORD LENGTH", font=("Segoe UI", 10, "bold"),
                 bg=PANEL, fg=TEXT).pack(anchor="w")

        length_row = tk.Frame(panel, bg=PANEL)
        length_row.pack(fill="x", pady=(8, 18))
        self.length_value = tk.Label(length_row, text="16", font=("Segoe UI", 12, "bold"),
                                      bg=PANEL, fg=ACCENT, width=4)
        self.length_value.pack(side="right")
        length_scale = tk.Scale(
            length_row, from_=4, to=64, orient="horizontal",
            variable=self.length_var, command=self.update_length,
            bg=PANEL, fg=TEXT, troughcolor=INPUT, highlightthickness=0,
            activebackground=ACCENT, showvalue=False, length=420
        )
        length_scale.pack(side="left")

        tk.Label(panel, text="INCLUDE CHARACTERS", font=("Segoe UI", 10, "bold"),
                 bg=PANEL, fg=TEXT).pack(anchor="w", pady=(0, 8))

        options = tk.Frame(panel, bg=PANEL)
        options.pack(fill="x")
        self.add_check(options, "Uppercase letters (A-Z)", self.upper_var, 0, 0)
        self.add_check(options, "Lowercase letters (a-z)", self.lower_var, 0, 1)
        self.add_check(options, "Numbers (0-9)", self.digits_var, 1, 0)
        self.add_check(options, "Symbols (!@#$...)", self.symbols_var, 1, 1)

        tk.Button(
            panel, text="GENERATE PASSWORD", command=self.generate_password,
            font=("Segoe UI", 11, "bold"), bg=ACCENT, fg="#082f49",
            activebackground="#7dd3fc", activeforeground="#082f49",
            relief="flat", cursor="hand2", pady=11
        ).pack(fill="x", pady=(22, 0))

        result_panel = tk.Frame(self.root, bg=PANEL, padx=25, pady=18)
        result_panel.pack(padx=28, pady=18, fill="x")

        tk.Label(result_panel, text="YOUR PASSWORD", font=("Segoe UI", 9, "bold"),
                 bg=PANEL, fg=MUTED).pack(anchor="w")

        result_row = tk.Frame(result_panel, bg=INPUT, padx=10, pady=10)
        result_row.pack(fill="x", pady=8)
        self.password_entry = tk.Entry(
            result_row, font=("Consolas", 13), bg=INPUT, fg=TEXT,
            insertbackground=TEXT, relief="flat", bd=0
        )
        self.password_entry.pack(side="left", fill="x", expand=True)
        tk.Button(
            result_row, text="COPY", command=self.copy_password,
            font=("Segoe UI", 9, "bold"), bg=GREEN, fg="#052e24",
            relief="flat", cursor="hand2", padx=12, pady=6
        ).pack(side="right")

        self.status_label = tk.Label(
            result_panel, text="Choose your settings and generate a password.",
            font=("Segoe UI", 9), bg=PANEL, fg=MUTED
        )
        self.status_label.pack(anchor="w")

        tk.Label(
            self.root, text="Tip: Use a unique password for every account.",
            font=("Segoe UI", 9), bg=BG, fg=MUTED
        ).pack(pady=(2, 0))

    def add_check(self, parent, label, variable, row, column):
        cb = tk.Checkbutton(
            parent, text=label, variable=variable, bg=PANEL, fg=TEXT,
            activebackground=PANEL, activeforeground=TEXT,
            selectcolor=INPUT, font=("Segoe UI", 9), padx=0
        )
        cb.grid(row=row, column=column, sticky="w", padx=(0, 12), pady=5)

    def update_length(self, value):
        self.length_value.config(text=str(int(float(value))))

    def generate_password(self):
        groups = []
        if self.upper_var.get():
            groups.append(string.ascii_uppercase)
        if self.lower_var.get():
            groups.append(string.ascii_lowercase)
        if self.digits_var.get():
            groups.append(string.digits)
        if self.symbols_var.get():
            groups.append("!@#$%^&*()-_=+[]{};:,.?/")

        length = self.length_var.get()
        if not groups:
            messagebox.showwarning("Select an option",
                                   "Please select at least one character type.")
            return
        if length < len(groups):
            messagebox.showwarning(
                "Password length too short",
                "Increase the length so each selected character type can be included."
            )
            return

        # Ensure at least one character from every selected group.
        password_chars = [secrets.choice(group) for group in groups]
        all_chars = "".join(groups)
        password_chars.extend(secrets.choice(all_chars)
                              for _ in range(length - len(password_chars)))
        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.status_label.config(
            text=f"Generated successfully • {length} characters",
            fg=GREEN
        )

    def copy_password(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.status_label.config(text="Password copied to clipboard.", fg=GREEN)


if __name__ == "__main__":
    window = tk.Tk()
    app = PasswordGeneratorApp(window)
    window.mainloop()
