#!/usr/bin/env python3
"""
ESP32 LDR Simple Serial Test
ทดสอบการเชื่อมต่อ serial และแสดงข้อมูล
"""

import serial
import time

# Configuration
SERIAL_PORT = '/dev/cu.usbserial-0001'  # Change to your port
BAUD_RATE = 115200

def test_serial_connection():
    """ทดสอบการเชื่อมต่อ serial"""
    print("🔌 ทดสอบการเชื่อมต่อ ESP32...")
    print(f"Port: {SERIAL_PORT}")
    print(f"Baud Rate: {BAUD_RATE}")
    print("=" * 50)
    
    try:
        # เชื่อมต่อ serial
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        print("✅ เชื่อมต่อสำเร็จ!")
        
        # รอข้อมูล 10 วินาที
        print("⏳ รอข้อมูลจาก ESP32 (10 วินาที)...")
        print("💡 ถ้าไม่เห็นข้อมูล ให้ตรวจสอบว่า ESP32 กำลังรันโค้ดหรือไม่")
        print("=" * 50)
        
        start_time = time.time()
        data_count = 0
        
        while time.time() - start_time < 10:
            if ser.in_waiting:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        data_count += 1
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"[{timestamp}] 📊 {line}")
                except Exception as e:
                    print(f"❌ ข้อผิดพลาดในการอ่านข้อมูล: {e}")
            time.sleep(0.1)
        
        if data_count > 0:
            print("=" * 50)
            print(f"✅ ได้รับข้อมูล {data_count} บรรทัด")
            print("🎉 ESP32 ทำงานได้ปกติ!")
        else:
            print("=" * 50)
            print("⚠️  ไม่ได้รับข้อมูลจาก ESP32")
            print("💡 ตรวจสอบว่า:")
            print("   1. ESP32 กำลังรันโค้ดหรือไม่")
            print("   2. โค้ดถูก flash แล้วหรือไม่")
            print("   3. ESP32 ส่งข้อมูลหรือไม่")
        
        ser.close()
        print("🔌 ปิดการเชื่อมต่อ")
        
    except Exception as e:
        print(f"❌ ไม่สามารถเชื่อมต่อได้: {e}")
        print("💡 ตรวจสอบว่า:")
        print("   1. ESP32 เชื่อมต่อแล้วหรือไม่")
        print("   2. Port ถูกต้องหรือไม่")
        print("   3. ไม่มีโปรแกรมอื่นใช้ port เดียวกัน")

if __name__ == "__main__":
    test_serial_connection()

