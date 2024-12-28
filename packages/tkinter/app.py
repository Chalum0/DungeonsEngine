import tkinter as tk
import threading
import time

# Function to run tkinter app
def run_tkinter_app(data):
    root = tk.Tk()
    root.title("Live Information")
    root.geometry("300x200")

    label = tk.Label(root, text="Loading...", font=("Helvetica", 10), anchor='w', justify='left')
    label.pack(pady=20, fill='x', padx=10)

    def update_label():
        # Keep updating the label with shared data
        while True:
            label.config(text=f'FPS: {data['fps']}\nx: {data['coords'][0]}\ny: {data['coords'][1]}\nz: {data['coords'][2]}\nyaw: {data["yaw"]}\npitch: {data["pitch"]}\n')
            time.sleep(0.1)

    threading.Thread(target=update_label, daemon=True).start()

    root.mainloop()

# Main application
def debug_app(data):
    # Start tkinter thread
    tkinter_thread = threading.Thread(target=run_tkinter_app, args=(data,), daemon=True)
    tkinter_thread.start()

