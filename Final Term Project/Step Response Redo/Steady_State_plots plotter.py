
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Directory containing your CSV files (change if needed)
DATA_DIR = "."

# Effort values represented in the filenames
efforts = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

def load_motor_data(prefix, efforts):
    """
    Load CSVs for one motor.

    prefix: 'left_motor' or 'right_motor'
    returns: dict[effort] -> DataFrame
    """
    data = {}
    for effort in efforts:
        filename = f"{prefix}_{effort}.csv"
        filepath = os.path.join(DATA_DIR, filename)

        if not os.path.exists(filepath):
            print(f"WARNING: {filepath} not found, skipping.")
            continue

        df = pd.read_csv(filepath)
        df = df.iloc[:, :2]                  # first col = time, second = velocity
        df.columns = ["time_us", "velocity_counts_s"]
        df["time_s"] = df["time_us"] * 1e-6  # convert to seconds if useful

        data[effort] = df

    return data

def compute_steady_state_speed(df, frac_tail=0.25):
    """Return mean velocity of the last fraction of samples."""
    n = len(df)
    if n == 0:
        return float("nan")
    start = int((1.0 - frac_tail) * n)
    return df["velocity_counts_s"].iloc[start:].mean()

def extract_stable_speeds(data):
    """Compute steady-state speeds for all efforts."""
    return {effort: compute_steady_state_speed(df) for effort, df in data.items()}

def plot_curve_with_fit(speeds, title):
    """
    Plot steady-state speed vs effort, fit a line, show slope on graph.
    """
    efforts_sorted = np.array(sorted(speeds.keys()))
    speeds_sorted = np.array([speeds[e] for e in efforts_sorted])

    # Best-fit line: speed = m * effort + b
    m, b = np.polyfit(efforts_sorted, speeds_sorted, 1)
    fit_line = m * efforts_sorted + b

    # Print slope
    print(f"{title} — Best-fit slope: {m:.3f} counts/s per % effort")

    # Plot
    plt.figure()
    plt.plot(efforts_sorted, speeds_sorted, 'o', label="Measured steady-state")
    plt.plot(efforts_sorted, fit_line, '-', label=f"Best-fit line (slope={m:.3f})")

    plt.xlabel("Effort (%)")
    plt.ylabel("Steady-State Velocity (counts/s)")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

# Load datasets
left_data = load_motor_data("left_motor", efforts)
right_data = load_motor_data("right_motor", efforts)

# Compute steady-state speeds
left_ss = extract_stable_speeds(left_data)
right_ss = extract_stable_speeds(right_data)

# Plot with linear fit and slope display
plot_curve_with_fit(left_ss, "Left Motor Steady-State Velocity vs Effort")
plot_curve_with_fit(right_ss, "Right Motor Steady-State Velocity vs Effort")

plt.show()
