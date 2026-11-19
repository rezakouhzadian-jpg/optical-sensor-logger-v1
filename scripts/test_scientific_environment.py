
import numpy as np
import matplotlib.pyplot as plt

# Generate simulated optical sensor data
time_s = np.linspace(0, 10, 101)

# Simulated sensor signal
signal = 2.5 + 0.5 * np.sin(2 * np.pi * 0.5 * time_s)

# Statistical analysis
mean_value = np.mean(signal)
max_value = np.max(signal)
min_value = np.min(signal)

print("Optical Sensor Test")
print("-------------------")
print(f"Number of samples: {len(signal)}")
print(f"Mean: {mean_value:.4f} V")
print(f"Maximum: {max_value:.4f} V")
print(f"Minimum: {min_value:.4f} V")

# Plot sensor signal
plt.figure(figsize=(10, 5))
plt.plot(time_s, signal, label="Sensor Signal")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Optical Sensor - Simulated Measurement")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
