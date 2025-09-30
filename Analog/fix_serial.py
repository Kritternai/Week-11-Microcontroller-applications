#!/usr/bin/env python3
"""
ESP32 LDR Serial Connection Fixer
แก้ไขปัญหา serial connection และทดสอบการเชื่อมต่อ
"""

import serial
import time
import sys

def check_serial_ports():
    """ตรวจสอบ serial ports ที่มีอยู่"""
    import serial.tools.list_ports
    
    print("🔍 ตรวจสอบ Serial Ports ที่มีอยู่:")
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("❌ ไม่พบ serial ports")
        return []
    
    for i, port in enumerate(ports):
        print(f"  {i+1}. {port.device} - {port.description}")
    
    return [port.device for port in ports]

def test_serial_connection(port, baud_rate=115200):
    """ทดสอบการเชื่อมต่อ serial"""
    print(f"\n🔌 ทดสอบการเชื่อมต่อ {port}...")
    
    try:
        ser = serial.Serial(port, baud_rate, timeout=2)
        print(f"✅ เชื่อมต่อสำเร็จ: {port}")
        
        # รอข้อมูล 5 วินาที
        print("⏳ รอข้อมูลจาก ESP32 (5 วินาที)...")
        start_time = time.time()
        data_received = False
        
        while time.time() - start_time < 5:
            if ser.in_waiting:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        print(f"📊 ข้อมูลที่ได้รับ: {line}")
                        data_received = True
                except:
                    pass
            time.sleep(0.1)
        
        if data_received:
            print("✅ ESP32 ส่งข้อมูลได้ปกติ")
        else:
            print("⚠️  ESP32 ไม่ส่งข้อมูล")
            print("💡 ตรวจสอบว่า ESP32 กำลังรันโค้ดหรือไม่")
        
        ser.close()
        return True
        
    except Exception as e:
        print(f"❌ ไม่สามารถเชื่อมต่อได้: {e}")
        return False

def fix_serial_connection():
    """แก้ไขปัญหา serial connection"""
    print("🔧 ESP32 Serial Connection Fixer")
    print("=" * 50)
    
    # ตรวจสอบ ports
    ports = check_serial_ports()
    
    if not ports:
        print("\n❌ ไม่พบ serial ports")
        print("💡 ตรวจสอบว่า ESP32 เชื่อมต่อแล้วหรือไม่")
        return None
    
    # ทดสอบแต่ละ port
    working_ports = []
    for port in ports:
        if test_serial_connection(port):
            working_ports.append(port)
    
    if working_ports:
        print(f"\n✅ Ports ที่ใช้งานได้: {working_ports}")
        return working_ports[0]
    else:
        print("\n❌ ไม่มี port ที่ใช้งานได้")
        return None

def create_working_plotter(port):
    """สร้าง plotter ที่ใช้งานได้"""
    plotter_code = f'''#!/usr/bin/env python3
"""
ESP32 LDR Working Real-Time Plotter
แก้ไขปัญหา serial connection แล้ว
"""

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import time

# Configuration
SERIAL_PORT = '{port}'  # Port ที่แก้ไขแล้ว
BAUD_RATE = 115200
MAX_POINTS = 100

# Data storage
adc_data = deque(maxlen=MAX_POINTS)
voltage_data = deque(maxlen=MAX_POINTS)
light_data = deque(maxlen=MAX_POINTS)
time_data = deque(maxlen=MAX_POINTS)

# Initialize plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))
fig.suptitle('ESP32 LDR Real-Time Monitor (Fixed)', fontsize=16)

# Setup subplots
ax1.set_ylabel('ADC Value')
ax1.set_ylim(0, 4095)
ax1.grid(True)
line1, = ax1.plot([], [], 'b-', linewidth=2)

ax2.set_ylabel('Voltage (V)')
ax2.set_ylim(0, 3.3)
ax2.grid(True)
line2, = ax2.plot([], [], 'g-', linewidth=2)

ax3.set_ylabel('Light Level (%)')
ax3.set_ylim(0, 100)
ax3.set_xlabel('Time (seconds)')
ax3.grid(True)
line3, = ax3.plot([], [], 'r-', linewidth=2)

# Serial connection with error handling
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"✅ Connected to {{SERIAL_PORT}}")
    print("📊 Real-time plotting started...")
    print("🔍 Close the plot window to stop")
except Exception as e:
    print(f"❌ Error: {{e}}")
    print("💡 ตรวจสอบว่า ESP32 เชื่อมต่อแล้วหรือไม่")
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

def animate(frame):
    """Real-time animation"""
    global adc_data, voltage_data, light_data, time_data
    
    # Read data from serial with error handling
    try:
        if ser.in_waiting:
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
                    
                    # Print current values
                    print(f"ADC: {{adc:4d}} | Voltage: {{voltage:5.2f}}V | Light: {{light:5.1f}}%")
    except Exception as e:
        print(f"Serial read error: {{e}}")
        # ไม่ต้องหยุดการทำงาน
    
    # Update plots
    if len(time_data) > 1:
        # Convert time to relative seconds
        time_rel = [(t - time_data[0]) for t in time_data]
        
        # Update line data
        line1.set_data(time_rel, list(adc_data))
        line2.set_data(time_rel, list(voltage_data))
        line3.set_data(time_rel, list(light_data))
        
        # Update axis limits for scrolling
        if len(time_rel) > 1:
            x_min = max(0, time_rel[-1] - 20)
            x_max = time_rel[-1] + 1
            
            ax1.set_xlim(x_min, x_max)
            ax2.set_xlim(x_min, x_max)
            ax3.set_xlim(x_min, x_max)
    
    return line1, line2, line3

# Start animation
print("🚀 Starting animation...")
ani = animation.FuncAnimation(fig, animate, interval=100, blit=False)

try:
    plt.tight_layout()
    plt.show()
except KeyboardInterrupt:
    print("\\n⏹️  Stopping...")

# Cleanup
ser.close()
print("🔌 Serial connection closed")
'''
    
    with open('/Users/kbbk/Week-11-Microcontroller-applications/Analog/working_plotter.py', 'w') as f:
        f.write(plotter_code)
    
    print(f"\n✅ สร้างไฟล์ working_plotter.py สำหรับ port {port}")

if __name__ == "__main__":
    # แก้ไขปัญหา serial connection
    working_port = fix_serial_connection()
    
    if working_port:
        print(f"\n🎯 ใช้ port: {working_port}")
        create_working_plotter(working_port)
        print("\n🚀 วิธีใช้งาน:")
        print("1. Flash โค้ด ESP32:")
        print(f"   idf.py -p {working_port} flash monitor")
        print("2. รัน plotter:")
        print("   python3 working_plotter.py")
    else:
        print("\n💡 วิธีแก้ไข:")
        print("1. ตรวจสอบว่า ESP32 เชื่อมต่อแล้ว")
        print("2. ตรวจสอบว่าไม่มีโปรแกรมอื่นใช้ serial port")
        print("3. ลองเปลี่ยน USB cable")
        print("4. ลองเปลี่ยน USB port")

