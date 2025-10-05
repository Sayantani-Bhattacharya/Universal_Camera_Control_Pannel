import tkinter as tk
from tkinter import ttk
import subprocess

DEVICE = "/dev/video4"

# Define camera controls (name: (min, max, default))
controls = {
    "brightness": (-64, 64, 0),
    "contrast": (0, 64, 32),
    "saturation": (0, 128, 56),
    "hue": (-40, 40, 0),
    "gamma": (72, 500, 100),
    "gain": (0, 100, 0),
    "sharpness": (0, 6, 3),
    "backlight_compensation": (0, 2, 1),
    "white_balance_temperature": (2800, 6500, 4600),
    "exposure_time_absolute": (1, 5000, 156),
}

def set_control(name, value):
    """Send v4l2-ctl command to set a camera parameter."""
    try:
        val = int(float(value))  # ✅ convert safely: "32.0" → 32
        cmd = ["v4l2-ctl", "-d", DEVICE, f"--set-ctrl={name}={val}"]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Error setting {name}: {e}")

root = tk.Tk()
root.title("Camera Control Panel")

for idx, (ctrl, (minv, maxv, default)) in enumerate(controls.items()):
    ttk.Label(root, text=ctrl).grid(row=idx, column=0, sticky="w", padx=10)
    slider = ttk.Scale(
        root, from_=minv, to=maxv, orient="horizontal",
        command=lambda val, name=ctrl: set_control(name, val)
    )
    slider.set(default)
    slider.grid(row=idx, column=1, padx=10, pady=4, sticky="ew")

root.columnconfigure(1, weight=1)
root.mainloop()
