# 📊 ESP32 LDR Real-Time Plotting Guide

## 🚀 วิธีการใช้งาน Real-Time Plotting

### 1. **เตรียมความพร้อม**
```bash
# ติดตั้ง dependencies
pip install matplotlib pyserial numpy

# ตรวจสอบ port ของ ESP32
ls /dev/cu.usb*
# หรือ
ls /dev/ttyUSB*
```

### 2. **Flash โค้ด ESP32**
```bash
cd /Users/kbbk/Week-11-Microcontroller-applications/Analog
idf.py -p /dev/cu.usbserial-0001 flash monitor
```

### 3. **รัน Real-Time Plotter**

#### **แบบง่าย (แนะนำ)**
```bash
python3 easy_realtime.py
```

#### **แบบเต็มรูปแบบ**
```bash
python3 realtime_plot.py
```

## 📈 คุณสมบัติ Real-Time Plotting

### **Easy Real-Time Plotter**
- ✅ แสดงกราฟ 3 เส้น: ADC, Voltage, Light Level
- ✅ Auto-scrolling (แสดง 20 วินาทีล่าสุด)
- ✅ Real-time updates ทุก 100ms
- ✅ แสดงค่าปัจจุบันใน console

### **Full Real-Time Plotter**
- ✅ แสดงกราฟ 3 เส้นพร้อม styling สวยงาม
- ✅ Auto-scaling Y-axis
- ✅ Status text แสดงสถานะปัจจุบัน
- ✅ Background threading สำหรับ serial reading
- ✅ Smooth animations
- ✅ Real-time updates ทุก 50ms

## 🔧 การปรับแต่ง

### **เปลี่ยน Serial Port**
แก้ไขในไฟล์ Python:
```python
SERIAL_PORT = '/dev/cu.usbserial-0001'  # เปลี่ยนเป็น port ของคุณ
```

### **ปรับความเร็ว**
```python
# ใน easy_realtime.py
ani = animation.FuncAnimation(fig, animate, interval=50, blit=False)  # เร็วขึ้น

# ใน realtime_plot.py
UPDATE_INTERVAL = 25  # เร็วขึ้น
```

### **ปรับจำนวนจุดข้อมูล**
```python
MAX_POINTS = 200  # เพิ่มจำนวนจุดที่แสดง
```

## 📊 ข้อมูลที่แสดง

### **รูปแบบข้อมูลจาก ESP32**
```
1500,1.21,36.6,2
1600,1.30,39.0,2
1400,1.15,34.1,2
```

**ความหมาย:**
- **คอลัมน์ 1**: ADC Value (0-4095)
- **คอลัมน์ 2**: Voltage (0-3.3V)
- **คอลัมน์ 3**: Light Level (0-100%)
- **คอลัมน์ 4**: Status (0=มืด, 1=แสงน้อย, 2=ปานกลาง, 3=แสงจ้า)

### **กราฟที่แสดง**
1. **ADC Reading**: ค่า ADC แบบ raw (0-4095)
2. **Voltage**: แรงดันที่วัดได้ (0-3.3V)
3. **Light Level**: ระดับแสงเป็นเปอร์เซ็นต์ (0-100%)

## 🧪 การทดสอบ

### **ทดสอบการเปลี่ยนแปลงแสง**
1. **ปิดไฟ** → ควรเห็นค่า ADC ต่ำ, แรงดันต่ำ, ระดับแสงต่ำ
2. **เปิดไฟ** → ควรเห็นค่า ADC สูง, แรงดันสูง, ระดับแสงสูง
3. **ใช้มือบัง** → ควรเห็นการเปลี่ยนแปลงแบบเรียลไทม์
4. **ใช้ไฟฉาย** → ควรเห็นค่าเพิ่มขึ้นทันที

### **ทดสอบความเร็ว**
- กราฟควรอัปเดตทุก 100ms (easy) หรือ 50ms (full)
- การเปลี่ยนแปลงแสงควรเห็นได้ทันที
- กราฟควรเลื่อนไปทางขวาอัตโนมัติ

## 🐛 การแก้ไขปัญหา

### **ปัญหา: ไม่เห็นกราฟ**
```bash
# ตรวจสอบ serial port
ls /dev/cu.usb*

# ตรวจสอบ baud rate
# ต้องเป็น 115200
```

### **ปัญหา: กราฟไม่อัปเดต**
```bash
# ตรวจสอบว่า ESP32 ส่งข้อมูล
# ควรเห็นข้อมูลใน console
```

### **ปัญหา: กราฟช้า**
```python
# ลด interval
ani = animation.FuncAnimation(fig, animate, interval=25, blit=False)
```

## 🎯 Tips การใช้งาน

1. **ใช้ easy_realtime.py** สำหรับการทดสอบเบื้องต้น
2. **ใช้ realtime_plot.py** สำหรับการวิเคราะห์ข้อมูล
3. **ปิด terminal อื่น** ที่ใช้ serial port เดียวกัน
4. **ใช้ USB cable ที่ดี** เพื่อความเสถียร
5. **ทดสอบในสภาพแสงต่างๆ** เพื่อดูการเปลี่ยนแปลง

## 📱 การใช้งานกับ Arduino IDE Serial Plotter

หากต้องการใช้ Arduino IDE Serial Plotter:
1. เปิด Arduino IDE
2. ไปที่ `Tools` → `Serial Plotter`
3. ตั้งค่า Baud Rate เป็น `115200`
4. เลือก Port ที่ถูกต้อง
5. คุณจะเห็นกราฟ 4 เส้นพร้อมกัน

---

**🎉 ตอนนี้คุณสามารถ plot กราฟ real-time ได้แล้วครับ!**

