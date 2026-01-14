# Vibration Analysis

A comprehensive vibration analysis project for machine health monitoring using acceleration and velocity data.

## Overview

This project analyzes vibration data from industrial machinery to detect anomalies, predict failures, and monitor machine health. It includes data preprocessing, anomaly detection using machine learning, and frequency domain analysis through FFT (Fast Fourier Transform).

## Features

### Data Processing (Parte 1)
- Load and pivot vibration data from CSV files
- Handle velocity and acceleration measurements
- Clean and preprocess time-series data
- Separate machine on/off states
- Filter and normalize data

### Anomaly Detection (Parte 2)
- **Isolation Forest**: Unsupervised anomaly detection
- **Autoencoder (MLP)**: Neural network-based reconstruction for anomaly scoring
- Alert system with warning and critical thresholds
- Health index tracking over operational time
- Temperature correlation analysis

### Frequency Analysis (NEW)
- **FFT (Fast Fourier Transform)** of reconstructed waveforms
- Frequency band energy analysis (very low, low, mid, high)
- Dominant frequency identification
- Baseline vs. alert condition comparison
- Spectrogram visualization showing frequency evolution over time

## Project Structure

```
.
├── Manipulaçãodados_parte1.ipynb  # Data preprocessing and cleaning
├── Manipulaçãodados_parte2.ipynb  # Anomaly detection and FFT analysis
├── FFT_Analysis_README.md         # Detailed FFT documentation
├── FFT_Example.py                 # Standalone FFT demo script
└── m3_preprocess_cache.pkl        # Cached preprocessed data
```

## Getting Started

### Prerequisites

```bash
pip install pandas numpy scipy matplotlib seaborn scikit-learn
```

### Running the Analysis

1. **Data Preprocessing (Parte 1)**:
   - Run all cells in `Manipulaçãodados_parte1.ipynb`
   - Generates `m3_preprocess_cache.pkl` with cleaned data
   - Separates machine on/off states

2. **Anomaly Detection & FFT Analysis (Parte 2)**:
   - Run all cells in `Manipulaçãodados_parte2.ipynb`
   - Trains Isolation Forest and Autoencoder models
   - Generates alerts and health metrics
   - **NEW**: Performs FFT analysis on reconstructed waveforms

3. **Standalone FFT Demo**:
   ```bash
   python FFT_Example.py
   ```
   Generates a demo visualization showing FFT analysis

## FFT Analysis

The FFT (Fast Fourier Transform) functionality transforms time-domain vibration signals into frequency domain for advanced analysis:

### Key Capabilities

1. **Frequency Spectrum Analysis**: Identify which frequencies are present in vibration signals
2. **Energy Distribution**: Analyze energy across different frequency bands
3. **Dominant Frequencies**: Detect characteristic vibration frequencies that may indicate specific mechanical issues
4. **Trend Analysis**: Track how frequency content changes over time
5. **Spectrogram**: Visualize frequency evolution as a 2D heatmap

### Use Cases

- **Bearing Defects**: High-frequency components increase
- **Imbalance**: Low-frequency peaks at rotational speed
- **Misalignment**: Harmonic patterns at 2x, 3x rotational frequency
- **Looseness**: Broadband noise increase

For detailed documentation, see [FFT_Analysis_README.md](FFT_Analysis_README.md)

## Workflow

```
Raw Data → Preprocessing → On/Off Separation → Anomaly Detection → FFT Analysis
   ↓            ↓                ↓                    ↓                  ↓
 CSV         Cleaned         Machine           Alerts &           Frequency
Files        Data            States            Scores             Analysis
```

## Data Format

Input data should be CSV files with columns:
- `variable`: Measurement type (e.g., velocity_rms, acceleration_max)
- `value`: Numerical measurement
- `group`: Measurement group identifier
- `time`: Timestamp

## Anomaly Detection Models

### Isolation Forest
- Unsupervised method
- Fast training
- Good for outlier detection
- Score: Higher = more anomalous

### Autoencoder (MLP)
- Neural network approach
- Learns normal patterns
- Score: Reconstruction error (MSE)
- Better at capturing complex patterns

### Combined Approach
- Critical alerts: Both models agree
- Warning alerts: Either model flags
- Reduces false positives while maintaining sensitivity

## Health Index

The health index tracks machine degradation:
- **Baseline**: Initial operational period (first 3 days)
- **Z-score**: Deviation from baseline
- **Trend**: Change over 7-day operational window
- **Active time**: Excludes downtime for accurate tracking

## Visualization

The project includes various visualizations:
- Time-series plots of vibration data
- Anomaly score plots with thresholds
- Alert markers on timelines
- Health index trends
- FFT spectra (baseline vs. alert)
- Spectrograms (frequency evolution)
- Comparison plots (time and frequency domain)

## Contributing

When adding new features:
1. Maintain consistency with existing code style
2. Update documentation
3. Add visualizations where helpful
4. Test with the existing dataset

## License

This project is provided as-is for educational and research purposes.

## Acknowledgments

- Uses industry-standard vibration analysis techniques
- Implements best practices from ISO 10816/20816 standards
- FFT analysis based on established signal processing methods
