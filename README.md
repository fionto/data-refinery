# data-refinery

A modular, observable data-ingress validation pipeline for research lab files (CSV, TXT, etc.). 

This utility acts as a "gatekeeper" for raw characterization data—ensuring files are structurally sound, readable, and non-empty *before* they hit downstream processing scripts.

## Core Architecture

The project relies on a **Fail-Fast Pipe-and-Filter** design:
1. **The State Tracker:** A lightweight dataclass wrapping each file to track its validation lifecycle.
2. **The Gates:** Isolated, sequential, single-purpose validation checks.
3. **The Pipeline:** An engine that streams files through configured gates, instantly detouring failures to achieve high observability.

## Current Focus: Phase 1 (File-Level Validation)

Before parsing data payloads, the pipeline executes rapid OS-level screening:

* **Extension Verification:** Flushes out incorrect file formats.
* **Size Thresholds:** Catches empty files or corrupted, zero-byte exports.
* **System Permissions:** Ensures the pipeline has read privileges.
* **File Integrity (Pre-check):** Verifies the file can be opened at the OS level.

## Key Features

* **High Observability:** Rejections don't just happen; they are logged with the exact stage and reason for failure.
* **Separation of Concerns:** Validation logic is decoupled from scientific processing logic.
* **Pluggable Config:** Easily swap or reorder validation gates depending on the specific characterization technique (Raman, Hall Effect, I(V), etc.).