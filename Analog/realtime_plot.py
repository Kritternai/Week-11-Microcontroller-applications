#!/usr/bin/env python3
"""
ESP32 LDR Real-Time Plotter
High-performance real-time plotting with smooth animations
"""

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import time
import numpy as np
import threading
import queue

# Configuration
SERIAL_PORT = '/dev/cu.usbserial-0001'  # Change to your port
BAUD_RATE = 115200
MAX_POINTS = 200  # Number of points to display
UPDATE_INTERVAL = 50  # Update interval in milliseconds

# Data storage
data_queue = queue.Queue()
adc_data = deque(maxlen=MAX_POINTS)
voltage_data = deque(maxlen=MAX_POINTS)
light_data = deque(maxlen=MAX_POINTS)
status_data = deque(maxlen=MAX_POINTS)
time_data = deque(maxlen=MAX_POINTS)

# Initialize plot with better styling
plt.style.use('seaborn-v0_8')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10))
fig.suptitle('ESP32 LDR Sensor - Real-Time Monitor', fontsize=16, fontweight='bold')

# Setup subplots with better styling
ax1.set_ylabel('ADC Value', fontsize=12, fontweight='bold')
ax1.set_ylim(0, 4095)
ax1.grid(True, alpha=0.3)
ax1.set_title('ADC Reading (0-4095)', fontsize=14)
line1, = ax1.plot([], [], 'b-', linewidth=2, label='ADC Raw')
ax1.legend()

ax2.set_ylabel('Voltage (V)', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 3.3)
ax2.grid(True, alpha=0.3)
ax2.set_title('Voltage Reading (0-3.3V)', fontsize=14)
line2, = ax2.plot([], [], 'g-', linewidth=2, label='Voltage')
ax2.legend()

ax3.set_ylabel('Light Level (%)', fontsize=12, fontweight='bold')
ax3.set_ylim(0, 100)
ax3.set_xlabel('Time (seconds)', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.set_title('Light Level (0-100%)', fontsize=14)
line3, = ax3.plot([], [], 'r-', linewidth=2, label='Light Level')
ax3.legend()

# Add status text
status_text = fig.text(0.02, 0.02, '', fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))

# Serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"✅ Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
    print("📊 Real-time plotting started...")
    print("🔍 Close the plot window to stop")
except Exception as e:
    print(f"❌ Error connecting to serial port: {e}")
    exit(1)

def parse_data(line):
    """Parse data from ESP32 serial output"""
    try:
        if ',' in line:
            parts = line.strip().split(',')
            if len(parts) >= 4:
                adc = int(parts[0])
                voltage = float(parts[1])
                light = float(parts[2])
                status = int(parts[3])
                return adc, voltage, light, status
    except:
        pass
    return None

def serial_reader():
    """Background thread to read serial data"""
    while True:
        try:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    data = parse_data(line)
                    if data:
                        data_queue.put(data)
        except Exception as e:
            print(f"Serial read error: {e}")
        time.sleep(0.01)  # Small delay to prevent CPU overload

def get_status_text(status):
    """Convert status number to text"""
    status_map = {0: "มืด", 1: "แสงน้อย", 2: "แสงปานกลาง", 3: "แสงจ้า"}
    return status_map.get(status, "ไม่ทราบ")

def animate(frame):
    """Animation function for real-time plotting"""
    global adc_data, voltage_data, light_data, status_data, time_data
    
    # Process all available data from queue
    while not data_queue.empty():
        try:
            adc, voltage, light, status = data_queue.get_nowait()
            
            # Add to data arrays
            current_time = time.time()
            adc_data.append(adc)
            voltage_data.append(voltage)
            light_data.append(light)
            status_data.append(status)
            time_data.append(current_time)
            
        except queue.Empty:
            break
    
    # Update plots if we have data
    if len(time_data) > 1:
        # Convert time to relative seconds
        time_rel = [(t - time_data[0]) for t in time_data]
        
        # Update line data
        line1.set_data(time_rel, list(adc_data))
        line2.set_data(time_rel, list(voltage_data))
        line3.set_data(time_rel, list(light_data))
        
        # Update axis limits for real-time scrolling
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
        
        # Update status text
        if len(adc_data) > 0:
            current_status = get_status_text(status_data[-1])
            status_text.set_text(f'Current Status: {current_status} | '
                               f'ADC: {adc_data[-1]} | '
                               f'Voltage: {voltage_data[-1]:.2f}V | '
                               f'Light: {light_data[-1]:.1f}%')
        
        # Print current values with timestamp
        if len(adc_data) > 0:
            timestamp = time.strftime("%H:%M:%S")
            print(f"🕐 [{timestamp}] ADC: {adc_data[-1]:4d} | "
                  f"Voltage: {voltage_data[-1]:5.2f}V | "
                  f"Light: {light_data[-1]:5.1f}% | "
                  f"Status: {get_status_text(status_data[-1])}")
    
    return line1, line2, line3, status_text

# Start background serial reader thread
serial_thread = threading.Thread(target=serial_reader, daemon=True)
serial_thread.start()

# Start animation
print("🚀 Starting real-time animation...")
ani = animation.FuncAnimation(fig, animate, interval=UPDATE_INTERVAL, blit=False)

try:
    plt.tight_layout()
    plt.show()
except KeyboardInterrupt:
    print("\n⏹️  Stopping...")

# Cleanup
ser.close()
print("🔌 Serial connection closed")
print("👋 Goodbye!")
