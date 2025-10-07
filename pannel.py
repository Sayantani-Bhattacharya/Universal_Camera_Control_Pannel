import tkinter as tk
from tkinter import ttk
import subprocess
import json

# File to save and load parameters
PARAMS_FILE = "camera_params.json"
# The port where USB device is connected.
DEVICE = "/dev/video4"



# Dictionary to store slider widgets for easy access
sliders = {}






def run_cmd(cmd):
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def set_control(name, value):
    """Send v4l2-ctl command to set a camera parameter."""
    try:
        val = int(float(value)) # Convert safely: "32.0" → 32
        run_cmd(["v4l2-ctl", "-d", DEVICE, f"--set-ctrl={name}={val}"])
    except Exception as e:
        print(f"Error setting {name}: {e}")

def save_parameters():
    """Save current parameter values to a file."""
    params = {}
    for ctrl, (_, _, default) in controls.items():
        params[ctrl] = sliders[ctrl].get()  # Get the current value from the slider
    try:
        with open(PARAMS_FILE, "w") as f:
            json.dump(params, f)
        print("Parameters saved successfully.")
    except Exception as e:
        print(f"Error saving parameters: {e}")

def load_parameters():
    """Load parameter values from a file and update sliders."""
    try:
        with open(PARAMS_FILE, "r") as f:
            params = json.load(f)
        for ctrl, value in params.items():
            if ctrl in controls:
                set_control(ctrl, value)  # Update the camera control
                sliders[ctrl].set(value)  # Update the slider value
        print("Parameters loaded successfully.")
    except Exception as e:
        print(f"Error loading parameters: {e}")

def toggle_auto_exposure():
    run_cmd(["v4l2-ctl", "-d", DEVICE, "--set-ctrl=auto_exposure=1"])  # manual

def toggle_white_balance():
    run_cmd(["v4l2-ctl", "-d", DEVICE, "--set-ctrl=white_balance_automatic=0"])  # manual

root = tk.Tk()
root.title("Camera Control Panel")

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

# Buttons to enable manual control
ttk.Button(root, text="Enable Manual Exposure", command=toggle_auto_exposure).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(root, text="Enable Manual White Balance", command=toggle_white_balance).grid(row=0, column=1, padx=10, pady=5)

# Add sliders for each control
for idx, (ctrl, (minv, maxv, default)) in enumerate(controls.items(), start=1):
    ttk.Label(root, text=ctrl).grid(row=idx, column=0, sticky="w", padx=10)
    slider = ttk.Scale(
        root, from_=minv, to=maxv, orient="horizontal",
        command=lambda val, name=ctrl: set_control(name, val)
    )
    slider.set(default)
    slider.grid(row=idx, column=1, padx=10, pady=4, sticky="ew")
    sliders[ctrl] = slider  # Store slider in the dictionary

ttk.Button(root, text="Save Parameters", command=save_parameters).grid(row=len(controls) + 1, column=0, padx=10, pady=5)
ttk.Button(root, text="Load Parameters", command=load_parameters).grid(row=len(controls) + 1, column=1, padx=10, pady=5)


root.columnconfigure(1, weight=1)
root.mainloop()
