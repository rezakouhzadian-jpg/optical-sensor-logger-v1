
# Optical Sensor Logger V1
# Project Architecture

## 1. Project Overview

This project develops an embedded optical measurement
and data acquisition system based on STM32 and Python.

## 2. Software Architecture

### Firmware Layer

Location: firmware/stm32/

Responsibilities:
- ADC initialization
- Sensor data acquisition
- UART communication
- Sampling timer configuration
- Measurement data transmission

### Host Software Layer

Location: host/python/

Responsibilities:
- Serial communication
- Data reception
- Data validation
- Timestamp handling
- CSV storage
- Measurement analysis
- Data visualization

### Configuration Layer

Location: config/

Responsibilities:
- Sampling configuration
- UART configuration
- Measurement parameters
- Experiment settings

### Data Layer

Location: data/

Subdirectories:
- simulated/: Synthetic test datasets
- raw/: Original experimental measurements
- processed/: Validated or processed datasets

### Testing Layer

Location: tests/

Responsibilities:
- Host software tests
- Firmware-related tests
- Data validation tests

### Documentation Layer

Location: docs/

Responsibilities:
- Problem statement
- Engineering requirements
- System architecture
- Technical reports

## 3. Communication Architecture

Optical Sensor
      |
Analog Front-End
      |
STM32 ADC
      |
UART
      |
Python Host Application
      |
CSV Dataset
      |
Data Analysis

## 4. Design Principles

- Modular architecture
- Separation of firmware and host software
- Reproducible measurements
- Data traceability
- Version control
- Testability
- Extensible software structure

## 5. Current Development Status

Day 01:
System definition and initial documentation.

Day 02:
Python scientific computing foundation.

Day 03:
Git workflow and project architecture.
