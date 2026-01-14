#!/usr/bin/env python3
"""
FFT Analysis Example for Vibration Waveforms

This script demonstrates the FFT analysis functionality added to the 
Vibration Analysis project. It shows how to use the FFT functions 
independently from the Jupyter notebook.

Requirements:
- numpy
- scipy
- matplotlib
"""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt


def compute_fft(waveform, sampling_rate=200.0):
    """
    Compute FFT (Fast Fourier Transform) of a waveform.
    
    Parameters:
    - waveform: time-domain signal
    - sampling_rate: sampling frequency in Hz
    
    Returns:
    - freqs: frequency bins (Hz) or empty array if invalid input
    - magnitude: magnitude spectrum (normalized) or empty array if invalid input
    - phase: phase spectrum (radians) or empty array if invalid input
    
    Note: Returns empty arrays (not None) for invalid input to prevent downstream errors
    """
    # Handle NaN values - return empty arrays instead of None
    if np.any(np.isnan(waveform)):
        return np.array([]), np.array([]), np.array([])
    
    # Compute FFT
    n = len(waveform)
    yf = fft(waveform)
    xf = fftfreq(n, 1 / sampling_rate)
    
    # Take only positive frequencies
    positive_freq_idx = xf >= 0
    freqs = xf[positive_freq_idx]
    magnitude = np.abs(yf[positive_freq_idx]) / n  # Normalize
    phase = np.angle(yf[positive_freq_idx])
    
    return freqs, magnitude, phase


def analyze_frequency_bands(freqs, magnitude, bands=None):
    """
    Analyze energy in different frequency bands.
    
    Parameters:
    - freqs: frequency array from FFT
    - magnitude: magnitude spectrum from FFT
    - bands: dict of frequency bands, e.g., {'low': (0, 10), 'mid': (10, 50)}
    
    Returns:
    - band_energy: dict with energy per band
    """
    if bands is None:
        bands = {
            'very_low': (0, 5),
            'low': (5, 20),
            'mid': (20, 60),
            'high': (60, 100),
        }
    
    band_energy = {}
    for band_name, (f_min, f_max) in bands.items():
        mask = (freqs >= f_min) & (freqs <= f_max)
        # Energy is proportional to magnitude squared (Parseval's theorem)
        energy = np.sum(magnitude[mask] ** 2)
        band_energy[band_name] = float(energy)
    
    return band_energy


def find_dominant_frequencies(freqs, magnitude, n_peaks=5, min_freq=1.0, peak_distance=2):
    """
    Find dominant (peak) frequencies in the spectrum.
    
    Parameters:
    - freqs: frequency array
    - magnitude: magnitude spectrum
    - n_peaks: number of peaks to return
    - min_freq: minimum frequency to consider (ignore DC and very low freq)
    - peak_distance: minimum distance between peaks in samples (default=2 to avoid 
                     detecting noise as separate peaks)
    
    Returns:
    - peak_freqs: frequencies of peaks
    - peak_mags: magnitudes of peaks
    """
    # Filter out very low frequencies
    mask = freqs >= min_freq
    freqs_filtered = freqs[mask]
    magnitude_filtered = magnitude[mask]
    
    # Find peaks using scipy
    # distance=2 ensures peaks are at least 2 samples apart to avoid noise
    peaks, properties = signal.find_peaks(magnitude_filtered, height=0, distance=peak_distance)
    
    if len(peaks) == 0:
        return [], []
    
    # Sort by magnitude (height) and take top n
    heights = properties['peak_heights']
    sorted_idx = np.argsort(heights)[::-1][:n_peaks]
    
    peak_freqs = freqs_filtered[peaks[sorted_idx]]
    peak_mags = heights[sorted_idx]
    
    return peak_freqs, peak_mags


def synthesize_waveform(rms, mean, max_val, n_samples=200, freq_hz=50.0):
    """
    Synthesize a waveform from statistics (for demonstration).
    
    Parameters:
    - rms: RMS value
    - mean: mean value (DC offset)
    - max_val: maximum value (for clipping)
    - n_samples: number of samples
    - freq_hz: fundamental frequency
    
    Returns:
    - waveform: synthesized time-domain signal
    """
    if np.isnan(rms) or np.isnan(mean) or np.isnan(max_val):
        return np.full(n_samples, np.nan)
    
    amplitude = float(rms) * np.sqrt(2)
    t = np.linspace(0, 1, n_samples)
    
    # Fundamental + harmonics
    signal = (
        amplitude * np.sin(2 * np.pi * freq_hz * t)
        + 0.3 * amplitude * np.sin(2 * np.pi * freq_hz * 2 * t + 0.5)
        + 0.15 * amplitude * np.sin(2 * np.pi * freq_hz * 3 * t + 1.2)
    )
    
    signal += float(mean)
    noise = np.random.normal(0, float(rms) * 0.05, n_samples)
    signal += noise
    signal = np.clip(signal, -abs(float(max_val)), abs(float(max_val)))
    
    return signal


