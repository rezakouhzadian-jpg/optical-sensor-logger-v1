# Optical Sensor Logger — V1

## 1. Project Overview

Optical Sensor Logger V1 is a small embedded measurement system intended to acquire an analog signal related to optical intensity, transfer measurement samples to a PC, and store the received data in a structured dataset for later analysis.

The first version focuses on a reliable end-to-end acquisition pipeline: analog input, STM32 ADC sampling, UART communication, Python reception, timestamping, and CSV logging.

## 2. Problem Statement

In a typical small optical laboratory experiment, an operator may read a sensor output and record measurements manually. This workflow is slow, difficult to reproduce, and vulnerable to transcription errors, missing timestamps, and inconsistent file formats. Comparing repeated experiments can also become difficult when acquisition settings and measurement metadata are not recorded consistently.

The proposed system will automate the capture and storage of measurement samples. An analog sensor signal (or a controlled test signal during initial development) will be sampled by an STM32 microcontroller. The firmware will transmit sample records over UART to a PC. A Python application will receive the records, validate them, attach a host-side timestamp, and save the data and run metadata to files suitable for later analysis.

## 3. Intended Users

- An optical laboratory operator who needs repeatable measurement records.
- An engineering student or researcher who needs traceable datasets for signal analysis.
- A developer who needs a reusable acquisition platform for later optical test-bench automation.

## 4. Current Workflow and Pain Points

1. Measurements may be written down manually.
2. Transcription can introduce mistakes.
3. Measurement timestamps may be missing or inconsistent.
4. Repeated experiments may use different recording formats.
5. Reconstructing acquisition settings later may be difficult.

## 5. Proposed Solution

The system will implement the following data path:

1. An optical sensor and its required analog front-end produce a voltage suitable for the MCU ADC input.
2. The STM32 samples the analog voltage using its ADC.
3. Firmware sends a simple, documented sample record over UART.
4. A Python PC application receives and validates each record.
5. Python records a host-side timestamp and saves samples to CSV.
6. A separate analysis stage can later clean, visualize, and characterize the dataset.

During early bring-up, a potentiometer or another safe, known analog test source may be used instead of the optical sensor. This verifies the ADC-to-PC data path before the optical sensor and analog front-end are integrated.

## 6. Important Measurement Boundary

The ADC measures voltage, not optical intensity directly. A photodiode generally requires an appropriate analog front-end, commonly a transimpedance amplifier, to convert photocurrent into a voltage. Converting ADC voltage into optical power or irradiance requires sensor-specific calibration. V1 must therefore preserve raw ADC counts and voltage values; it must not label voltage as optical intensity unless a valid calibration model has been applied.

## 7. Scope of V1

### Included

- One analog measurement channel.
- STM32 ADC acquisition.
- UART data transfer to a PC.
- Python serial reception and basic record validation.
- Host-side timestamping.
- CSV sample logging.
- A metadata file describing each measurement run.
- A basic repeatable test using a known analog input.

### Not included in the first version

- Multi-channel acquisition.
- A finalized photodiode/TIA PCB design.
- Traceable optical-power calibration.
- Advanced digital filtering or peak analysis.
- Automated instrument control or a complete optical test bench.
- A graphical user interface.

## 8. Expected Deliverables

- STM32 firmware source code.
- Python serial receiver.
- One or more raw CSV datasets.
- Run metadata (for example, JSON).
- A short technical report with setup, test procedure, results, and limitations.
- Documentation of the serial data format and system architecture.

## 9. Main Risks and Mitigations

| Risk | Mitigation |
|---|---|
| ADC input exceeds permitted voltage | Check MCU datasheet and board design; keep input within the specified analog supply range. |
| UART records are incomplete or corrupted | Use a documented line format, delimiters, and Python validation. |
| Serial data is lost | Include a monotonically increasing sample index and detect gaps. |
| ADC readings are noisy | Begin with a stable test voltage; investigate grounding, wiring, reference voltage, and analog filtering. |
| Voltage is incorrectly reported as optical power | Store raw counts and voltage; apply optical calibration only after sensor characterization. |

## 10. Success Definition

V1 will be considered successful when the system can acquire a known analog input, transfer a sequence of indexed samples to the PC, validate the received records, and save a timestamped CSV dataset plus run metadata without unexplained missing or malformed records during a documented bench test.
