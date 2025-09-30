#!/usr/bin/env python3
"""
ESP32 LDR Easy Real-Time Plotter
Simple but effective real-time plotting
"""

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import time

# Configuration
SERIAL_PORT = '/dev/cu.usbserial-0001'  # Change to your port
BAUD_RATE = 115200
MAX_POINTS = 200  # Number of points to display
SMOOTH_FACTOR = 0.3  # Smoothing factor (0.1 = very smooth, 1.0 = no smoothing)
INTERPOLATION_POINTS = 5  # Number of interpolation points between real data

# Data storage
adc_data = deque(maxlen=MAX_POINTS)
voltage_data = deque(maxlen=MAX_POINTS)
light_data = deque(maxlen=MAX_POINTS)
time_data = deque(maxlen=MAX_POINTS)

# Smoothed data storage
adc_smooth = deque(maxlen=MAX_POINTS)
voltage_smooth = deque(maxlen=MAX_POINTS)
light_smooth = deque(maxlen=MAX_POINTS)

# Initialize plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))
fig.suptitle('ESP32 LDR Real-Time Monitor', fontsize=16)

# Setup subplots with better styling
ax1.set_ylabel('ADC Value', fontsize=12, fontweight='bold')
ax1.set_ylim(0, 4095)
ax1.grid(True, alpha=0.3)
ax1.set_title('ADC Reading (0-4095)', fontsize=14)
line1, = ax1.plot([], [], 'b-', linewidth=2, alpha=0.8, label='ADC Raw')
line1_smooth, = ax1.plot([], [], 'b-', linewidth=3, alpha=1.0, label='ADC Smooth')
ax1.legend()

ax2.set_ylabel('Voltage (V)', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 3.3)
ax2.grid(True, alpha=0.3)
ax2.set_title('Voltage Reading (0-3.3V)', fontsize=14)
line2, = ax2.plot([], [], 'g-', linewidth=2, alpha=0.8, label='Voltage Raw')
line2_smooth, = ax2.plot([], [], 'g-', linewidth=3, alpha=1.0, label='Voltage Smooth')
ax2.legend()

