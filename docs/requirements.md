# Optical Sensor Logger — V1 Requirements

## 1. Purpose

This document defines the initial, testable requirements for Optical Sensor Logger V1. Values marked **provisional** are starting targets and must be confirmed against the selected STM32 board, sensor, analog front-end, and test setup before implementation.

## 2. Functional Requirements

| ID | Requirement | Verification |
|---|---|---|
| FR-01 | The system shall acquire one analog input channel using the STM32 ADC. | Apply at least three known input levels and confirm the ADC response changes accordingly. |
| FR-02 | Firmware shall transmit each sample with a monotonically increasing sample index. | Inspect a serial capture and confirm indices increase by one. |
| FR-03 | Firmware shall transmit samples using a documented, line-based UART format. | Compare transmitted lines with the protocol specification. |
| FR-04 | The PC application shall receive UART data through a selected serial port. | Receive data from the target board in a bench test. |
| FR-05 | The PC application shall reject or flag malformed records rather than silently storing them as valid samples. | Inject malformed lines and verify error handling. |
| FR-06 | The PC application shall attach a host-side timestamp to each accepted sample. | Confirm timestamps exist and are parseable in the saved CSV. |
| FR-07 | The PC application shall save accepted samples to a CSV file. | Open the resulting CSV and verify its header and rows. |
| FR-08 | The system shall save run-level metadata separately from sample rows. | Confirm a metadata file is created and contains the agreed fields. |
| FR-09 | The system shall make missing sample indices detectable. | Remove or skip a sample in a test stream and verify a sequence gap is reported. |

## 3. Initial Non-Functional Requirements

| ID | Requirement | Initial target / note |
|---|---|---|
| NFR-01 | Sampling rate | **Provisional:** 100 samples/s for the first bench test; confirm ADC and serial throughput before freezing. |
| NFR-02 | ADC resolution | **Provisional:** 12-bit mode if supported by the selected STM32 ADC configuration. |
| NFR-03 | Analog input range | Must remain within the exact MCU board's permitted ADC input range. A 0–3.3 V range is only a design target if the board's VDDA/reference and pin limits support it. |
| NFR-04 | UART settings | **Provisional:** 115200 baud, 8 data bits, no parity, 1 stop bit (8N1). |
| NFR-05 | Data integrity | Every accepted sample must have a valid index and numeric ADC value in the allowed range. |
| NFR-06 | Reproducibility | Each run must record its configuration and relevant hardware/software identifiers. |
| NFR-07 | Maintainability | Firmware, Python receiver, documentation, and generated data should be kept in clearly separated folders. |

## 4. Data Interface Requirements

### 4.1 Provisional firmware-to-PC serial record

Use one ASCII line per sample, terminated by a newline character:

```text
sample_index,adc_raw\n
```

Example:

```text
0,2048
1,2051
2,2047
```

The exact protocol can be extended later, but V1 should keep it simple and documented. The receiver should validate that `sample_index` is an integer and `adc_raw` is an integer within the selected ADC's legal count range.

### 4.2 CSV sample file

Suggested columns:

```text
timestamp_utc,run_id,sample_index,adc_raw,voltage_v
```

`timestamp_utc` is assigned by the PC when the record is received. It is therefore a host reception timestamp, not a guaranteed hardware sampling timestamp. If precise acquisition timing is later required, firmware should transmit a device-side timer tick or timestamp.

`voltage_v` is a calculated estimate based on the configured ADC reference/supply value. Record the reference assumption in metadata; do not treat it as a calibrated optical-power measurement.

### 4.3 Run metadata

Suggested metadata fields:

- `run_id`
- `start_time_utc`
- `device_id`
- `firmware_version`
- `sensor_type`
- `analog_front_end`
- `sampling_rate_hz`
- `adc_resolution_bits`
- `adc_reference_voltage_assumed_v`
- `uart_baud_rate`
- `serial_port`
- `operator_notes`

## 5. Safety and Electrical Constraints

1. Never connect a signal to an MCU pin until its pin limits and board voltage domains have been checked in the datasheet and schematic.
2. Do not assume every STM32 pin is 5 V tolerant; ADC pins must be treated according to their specific limits.
3. Connect grounds appropriately between the signal source and MCU board.
4. Use a potentiometer or known low-voltage source for early tests; do not connect an uncharacterized photodiode circuit directly to the ADC.
5. A photodiode normally needs a suitable analog front-end. The TIA gain, bandwidth, stability, and output range will be designed separately.

## 6. Acceptance Criteria for V1

- A known analog input produces changing and plausible ADC readings.
- The firmware transmits indexed samples at the configured nominal rate.
- Python receives the stream and validates records.
- The CSV contains timestamps, run ID, sample index, raw ADC counts, and calculated voltage.
- The metadata file records the configuration used for the run.
- Missing indices and malformed records are detectable and reported.
- A short test report documents the equipment, wiring, settings, test steps, and observed results.

## 7. Open Decisions to Resolve Before Hardware Implementation

- Exact STM32 board and MCU part number.
- Exact ADC pin and analog supply/reference arrangement.
- Optical sensor type and its electrical output characteristics.
- Whether the first physical test uses a potentiometer or a sensor front-end.
- UART interface method (on-board ST-LINK virtual COM port or external USB-to-UART adapter).
- Whether the target sampling rate remains 100 samples/s after validating timing and serial throughput.
