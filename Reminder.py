import tkinter as tk
from threading import Thread
import time

# --- SETTINGS ---
MESSAGE = "Take a break"
INTERVAL = 1  # minutes
interval_seconds = INTERVAL * 60

# --- GLOBAL STATE ---
window_open = False
next_notification = 0

# --- FUNCTION TO SHOW REMINDER WINDOW ---
def show_notification():
    global window_open, next_notification, interval_seconds

    if window_open:
        return

    window_open = True
    win = tk.Tk()
    win.title("Reminder")
    win.geometry("350x150+1000+600")
    win.attributes("-topmost", True)

    # Remove window icon (optional)
    try:
        win.iconbitmap(default="")
    except Exception:
        pass

    # Message
    label = tk.Label(win, text=MESSAGE, font=("Arial", 14))
    label.pack(pady=10)

    # Interval input
    tk.Label(win, text="Interval (minutes):").pack()
    interval_entry = tk.Entry(win)
    interval_entry.pack()
    interval_entry.insert(0, str(interval_seconds // 60))

    # Handle window close (titlebar X)
    def on_close():
        global window_open, next_notification, interval_seconds
        try:
            new_interval = float(interval_entry.get())
            if new_interval > 0:
                interval_seconds = new_interval * 60
        except ValueError:
            pass
        window_open = False
        next_notification = time.time() + interval_seconds
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)  # catch titlebar close


    win.mainloop()

# --- BACKGROUND LOOP ---
def notification_loop():
    global next_notification
    next_notification = time.time()
    while True:
        if time.time() >= next_notification:
            show_notification()
        time.sleep(1)

# --- START BACKGROUND THREAD ---
thread = Thread(target=notification_loop, daemon=True)
thread.start()

# --- KEEP MAIN THREAD ALIVE ---
while True:
    time.sleep(1)
