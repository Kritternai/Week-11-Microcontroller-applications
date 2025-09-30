# ตัวอย่างการใช้งาน ESP32 ADC

## ขั้นตอนการทดลอง

### 1. เตรียมอุปกรณ์
```
- ESP32 Development Board
- Potentiometer 10kΩ
- Breadboard
- สายไฟ (Male-to-Male)
- USB Cable
```

### 2. ต่อวงจร
```
ESP32          Potentiometer
-----          ------------
GND     →      ขา 1 (GND)
GPIO34  →      ขา 2 (Wiper)
3.3V    →      ขา 3 (VCC)
```

### 3. Build และ Flash
```bash
# ไปที่โฟลเดอร์โปรเจค
cd /Users/kbbk/Week-11-Microcontroller-applications/Analog

# ตั้งค่า ESP-IDF environment
source ~/esp/esp-idf/export.sh

# Build โปรเจค
idf.py build

# Flash ไปยัง ESP32
idf.py -p /dev/ttyUSB0 flash monitor
```

### 4. ดูผลลัพธ์
เมื่อโปรแกรมทำงาน คุณจะเห็นผลลัพธ์ดังนี้:

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

### 5. ทดลอง
- หมุน Potentiometer ไปทางซ้าย (ค่า ADC จะลดลง)
- หมุน Potentiometer ไปทางขวา (ค่า ADC จะเพิ่มขึ้น)
- สังเกตการเปลี่ยนแปลงของค่า ADC, แรงดัน, และเปอร์เซ็นต์

## การตีความผลลัพธ์

### ค่า ADC
- **0-100**: ต่ำมาก (Low)
- **100-1000**: ต่ำ (Low)
- **1000-2000**: ปานกลาง (Medium)
- **2000-3000**: สูง (High)
- **3000-4095**: สูงมาก (Very High)

### แรงดัน
- **0V**: Potentiometer หมุนไปทางซ้ายสุด
- **1.65V**: Potentiometer อยู่ตรงกลาง
- **3.3V**: Potentiometer หมุนไปทางขวาสุด

### เปอร์เซ็นต์
- **0%**: Potentiometer หมุนไปทางซ้ายสุด
- **50%**: Potentiometer อยู่ตรงกลาง
- **100%**: Potentiometer หมุนไปทางขวาสุด

## การแก้ไขปัญหา

### ปัญหา: ค่า ADC ไม่เปลี่ยนแปลง
**สาเหตุ**: การต่อวงจรไม่ถูกต้อง
**วิธีแก้**: ตรวจสอบการต่อสายไฟ

### ปัญหา: ค่า ADC เปลี่ยนแปลงไม่สม่ำเสมอ
**สาเหตุ**: Potentiometer เสื่อมหรือการต่อไม่แน่น
**วิธีแก้**: เปลี่ยน Potentiometer ใหม่หรือตรวจสอบการต่อ

### ปัญหา: ไม่มี Serial Output
**สาเหตุ**: Port ไม่ถูกต้องหรือ Baud Rate ผิด
**วิธีแก้**: ตรวจสอบ Port และใช้ Baud Rate 115200

## การพัฒนาต่อ

### 1. เพิ่ม LED Indicator
```c
// เพิ่ม LED ที่ GPIO2
#define LED_PIN 2
gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);

// ในลูปหลัก
if (percentage > 50) {
    gpio_set_level(LED_PIN, 1);  // เปิด LED
} else {
    gpio_set_level(LED_PIN, 0);  // ปิด LED
}
```

### 2. เพิ่ม Buzzer
```c
// เพิ่ม Buzzer ที่ GPIO4
#define BUZZER_PIN 4
gpio_set_direction(BUZZER_PIN, GPIO_MODE_OUTPUT);

// ในลูปหลัก
if (percentage > 80) {
    gpio_set_level(BUZZER_PIN, 1);  // เปิด Buzzer
} else {
    gpio_set_level(BUZZER_PIN, 0);  // ปิด Buzzer
}
```

### 3. เพิ่ม WiFi และส่งข้อมูล
```c
// ส่งข้อมูลไปยัง Server
void send_data_to_server(int adc_value, float voltage, float percentage) {
    // สร้าง JSON payload
    char payload[200];
    snprintf(payload, sizeof(payload), 
        "{\"adc\":%d,\"voltage\":%.2f,\"percentage\":%.1f}", 
        adc_value, voltage, percentage);
    
    // ส่งข้อมูลไปยัง Server
    // ... HTTP POST code ...
}
```

## ข้อควรระวัง

1. **แรงดัน**: อย่าใช้แรงดันเกิน 3.3V ที่ GPIO
2. **กระแส**: ตรวจสอบกระแสที่ดึงจาก ESP32
3. **Ground**: ต้องต่อ Ground ให้ถูกต้อง
4. **สายไฟ**: ใช้สายไฟที่เหมาะสมและต่อให้แน่น

## การวัดประสิทธิภาพ

### ความแม่นยำ
- ใช้ Multimeter วัดแรงดันจริง
- เปรียบเทียบกับค่าที่แสดงใน Serial Monitor
- คำนวณ Error Percentage

### ความเสถียร
- วัดค่า ADC หลายครั้ง
- คำนวณ Standard Deviation
- ตรวจสอบการเปลี่ยนแปลงของค่า

### Response Time
- วัดเวลาตอบสนองเมื่อหมุน Potentiometer
- ตรวจสอบการอัพเดทของค่า
