
# Day 02 — Python Scientific Computing Foundation

## Project
Optical Sensor Logger V1

## Objective
Build the first Python-based engineering data pipeline using simulated ADC measurements.

## Technologies
- Python
- NumPy
- Matplotlib
- CSV
- JSON

## Features
- Simulated 12-bit ADC data generation
- CSV data storage
- Experiment metadata generation
- CSV data loading
- Measurement validation
- Basic statistical analysis
- Voltage versus time visualization

## Measurement Configuration

| Parameter | Value |
|---|---:|
| ADC Resolution | 12-bit |
| ADC Maximum | 4095 |
| Reference Voltage | 3.3 V |
| Sampling Rate | 100 Hz |
| Sample Count | 300 |
| Signal Frequency | 1.5 Hz |

## Output Files

```text
data/
├── simulated_sensor_data.csv
└── metadata.json

results/
└── voltage_vs_time.png
```

## How to Run

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Important Note

All data generated in this exercise are simulated.

No physical sensor or STM32 hardware is connected yet.

The purpose is to prepare the Python data pipeline before hardware integration.
