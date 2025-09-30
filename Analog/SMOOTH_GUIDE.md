# 🌊 ESP32 LDR Ultra-Smooth Real-Time Plotting Guide

## 🎯 คุณสมบัติ Smooth Plotting

### **1. Easy Smooth Real-Time**
```bash
python3 easy_realtime.py
```
**คุณสมบัติ:**
- ✅ แสดงกราฟ 2 เส้น: Raw + Smooth
- ✅ Exponential smoothing
- ✅ Auto-scaling Y-axis
- ✅ Real-time updates ทุก 50ms
- ✅ Smoothing factor: 0.3

### **2. Ultra-Smooth Real-Time**
```bash
python3 smooth_realtime.py
```
**คุณสมบัติ:**
- ✅ แสดงกราฟ 2 เส้น: Raw + Ultra-Smooth
- ✅ Advanced smoothing algorithms
- ✅ Beautiful styling with seaborn
- ✅ Real-time updates ทุก 30ms
- ✅ Smoothing factor: 0.2 (ลื่นกว่า)

## 🔧 การปรับแต่ง Smoothing

### **ปรับ Smoothing Factor**
```python
# ในไฟล์ Python
SMOOTH_FACTOR = 0.1  # ลื่นมาก (ช้าในการตอบสนอง)
SMOOTH_FACTOR = 0.3  # ปานกลาง (แนะนำ)
SMOOTH_FACTOR = 0.5  # ลื่นน้อย (ตอบสนองเร็ว)
SMOOTH_FACTOR = 1.0  # ไม่ลื่น (แสดงข้อมูลดิบ)
```

### **ปรับความเร็ว Animation**
```python
# ในไฟล์ Python
UPDATE_INTERVAL = 20  # เร็วมาก (อาจทำให้ CPU หนัก)
UPDATE_INTERVAL = 30  # เร็ว (แนะนำ)
UPDATE_INTERVAL = 50  # ปานกลาง
UPDATE_INTERVAL = 100 # ช้า
```

### **ปรับจำนวนจุดข้อมูล**
```python
MAX_POINTS = 100   # น้อย (เร็ว)
MAX_POINTS = 200   # ปานกลาง (แนะนำ)
MAX_POINTS = 500   # มาก (ช้า)
```

## 📊 วิธีการใช้งาน

### **1. ติดตั้ง Dependencies**
```bash
pip install matplotlib pyserial numpy scipy seaborn
```

### **2. Flash โค้ด ESP32**
```bash
cd /Users/kbbk/Week-11-Microcontroller-applications/Analog
idf.py -p /dev/cu.usbserial-0001 flash monitor
```

### **3. รัน Smooth Plotter**
```bash
# แบบง่าย
python3 easy_realtime.py

# แบบลื่นมาก
python3 smooth_realtime.py
```

## 🎨 การปรับแต่งกราฟ

### **เปลี่ยนสีกราฟ**
```python
# ในไฟล์ Python
line1, = ax1.plot([], [], 'b-', linewidth=2, alpha=0.6, label='ADC Raw')
line1_smooth, = ax1.plot([], [], 'b-', linewidth=4, alpha=1.0, label='ADC Smooth')

# เปลี่ยนสี
line1, = ax1.plot([], [], 'r-', linewidth=2, alpha=0.6, label='ADC Raw')  # สีแดง
line1_smooth, = ax1.plot([], [], 'g-', linewidth=4, alpha=1.0, label='ADC Smooth')  # สีเขียว
```

### **เปลี่ยนความหนาของเส้น**
```python
linewidth=2   # บาง
linewidth=4   # หนา (แนะนำ)
linewidth=6   # หนามาก
```

### **เปลี่ยนความโปร่งใส**
```python
alpha=0.6   # โปร่งใส
alpha=0.8   # ปานกลาง
alpha=1.0   # ทึบ (แนะนำ)
```

## 🧪 การทดสอบ Smoothness

### **ทดสอบการเปลี่ยนแปลงแสง**
1. **ปิดไฟ** → ควรเห็นกราฟ Smooth ลดลงอย่างนุ่มนวล
2. **เปิดไฟ** → ควรเห็นกราฟ Smooth เพิ่มขึ้นอย่างนุ่มนวล
3. **ใช้มือบัง** → ควรเห็นการเปลี่ยนแปลงแบบเรียบ
4. **ใช้ไฟฉาย** → ควรเห็นการเปลี่ยนแปลงแบบนุ่มนวล

### **เปรียบเทียบ Raw vs Smooth**
- **Raw**: แสดงข้อมูลดิบจากเซนเซอร์ (อาจมี noise)
- **Smooth**: แสดงข้อมูลที่ผ่านการ smoothing (ลื่นกว่า)

## 🎯 Tips การใช้งาน

### **สำหรับการทดสอบเบื้องต้น**
- ใช้ `easy_realtime.py`
- Smoothing factor: 0.3
- Update interval: 50ms

### **สำหรับการวิเคราะห์ข้อมูล**
- ใช้ `smooth_realtime.py`
- Smoothing factor: 0.2
- Update interval: 30ms

### **สำหรับการแสดงผล**
- ใช้ `smooth_realtime.py`
- Smoothing factor: 0.1
- Update interval: 20ms

## 🐛 การแก้ไขปัญหา

### **ปัญหา: กราฟไม่ลื่น**
```python
# ลด smoothing factor
SMOOTH_FACTOR = 0.1

# เพิ่ม update frequency
UPDATE_INTERVAL = 20
```

### **ปัญหา: กราฟช้า**
```python
# เพิ่ม smoothing factor
SMOOTH_FACTOR = 0.5

# ลด update frequency
UPDATE_INTERVAL = 100
```

### **ปัญหา: CPU หนัก**
```python
# ลดจำนวนจุดข้อมูล
MAX_POINTS = 100

# เพิ่ม update interval
UPDATE_INTERVAL = 50
```

## 📈 ข้อมูลที่แสดง

### **รูปแบบข้อมูล**
```
1500,1.21,36.6,2
1600,1.30,39.0,2
1400,1.15,34.1,2
```

### **กราฟที่แสดง**
1. **ADC Raw**: ค่า ADC ดิบ (อาจมี noise)
2. **ADC Smooth**: ค่า ADC ที่ผ่านการ smoothing (ลื่น)
3. **Voltage Raw**: แรงดันดิบ
4. **Voltage Smooth**: แรงดันที่ผ่านการ smoothing
5. **Light Raw**: ระดับแสงดิบ
6. **Light Smooth**: ระดับแสงที่ผ่านการ smoothing

## 🎉 ผลลัพธ์ที่คาดหวัง

### **กราฟ Smooth ควรมีลักษณะ:**
- ✅ เส้นกราฟลื่น ไม่มี noise
- ✅ การเปลี่ยนแปลงนุ่มนวล
- ✅ ไม่มีการกระตุกของกราฟ
- ✅ แสดงแนวโน้มที่ชัดเจน

### **กราฟ Raw ควรมีลักษณะ:**
- ✅ เส้นกราฟอาจมี noise เล็กน้อย
- ✅ การเปลี่ยนแปลงทันที
- ✅ แสดงข้อมูลดิบจากเซนเซอร์
- ✅ มีการกระตุกเล็กน้อย

---

**🌊 ตอนนี้คุณสามารถ plot กราฟที่ลื่น smooth ได้แล้วครับ!**

