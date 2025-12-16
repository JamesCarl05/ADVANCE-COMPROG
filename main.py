# main.py
import tkinter as tk
from gui import welcome_screen
from database import init_db

def main():
    init_db()

    root = tk.Tk()
    root.title("Clean Impact for the Waves")
    root.geometry("1200x700")
    root.resizable(True, True)

    # ============================
    #     FULLSCREEN SHORTCUTS
    # ============================

    # Toggle fullscreen with F11
    def toggle_fullscreen(event=None):
        is_full = root.attributes("-fullscreen")
        root.attributes("-fullscreen", not is_full)

    # Escape exits fullscreen
    def end_fullscreen(event=None):
        root.attributes("-fullscreen", False)

    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", end_fullscreen)

    # Load welcome screen
    welcome_screen(root)

    root.mainloop()

if __name__ == "__main__":
    main()
