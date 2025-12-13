
import os
import pandas as pd
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

        # If your CSVs do NOT have headers, use header=None and rename columns.
        df = pd.read_csv(filepath)

        # Assume first column is time (us), second is velocity (counts/s)
        # If the column names are known (e.g. "time_us", "velocity_counts_s"),
        # replace iloc with explicit column names.
        df = df.iloc[:, :2]
        df.columns = ["time_us", "velocity_counts_s"]

        # Optional: convert time to seconds for a nicer axis
        df["time_s"] = df["time_us"] * 1e-6

        data[effort] = df

    return data

def plot_motor_curves(data, title):
    """
    Plot velocity vs time for a set of effort curves.
    data: dict[effort] -> DataFrame with columns 'time_s' and 'velocity_counts_s'
    """
    plt.figure()
    for effort, df in sorted(data.items()):
        plt.plot(df["time_s"], df["velocity_counts_s"], label=f"{effort}% effort")

    plt.xlabel("Time (s)")          # change to "Time (µs)" and use time_us if you prefer
    plt.ylabel("Velocity (counts/s)")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

# Load data
left_data = load_motor_data("left_motor", efforts)
right_data = load_motor_data("right_motor", efforts)

# Plot
plot_motor_curves(left_data, "Left Motor Step Responses")
plot_motor_curves(right_data, "Right Motor Step Responses")

plt.show()
