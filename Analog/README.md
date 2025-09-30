# ESP32 ADC Experiments - Week 11

โปรเจคนี้ประกอบด้วยการทดลอง ADC (Analog-to-Digital Converter) สำหรับ ESP32 โดยใช้ ESP-IDF v6.0

## การทดลองที่มี

### การทดลองที่ 1: อ่านค่า Potentiometer
- **ไฟล์**: `main/Analog.c`
- **วัตถุประสงค์**: การอ่านค่าพื้นฐานจาก Potentiometer
- **Pin**: GPIO34 (ADC1_CH6)
- **Features**:
  - 12-bit ADC resolution (0-4095)
  - Voltage conversion with calibration
  - Percentage calculation
  - Oversampling for better accuracy
  - Error handling and fallback

## วงจรการต่อ

### Potentiometer Circuit
```
Potentiometer 10kΩ:
- ขา 1 (GND) → GND
- ขา 2 (Wiper) → GPIO34 (ADC1_CH6)
- ขา 3 (VCC) → 3.3V
```

## วิธีการใช้งาน

### 1. เตรียมอุปกรณ์
- ESP32 Development Board
- Potentiometer 10kΩ
- Breadboard และสายไฟ
- USB Cable

### 2. Build และ Flash

```bash
# ไปที่โฟลเดอร์โปรเจค
cd /Users/kbbk/Week-11-Microcontroller-applications/Analog

# ตั้งค่า ESP-IDF environment
source ~/esp/esp-idf/export.sh

# ตั้งค่า target
idf.py set-target esp32

# Build โปรเจค
idf.py build

# Flash ไปยัง ESP32 (เปลี่ยน /dev/ttyUSB0 เป็น port ของคุณ)
idf.py -p /dev/ttyUSB0 flash

# Monitor serial output
idf.py -p /dev/ttyUSB0 monitor
```

### 3. การใช้งาน
1. ต่อวงจรตามแผนภาพ
2. Flash โค้ดไปยัง ESP32
3. เปิด Serial Monitor (115200 baud)
4. หมุน Potentiometer เพื่อดูการเปลี่ยนแปลงค่า

## ผลลัพธ์ที่คาดหวัง

```
I (1234) ADC_POT: === การทดลอง ADC Potentiometer ESP32 ===
I (1234) ADC_POT: Pin: GPIO34 (ADC1_CH6)
I (1234) ADC_POT: ช่วงแรงดัน: 0-3.3V
I (1234) ADC_POT: ความละเอียด: 12-bit (0-4095)
I (1234) ADC_POT: Attenuation: 12dB
I (1234) ADC_POT: การปรับเทียบ: เปิดใช้งาน
I (1234) ADC_POT: จำนวนตัวอย่าง: 64
I (1234) ADC_POT: =========================================
I (1234) ADC_POT: ADC: 2048 | แรงดัน: 1.65V | เปอร์เซ็นต์: 50.0%
I (1234) ADC_POT: สถานะ: ปานกลาง (Medium)
```

## คุณสมบัติของโค้ด

### 1. การปรับเทียบ ADC
- รองรับ Curve Fitting และ Line Fitting
- Fallback ไปยังการคำนวณแบบง่ายหากการปรับเทียบล้มเหลว

### 2. การสุ่มตัวอย่าง
- ใช้ Oversampling 64 ครั้งต่อการอ่าน
- ลดสัญญาณรบกวนและเพิ่มความแม่นยำ

### 3. การแสดงผล
- แสดงค่า ADC, แรงดัน, และเปอร์เซ็นต์
- แสดงสถานะการทำงาน (ต่ำ, ปานกลาง, สูง)
- ข้อมูลการตั้งค่าที่ชัดเจน

### 4. การจัดการ Error
- ตรวจสอบการทำงานของ ADC
- แสดงข้อความเตือนเมื่อเกิดข้อผิดพลาด
- Fallback mechanism

## การแก้ไขปัญหา

1. **"idf.py command not found"**: 
   ```bash
   source ~/esp/esp-idf/export.sh
   ```

2. **Build errors**: 
   - ตรวจสอบว่า ESP-IDF v6.0 ติดตั้งถูกต้อง
   - รัน `idf.py fullclean` แล้วลองใหม่

3. **Flash errors**: 
   - ตรวจสอบการเชื่อมต่อ USB
   - ตรวจสอบ port (ใช้ `ls /dev/tty*` หรือ `ls /dev/cu*`)

4. **No serial output**: 
   - ตรวจสอบ baud rate (115200)
   - ตรวจสอบการเชื่อมต่อสาย

5. **ค่า ADC ไม่เปลี่ยนแปลง**:
   - ตรวจสอบการต่อวงจร
   - ตรวจสอบว่า Potentiometer ทำงานถูกต้อง

## วัตถุประสงค์การเรียนรู้

- เข้าใจหลักการทำงานของ ADC ใน ESP32
- เรียนรู้การปรับเทียบ ADC
- ฝึกใช้เทคนิคการปรับปรุงความแม่นยำ
- เรียนรู้การจัดการ Error
- นำความรู้ไปประยุกต์ใช้ในโปรเจคจริง

## การพัฒนาต่อ

- เพิ่มการทดลอง LDR (Light Sensor)
- เพิ่มการทดลอง Temperature Sensor
- เพิ่มการทดลอง Enhanced ADC with Filtering
- เพิ่มการส่งข้อมูลผ่าน WiFi
