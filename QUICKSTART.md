# FFT Implementation - Quick Start Guide

## What Was Added

The FFT (Fast Fourier Transform) analysis allows you to see **which frequencies** are present in the vibration signals, helping identify specific mechanical issues.

## Why It Matters

Different mechanical problems create different frequency patterns:
- **Bearing defects** → High frequency components increase
- **Imbalance** → Peaks at rotational frequency
- **Misalignment** → Harmonics (2x, 3x the rotation speed)
- **Looseness** → Broadband noise increase

## How to Use

### Step 1: Run the Notebooks
```
1. Open Manipulaçãodados_parte1.ipynb
   → Run all cells to preprocess data
   
2. Open Manipulaçãodados_parte2.ipynb
   → Run all cells including the new FFT analysis cell
```

### Step 2: Understand the Output

The FFT analysis generates three types of visualizations:

#### A) Baseline vs Alert Comparison
Shows side-by-side:
- **Time Domain**: How the waveform looks (amplitude over time)
- **Frequency Domain**: Which frequencies are present (FFT spectrum)

**What to look for:**
- New peaks appearing in alert condition
- Existing peaks getting larger
- Shifts in dominant frequencies

#### B) FFT Evolution
Shows how frequency content changes over time:
- Multiple timestamps from early → middle → late operation
- Alert events highlighted in red

**What to look for:**
- Gradual changes in frequency content
- Sudden appearance of new frequencies
- Energy shifts to higher frequencies

#### C) Spectrogram
2D heatmap showing frequency evolution:
- **X-axis**: Time progression
- **Y-axis**: Frequency (0-100 Hz)
- **Color**: Energy level (brighter = more energy)

**What to look for:**
- Vertical white lines mark alert events
- Horizontal bands show persistent frequencies
- Color intensity changes indicate energy evolution

### Step 3: Interpret the Numbers

The analysis prints quantitative metrics:

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
    high      : 0.000456 (Δ +270.7%)  ← SIGNIFICANT INCREASE!
```

**Interpretation:**
- High frequency energy increased by 270% 
- This pattern suggests **bearing wear or defect**
- Early warning of potential failure

## Quick Reference: Frequency Bands

| Band | Range | Typical Issues |
|------|-------|----------------|
| Very Low | 0-5 Hz | Structural issues, very slow oscillations |
| Low | 5-20 Hz | Imbalance, misalignment, rotor issues |
| Mid | 20-60 Hz | Gear mesh frequencies, motor issues |
| High | 60-100 Hz | Bearing defects, electrical issues |

## Try the Demo

Run the standalone example:
```bash
python FFT_Example.py
```

This generates a demo visualization showing:
1. Baseline signal (normal operation)
2. Alert signal (anomaly detected)
3. FFT comparison between both

## Advanced Usage

### Customize Frequency Bands
Edit the `bands` parameter in `analyze_frequency_bands()`:
```python
custom_bands = {
    'slow_roll': (0, 10),
    'running_speed': (10, 30),
    'high_freq': (30, 100),
}
```

### Adjust Sampling Rate
If you know your actual sensor sampling rate:
```python
sampling_rate = 200.0  # Change this value
```

### Change Number of Peaks
To detect more or fewer dominant frequencies:
```python
peak_freqs, peak_mags = find_dominant_frequencies(
    freqs, magnitude, n_peaks=5  # Increase/decrease this
)
```

## Troubleshooting

### Issue: "No peaks found"
- Signal might be too noisy
- Try lowering `min_freq` parameter
- Check if waveform has NaN values

### Issue: "FFT looks flat"
- Waveform might have very low amplitude
- Check RMS values are reasonable
- Verify synthesize_waveform parameters

### Issue: "Too many peaks detected"
- Increase `peak_distance` parameter
- This filters out noise peaks

## Learn More

- **Full Documentation**: See `FFT_Analysis_README.md`
- **Code Examples**: See `FFT_Example.py`
- **Theory**: Look up "vibration analysis frequency domain" online

## Support

For issues or questions:
1. Check the full documentation in `FFT_Analysis_README.md`
2. Review code comments in `FFT_Example.py`
3. Examine the notebook outputs for examples

---

**Remember**: FFT analysis is most powerful when combined with knowledge of the machinery:
- What is the expected rotation speed?
- What are the bearing specifications?
- What frequencies are normal for this machine?

Use FFT to **detect changes** from baseline, not just absolute values!
