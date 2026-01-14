# FFT Analysis for Vibration Waveforms

This document explains the FFT (Fast Fourier Transform) analysis added to the vibration analysis project.

## Overview

The FFT analysis has been integrated into `Manipulaçãodados_parte2.ipynb` to analyze the frequency content of synthesized vibration waveforms. This allows us to:

1. **Identify dominant frequencies** in vibration signals
2. **Compare frequency content** between baseline and alert conditions
3. **Track frequency evolution** over time
4. **Analyze energy distribution** across different frequency bands

## Features Added

### 1. FFT Computation Function (`compute_fft`)

Computes the Fast Fourier Transform of a time-domain waveform:
- **Input**: Time-domain signal, sampling rate
- **Output**: Frequency bins, magnitude spectrum, phase spectrum
- Automatically handles positive frequencies only
- Normalizes magnitude for consistent comparison

### 2. Frequency Band Analysis (`analyze_frequency_bands`)

Analyzes energy distribution across frequency bands:
- **Default bands**:
  - Very Low: 0-5 Hz
  - Low: 5-20 Hz
  - Mid: 20-60 Hz
  - High: 60-100 Hz
- Computes energy per band (sum of squared magnitudes)
- Useful for identifying which frequency ranges change during anomalies

### 3. Dominant Frequency Detection (`find_dominant_frequencies`)

Identifies peak frequencies in the spectrum:
- Uses `scipy.signal.find_peaks` for robust peak detection
- Returns top N frequencies with highest magnitude
- Filters out DC component and very low frequencies
- Useful for identifying characteristic vibration frequencies (e.g., bearing defects, imbalance)

## Visualizations

### 1. Baseline vs Alert Comparison

Side-by-side comparison showing:
- **Time domain**: Original waveform (baseline vs alert)
- **Frequency domain**: FFT spectrum with dominant frequencies marked
- Separate plots for acceleration and velocity
- Quantitative comparison of frequency band energy

### 2. FFT Evolution Over Time

Stacked FFT plots showing how frequency content changes:
- Samples from early, middle, and late operational phases
- Highlights alert events in red
- Shows progression of vibration characteristics

### 3. Spectrogram

2D heatmap showing frequency content evolution:
- X-axis: Time progression
- Y-axis: Frequency (0-100 Hz)
- Color: Magnitude in dB scale
- Alert times marked with vertical white lines

## Interpretation Guide

### What to Look For

1. **Frequency Shifts**: 
   - Changes in dominant frequency indicate mechanical changes
   - Example: Bearing wear may cause new frequencies to appear

2. **Energy Increase in Specific Bands**:
   - High-frequency energy increase often indicates bearing defects
   - Low-frequency changes may indicate imbalance or misalignment

3. **Harmonic Patterns**:
   - Multiple peaks at integer multiples indicate periodic phenomena
   - Can help identify rotating machinery issues

4. **Broadband Noise**:
   - Increase in broadband energy may indicate looseness or lubrication issues

### Example Output

```
Acceleration Channel: X
  Baseline frequency bands:
    very_low  : 0.000234
    low       : 0.001245
    mid       : 0.003456
    high      : 0.000123
  Alert frequency bands:
    very_low  : 0.000245 (Δ +4.7%)
    low       : 0.001567 (Δ +25.9%)
    mid       : 0.005234 (Δ +51.4%)
    high      : 0.000456 (Δ +270.7%)
  
  Baseline dominant frequencies: 50.0Hz, 100.0Hz, 25.3Hz
  Alert dominant frequencies: 50.0Hz, 87.5Hz, 175.0Hz
```

In this example:
- High-frequency energy increased by 270% (possible bearing issue)
- New frequency at 87.5 Hz appeared
- Harmonic at 175 Hz (2x 87.5) suggests periodic defect

## Technical Details

### Sampling Rate
- Default: 200 Hz (adjustable based on actual sensor sampling)
- Nyquist frequency: 100 Hz (max detectable frequency)
- Can be modified in the `sampling_rate` variable

### Waveform Synthesis
- Uses RMS, mean, and max statistics to recreate waveform
- Fundamental frequency + harmonics + noise
- Realistic clipping based on observed max values

### FFT Parameters
- Window: No windowing (rectangular)
- Resolution: Depends on signal length (default 200 samples = ~1 Hz resolution at 200 Hz sampling)
- Frequency range: 0-100 Hz (adjustable)

## Usage

Simply run the FFT analysis cell after the wave reconstruction cell (Cell 21). The analysis will:

1. Load existing reconstructed waveforms
2. Compute FFT for baseline and alert conditions
3. Generate all visualizations automatically
4. Print quantitative frequency analysis to console

## Dependencies

Required Python packages:
- `numpy` - Numerical computing
- `scipy` - FFT computation and peak detection
- `matplotlib` - Visualization
- `pandas` - Data manipulation

All dependencies are already included in the main notebook.

## Future Enhancements

Possible improvements:
1. **Windowing**: Apply Hann or Hamming window to reduce spectral leakage
2. **Order analysis**: Normalize by machine RPM for rotating machinery
3. **Envelope analysis**: For bearing defect detection
4. **Cepstrum analysis**: For gearbox diagnostics
5. **Statistical process control**: Track frequency features over time

## References

- Parseval's theorem: Energy conservation between time and frequency domains
- Vibration analysis standards: ISO 10816, ISO 20816
- Bearing defect frequencies: BPFO, BPFI, BSF, FTF