ax3.set_ylabel('Light Level (%)', fontsize=12, fontweight='bold')
ax3.set_ylim(0, 100)
ax3.set_xlabel('Time (seconds)', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.set_title('Light Level (0-100%)', fontsize=14)
line3, = ax3.plot([], [], 'r-', linewidth=2, alpha=0.8, label='Light Raw')
line3_smooth, = ax3.plot([], [], 'r-', linewidth=3, alpha=1.0, label='Light Smooth')
ax3.legend()

# Serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"✅ Connected to {SERIAL_PORT}")
    print("📊 Real-time plotting started...")
    print("🔍 Close the plot window to stop")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

def parse_data(line):
    """Parse data from ESP32"""
    try:
        if ',' in line:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                adc = int(parts[0])
                voltage = float(parts[1])
                light = float(parts[2])
                return adc, voltage, light
    except:
        pass
    return None

def smooth_data(raw_data, smooth_data, factor):
    """Apply exponential smoothing to data"""
    if len(smooth_data) == 0:
        smooth_data.append(raw_data)
    else:
        # Exponential smoothing: new_value = factor * raw + (1-factor) * previous
        smoothed = factor * raw_data + (1 - factor) * smooth_data[-1]
        smooth_data.append(smoothed)
    return smooth_data

def apply_moving_average(data, window_size=5):
    """Apply moving average smoothing"""
    if len(data) < window_size:
        return list(data)
    
    smoothed = []
    for i in range(len(data)):
        start_idx = max(0, i - window_size + 1)
        window_data = list(data)[start_idx:i+1]
        smoothed.append(sum(window_data) / len(window_data))
    
    return smoothed

def interpolate_data(x_data, y_data, num_points=5):
    """Interpolate data for smoother curves"""
    if len(x_data) < 2:
        return x_data, y_data
    
    import numpy as np
    
    # Convert to numpy arrays
    x = np.array(x_data)
    y = np.array(y_data)
    
    # Create interpolation function
    from scipy.interpolate import interp1d
    
    try:
        # Use cubic interpolation for smooth curves
        f = interp1d(x, y, kind='cubic', bounds_error=False, fill_value='extrapolate')
        
        # Create more points for smoother curve
        x_new = np.linspace(x[0], x[-1], len(x) * num_points)
        y_new = f(x_new)
        
        return x_new, y_new
    except:
        # Fallback to linear interpolation
        return x_data, y_data

def animate(frame):
    """Real-time animation with smoothing"""
    global adc_data, voltage_data, light_data, time_data, adc_smooth, voltage_smooth, light_smooth
    
    # Read data from serial
    if ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data = parse_data(line)
                if data:
                    adc, voltage, light = data
                    
                    # Add to data arrays
                    current_time = time.time()
                    adc_data.append(adc)
                    voltage_data.append(voltage)
                    light_data.append(light)
                    time_data.append(current_time)
                    
                    # Apply smoothing
                    smooth_data(adc, adc_smooth, SMOOTH_FACTOR)
                    smooth_data(voltage, voltage_smooth, SMOOTH_FACTOR)
                    smooth_data(light, light_smooth, SMOOTH_FACTOR)
                    
                    # Print current values
                    print(f"ADC: {adc:4d} | Voltage: {voltage:5.2f}V | Light: {light:5.1f}%")
        except Exception as e:
            print(f"Error: {e}")
    
    # Update plots
    if len(time_data) > 1:
        # Convert time to relative seconds
        time_rel = [(t - time_data[0]) for t in time_data]
        
        # Update raw data lines
        line1.set_data(time_rel, list(adc_data))
        line2.set_data(time_rel, list(voltage_data))
        line3.set_data(time_rel, list(light_data))
        
        # Update smoothed data lines
        if len(adc_smooth) > 0:
            line1_smooth.set_data(time_rel, list(adc_smooth))
        if len(voltage_smooth) > 0:
            line2_smooth.set_data(time_rel, list(voltage_smooth))
        if len(light_smooth) > 0:
            line3_smooth.set_data(time_rel, list(light_smooth))
        
        # Update axis limits for scrolling
        if len(time_rel) > 1:
            x_min = max(0, time_rel[-1] - 30)  # Show last 30 seconds
            x_max = time_rel[-1] + 2
            
            ax1.set_xlim(x_min, x_max)
            ax2.set_xlim(x_min, x_max)
            ax3.set_xlim(x_min, x_max)
            
            # Auto-scale Y axis for better visualization
            if len(adc_data) > 5:
                adc_margin = (max(adc_data) - min(adc_data)) * 0.1
                ax1.set_ylim(max(0, min(adc_data) - adc_margin), 
                           min(4095, max(adc_data) + adc_margin))
            
            if len(voltage_data) > 5:
                volt_margin = (max(voltage_data) - min(voltage_data)) * 0.1
                ax2.set_ylim(max(0, min(voltage_data) - volt_margin), 
                           min(3.3, max(voltage_data) + volt_margin))
            
            if len(light_data) > 5:
                light_margin = (max(light_data) - min(light_data)) * 0.1
                ax3.set_ylim(max(0, min(light_data) - light_margin), 
                           min(100, max(light_data) + light_margin))
    
    return line1, line1_smooth, line2, line2_smooth, line3, line3_smooth

# Start animation
print("🚀 Starting smooth animation...")
print(f"📊 Smoothing factor: {SMOOTH_FACTOR}")
print("🎯 Showing both raw and smoothed data")
ani = animation.FuncAnimation(fig, animate, interval=50, blit=False)

try:
    plt.tight_layout()
    plt.show()
except KeyboardInterrupt:
    print("\n⏹️  Stopping...")

# Cleanup
ser.close()
print("🔌 Serial connection closed")
