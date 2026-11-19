
"""
Optical Sensor Logger V1
Day 02 - Python Scientific Computing Foundation

This program:
1. Generates simulated 12-bit ADC measurements.
2. Saves measurements in CSV format.
3. Saves experiment metadata in JSON format.
4. Reads and validates the CSV dataset.
5. Calculates basic engineering statistics.
6. Plots voltage versus time.

IMPORTANT:
The data are simulated. No physical sensor or STM32 is connected.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# 1. Project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"

CSV_FILE = DATA_DIR / "simulated_sensor_data.csv"
METADATA_FILE = DATA_DIR / "metadata.json"
PLOT_FILE = RESULTS_DIR / "voltage_vs_time.png"


# ============================================================
# 2. Experiment configuration
# ============================================================

ADC_BITS = 12
ADC_MAX = (2 ** ADC_BITS) - 1

VREF_V = 3.3

SAMPLE_RATE_HZ = 100
NUMBER_OF_SAMPLES = 300

SIGNAL_FREQUENCY_HZ = 1.5

RANDOM_SEED = 42


# ============================================================
# 3. Create project directories
# ============================================================

def create_directories() -> None:
    """Create data and results directories."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 4. Generate simulated ADC data
# ============================================================

def generate_simulated_data() -> None:
    """
    Generate a simulated analog sensor signal.

    The signal contains:
    - A baseline ADC value
    - A sinusoidal variation
    - Random measurement noise
    """

    rng = np.random.default_rng(RANDOM_SEED)

    sample_index = np.arange(NUMBER_OF_SAMPLES)

    time_s = sample_index / SAMPLE_RATE_HZ

    baseline = 1800.0
    amplitude = 250.0

    noise = rng.normal(
        loc=0.0,
        scale=12.0,
        size=NUMBER_OF_SAMPLES
    )

    signal = (
        baseline
        + amplitude
        * np.sin(2 * np.pi * SIGNAL_FREQUENCY_HZ * time_s)
        + noise
    )

    adc_raw = np.clip(
        np.rint(signal),
        0,
        ADC_MAX
    ).astype(int)

    voltage_v = (adc_raw / ADC_MAX) * VREF_V

    # Save measurement data as CSV.
    with CSV_FILE.open(
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "sample_index",
            "time_s",
            "adc_raw",
            "voltage_v"
        ])

        writer.writerows(
            zip(
                sample_index.tolist(),
                np.round(time_s, 6).tolist(),
                adc_raw.tolist(),
                np.round(voltage_v, 6).tolist()
            )
        )

    print("Simulated CSV dataset created.")


# ============================================================
# 5. Save experiment metadata
# ============================================================

def save_metadata() -> None:
    """Save measurement configuration as JSON."""

    metadata = {
        "project": "Optical Sensor Logger V1",
        "day": 2,
        "data_source": "SIMULATED",
        "sensor_type": "Simulated analog input",
        "hardware_connected": False,
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "adc_resolution_bits": ADC_BITS,
        "adc_max_count": ADC_MAX,
        "reference_voltage_v": VREF_V,
        "sampling_rate_hz": SAMPLE_RATE_HZ,
        "sample_count": NUMBER_OF_SAMPLES,
        "signal_frequency_hz": SIGNAL_FREQUENCY_HZ,
        "random_seed": RANDOM_SEED,
        "voltage_conversion": "adc_raw / adc_max_count * vref_v"
    }

    with METADATA_FILE.open(
        mode="w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4
        )

    print("Experiment metadata saved.")


# ============================================================
# 6. Load and validate CSV measurements
# ============================================================

