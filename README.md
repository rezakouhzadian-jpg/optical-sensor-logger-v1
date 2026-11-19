# Optical Sensor Logger V1 — Day 01 Starter Files

This folder contains the Day 01 project-definition documents:

- `docs/problem_statement.md` — problem, users, scope, and success definition.
- `docs/requirements.md` — initial testable requirements and provisional interface assumptions.
- `docs/system_architecture.png` — system block diagram.

Copy the `docs` folder into the root of your `AI-Engineering-Career` repository (or into the project folder you choose). Review every item marked provisional before hardware implementation.



# Optical Sensor Logger V1

An STM32-based optical measurement data acquisition
and Python logging system.

## Project Overview

This project aims to develop a modular embedded
instrumentation system for optical sensor measurements.

The system is designed to acquire analog signals,
digitize measurements using an STM32 ADC,
transmit data through UART and process measurements
using a Python host application.

## System Architecture

Optical Sensor
      |
Analog Front-End
      |
STM32 ADC
      |
UART
      |
Python Host
      |
CSV Dataset
      |
Analysis and Visualization

## Repository Structure

```text
firmware/      STM32 firmware
host/          PC-side Python applications
config/        Experiment configuration
data/          Measurement datasets
docs/          Technical documentation
environment/   Development environment records
logs/          Runtime logs
tests/         Software tests
figures/       Engineering plots
```

## Technologies

- Python
- NumPy
- Matplotlib
- STM32
- ADC
- UART
- Git
- GitHub

## Development Status

| Day | Activity | Status |
|---|---|---|
| 01 | Engineering Problem Definition | Completed |
| 02 | Python Scientific Computing | In Progress / Completed |
| 03 | Git and Project Architecture | In Progress |

## Running the Python Environment

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Important Notice

The initial software exercises may use simulated ADC data.

Simulated measurements must not be interpreted as real
optical sensor measurements.

Hardware integration and experimental validation
will be documented separately.

## License

License not yet assigned.