def demo_fft_analysis():
    """Run a complete FFT analysis demo."""
    
    print("="*80)
    print("FFT Analysis Demo - Vibration Waveforms")
    print("="*80)
    
    # Parameters
    sampling_rate = 200.0  # Hz
    n_samples = 200
    
    # Simulate baseline and alert conditions
    print("\n1. Generating waveforms...")
    
    # Baseline: normal operation (50 Hz fundamental)
    baseline_rms = 1.0
    baseline_mean = 0.0
    baseline_max = 2.5
    waveform_baseline = synthesize_waveform(baseline_rms, baseline_mean, baseline_max, 
                                           n_samples=n_samples, freq_hz=50.0)
    
    # Alert: anomalous condition (higher RMS, new frequency component at 75 Hz)
    alert_rms = 2.5  # 2.5x increase in energy
    alert_mean = 0.1
    alert_max = 5.0
    # Mix 50 Hz and 75 Hz
    t = np.linspace(0, 1, n_samples)
    waveform_alert = (
        alert_rms * np.sqrt(2) * np.sin(2 * np.pi * 50 * t) +
        alert_rms * np.sqrt(2) * 0.5 * np.sin(2 * np.pi * 75 * t) +
        np.random.normal(0, alert_rms * 0.1, n_samples)
    )
    
    print(f"   Baseline: RMS={baseline_rms:.2f}, Mean={baseline_mean:.2f}")
    print(f"   Alert:    RMS={alert_rms:.2f}, Mean={alert_mean:.2f}")
    
    # Compute FFT
    print("\n2. Computing FFT...")
    freqs_baseline, mag_baseline, _ = compute_fft(waveform_baseline, sampling_rate)
    freqs_alert, mag_alert, _ = compute_fft(waveform_alert, sampling_rate)
    print(f"   ✓ FFT computed for both signals")
    
    # Analyze frequency bands
    print("\n3. Frequency band analysis:")
    bands_baseline = analyze_frequency_bands(freqs_baseline, mag_baseline)
    bands_alert = analyze_frequency_bands(freqs_alert, mag_alert)
    
    print("\n   Baseline:")
    for band, energy in bands_baseline.items():
        print(f"      {band:10s}: {energy:.6f}")
    
    print("\n   Alert:")
    for band, energy in bands_alert.items():
        # Protect against division by zero
        delta = ((energy - bands_baseline[band]) / bands_baseline[band] * 100) if bands_baseline[band] != 0 else 0
        print(f"      {band:10s}: {energy:.6f} (Δ {delta:+.1f}%)")
    
    # Find dominant frequencies
    print("\n4. Dominant frequencies:")
    peaks_baseline, _ = find_dominant_frequencies(freqs_baseline, mag_baseline, n_peaks=3)
    peaks_alert, _ = find_dominant_frequencies(freqs_alert, mag_alert, n_peaks=3)
    
    print(f"   Baseline: {', '.join([f'{f:.1f} Hz' for f in peaks_baseline])}")
    print(f"   Alert:    {', '.join([f'{f:.1f} Hz' for f in peaks_alert])}")
    
    # Visualization
    print("\n5. Creating visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Time domain - baseline
    t_norm = np.linspace(0, 1, n_samples)
    axes[0, 0].plot(t_norm, waveform_baseline, linewidth=1.5)
    axes[0, 0].set_title('Baseline - Time Domain', fontweight='bold')
    axes[0, 0].set_xlabel('Normalized Time')
    axes[0, 0].set_ylabel('Amplitude')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Time domain - alert
    axes[0, 1].plot(t_norm, waveform_alert, linewidth=1.5, color='red')
    axes[0, 1].set_title('Alert - Time Domain', fontweight='bold')
    axes[0, 1].set_xlabel('Normalized Time')
    axes[0, 1].set_ylabel('Amplitude')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Frequency domain - baseline
    axes[1, 0].plot(freqs_baseline, mag_baseline, linewidth=1.5)
    for pf in peaks_baseline:
        idx = np.argmin(np.abs(freqs_baseline - pf))
        axes[1, 0].plot(pf, mag_baseline[idx], 'ro', markersize=8)
        axes[1, 0].annotate(f'{pf:.1f}Hz', xy=(pf, mag_baseline[idx]), 
                           xytext=(5, 5), textcoords='offset points')
    axes[1, 0].set_title('Baseline - Frequency Domain (FFT)', fontweight='bold')
    axes[1, 0].set_xlabel('Frequency (Hz)')
    axes[1, 0].set_ylabel('Magnitude')
    axes[1, 0].set_xlim(0, 100)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Frequency domain - alert
    axes[1, 1].plot(freqs_alert, mag_alert, linewidth=1.5, color='red')
    for pf in peaks_alert:
        idx = np.argmin(np.abs(freqs_alert - pf))
        axes[1, 1].plot(pf, mag_alert[idx], 'ro', markersize=8)
        axes[1, 1].annotate(f'{pf:.1f}Hz', xy=(pf, mag_alert[idx]), 
                           xytext=(5, 5), textcoords='offset points', color='red')
    axes[1, 1].set_title('Alert - Frequency Domain (FFT)', fontweight='bold')
    axes[1, 1].set_xlabel('Frequency (Hz)')
    axes[1, 1].set_ylabel('Magnitude')
    axes[1, 1].set_xlim(0, 100)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('FFT Analysis Example', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Save figure
    output_file = 'fft_demo_output.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"   ✓ Visualization saved to '{output_file}'")
    
    print("\n" + "="*80)
    print("Demo completed successfully!")
    print("="*80)
    
    # Show if running interactively
    # plt.show()


if __name__ == '__main__':
    demo_fft_analysis()