def load_measurements():
    """Read CSV data and validate the measurement fields."""

    sample_indices = []
    time_values = []
    adc_values = []
    voltage_values = []

    required_columns = {
        "sample_index",
        "time_s",
        "adc_raw",
        "voltage_v"
    }

    with CSV_FILE.open(
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file has no header.")

        missing = required_columns.difference(
            reader.fieldnames
        )

        if missing:
            raise ValueError(
                f"Missing CSV columns: {sorted(missing)}"
            )

        for line_number, row in enumerate(reader, start=2):

            try:
                sample_indices.append(
                    int(row["sample_index"])
                )

                time_values.append(
                    float(row["time_s"])
                )

                adc_values.append(
                    int(row["adc_raw"])
                )

                voltage_values.append(
                    float(row["voltage_v"])
                )

            except (ValueError, TypeError) as error:

                raise ValueError(
                    f"Invalid numeric data at CSV line {line_number}."
                ) from error

    if not adc_values:
        raise ValueError("No measurement samples were found.")

    sample_indices = np.asarray(
        sample_indices,
        dtype=np.int64
    )

    time_values = np.asarray(
        time_values,
        dtype=float
    )

    adc_values = np.asarray(
        adc_values,
        dtype=np.int64
    )

    voltage_values = np.asarray(
        voltage_values,
        dtype=float
    )

    if np.any(adc_values < 0) or np.any(adc_values > ADC_MAX):
        raise ValueError("ADC values are outside the valid range.")

    if not np.all(np.diff(sample_indices) > 0):
        raise ValueError("Sample indices must be strictly increasing.")

    if not np.all(np.diff(time_values) > 0):
        raise ValueError("Sample times must be strictly increasing.")

    expected_voltage = (adc_values / ADC_MAX) * VREF_V

    if not np.allclose(
        voltage_values,
        expected_voltage,
        atol=1e-5
    ):
        raise ValueError("Voltage conversion validation failed.")

    return (
        sample_indices,
        time_values,
        adc_values,
        voltage_values
    )


# ============================================================
# 7. Calculate basic engineering statistics
# ============================================================

def analyze_measurements(
    adc_values: np.ndarray,
    voltage_values: np.ndarray
) -> None:
    """Calculate basic statistics of the dataset."""

    mean_adc = np.mean(adc_values)
    min_adc = np.min(adc_values)
    max_adc = np.max(adc_values)

    mean_voltage = np.mean(voltage_values)
    std_voltage = (
        np.std(voltage_values, ddof=1)
        if len(voltage_values) > 1
        else 0.0
    )

    min_voltage = np.min(voltage_values)
    max_voltage = np.max(voltage_values)

    maximum_index = int(np.argmax(voltage_values))

    print("\n========== MEASUREMENT REPORT ==========")

    print(f"Number of samples : {len(adc_values)}")

    print(f"Minimum ADC       : {min_adc}")
    print(f"Maximum ADC       : {max_adc}")
    print(f"Mean ADC          : {mean_adc:.2f}")

    print(f"Minimum voltage   : {min_voltage:.4f} V")
    print(f"Maximum voltage   : {max_voltage:.4f} V")
    print(f"Mean voltage      : {mean_voltage:.4f} V")
    print(f"Voltage std       : {std_voltage:.5f} V")

    print(f"Maximum sample    : {maximum_index}")

    print("========================================\n")


# ============================================================
# 8. Plot measurement data
# ============================================================

def plot_measurements(
    time_values: np.ndarray,
    voltage_values: np.ndarray
) -> None:
    """Plot voltage measurements against time."""

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        time_values,
        voltage_values,
        linewidth=1.2,
        label="Simulated ADC voltage"
    )

    ax.set_title("Simulated Sensor Voltage vs Time")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")

    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    fig.savefig(
        PLOT_FILE,
        dpi=150
    )

    plt.close(fig)

    print(f"Plot saved to: {PLOT_FILE}")

    


# ============================================================
# 9. Main program
# ============================================================

def main() -> None:
    """Execute the complete Day 02 data pipeline."""

    try:

        print("\nOptical Sensor Logger V1")
        print("Day 02 - Engineering Data Processing\n")

        create_directories()

        generate_simulated_data()

        save_metadata()

        (
            sample_indices,
            time_values,
            adc_values,
            voltage_values
        ) = load_measurements()

        analyze_measurements(
            adc_values,
            voltage_values
        )

        plot_measurements(
            time_values,
            voltage_values
        )

        print("Day 02 program completed successfully.")

    except (OSError, ValueError, KeyError) as error:

        print(f"\nERROR: {error}")

        raise SystemExit(1) from error


if __name__ == "__main__":
    main()


def plot_measurements(
    time_values: np.ndarray,
    voltage_values: np.ndarray,
    ideal_voltage: np.ndarray
) -> None:

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        time_values,
        voltage_values,
        linewidth=1.2,
        label="Measured Voltage"
    )

    ax.plot(
        time_values,
        ideal_voltage,
        linestyle="--",
        linewidth=1.5,
        label="Ideal Voltage"
    )

    ax.set_title("Ideal vs Measured Sensor Voltage")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")

    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(PLOT_FILE, dpi=150)
    plt.close(fig)

    print(f"Plot saved to: {PLOT_FILE}")