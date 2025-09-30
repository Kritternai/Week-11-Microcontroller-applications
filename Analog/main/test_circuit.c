// โค้ดทดสอบวงจร Potentiometer
// ใช้เพื่อตรวจสอบการต่อวงจรที่ถูกต้อง

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_log.h"

#define POTENTIOMETER_CHANNEL ADC_CHANNEL_6  // GPIO34
#define NO_OF_SAMPLES   5

static const char *TAG = "TEST_CIRCUIT";
static adc_oneshot_unit_handle_t adc1_handle;

void app_main(void)
{
    ESP_LOGI(TAG, "=== ทดสอบวงจร Potentiometer ===");
    
    // กำหนดค่า ADC
    adc_oneshot_unit_init_cfg_t init_config1 = {
        .unit_id = ADC_UNIT_1,
    };
    ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config1, &adc1_handle));

    // กำหนดค่า channel
    adc_oneshot_chan_cfg_t config = {
        .bitwidth = ADC_BITWIDTH_12,
        .atten = ADC_ATTEN_DB_12,
    };
    ESP_ERROR_CHECK(adc_oneshot_config_channel(adc1_handle, POTENTIOMETER_CHANNEL, &config));

    ESP_LOGI(TAG, "🔧 วิธีต่อวงจร:");
    ESP_LOGI(TAG, "   Potentiometer ขา 1 (ซ้าย) → GND");
    ESP_LOGI(TAG, "   Potentiometer ขา 2 (กลาง) → GPIO34");
    ESP_LOGI(TAG, "   Potentiometer ขา 3 (ขวา) → 3.3V");
    ESP_LOGI(TAG, "");
    ESP_LOGI(TAG, "📊 ค่าที่คาดหวัง (หมุนซ้ายไปขวา = น้อยไปมาก):");
    ESP_LOGI(TAG, "   หมุนซ้ายสุด: ADC ≈ 0 (0V) - ค่าน้อยที่สุด");
    ESP_LOGI(TAG, "   หมุนขวาสุด: ADC ≈ 4095 (3.3V) - ค่ามากที่สุด");
    ESP_LOGI(TAG, "   หมุนตรงกลาง: ADC ≈ 2048 (1.65V) - ค่ากลาง");
    ESP_LOGI(TAG, "");
    ESP_LOGI(TAG, "🔄 ทดสอบ: หมุนจากซ้ายไปขวา ค่าควรเพิ่มขึ้น");
    ESP_LOGI(TAG, "=========================================");

    int loop_count = 0;
    while (1) {
        int adc_reading = 0;
        
        // อ่านค่า ADC
        for (int i = 0; i < NO_OF_SAMPLES; i++) {
            int raw;
            ESP_ERROR_CHECK(adc_oneshot_read(adc1_handle, POTENTIOMETER_CHANNEL, &raw));
            adc_reading += raw;
        }
        adc_reading /= NO_OF_SAMPLES;
        
        // แปลงเป็นแรงดัน
        float voltage = (adc_reading * 3.3) / 4095.0;
        float percentage = (adc_reading / 4095.0) * 100.0;
        
        // แสดงผลลัพธ์
        ESP_LOGI(TAG, "📊 Loop %d: ADC=%4d | แรงดัน=%5.2fV | เปอร์เซ็นต์=%5.1f%%", 
                 loop_count, adc_reading, voltage, percentage);
        
        // วิเคราะห์ผลลัพธ์
        if (adc_reading < 50) {
            ESP_LOGI(TAG, "✅ หมุนซ้ายสุด - ค่าน้อยที่สุด (ถูกต้อง!)");
        } else if (adc_reading > 4045) {
            ESP_LOGI(TAG, "✅ หมุนขวาสุด - ค่ามากที่สุด (ถูกต้อง!)");
        } else if (adc_reading > 1900 && adc_reading < 2200) {
            ESP_LOGI(TAG, "✅ หมุนตรงกลาง - ค่ากลาง (ถูกต้อง!)");
        } else if (adc_reading < 100) {
            ESP_LOGI(TAG, "🔍 ใกล้ซ้ายสุด - ลองหมุนไปทางซ้ายมากขึ้น");
        } else if (adc_reading > 4000) {
            ESP_LOGI(TAG, "🔍 ใกล้ขวาสุด - ลองหมุนไปทางขวามากขึ้น");
        } else {
            ESP_LOGI(TAG, "🔍 ตำแหน่งกลาง - ลองหมุนดูการเปลี่ยนแปลง");
        }
        
        // แสดงทิศทางการหมุน
        if (loop_count > 0) {
            static int prev_reading = -1;
            if (prev_reading != -1) {
                int diff = adc_reading - prev_reading;
                if (diff > 20) {
                    ESP_LOGI(TAG, "🔄 หมุนไปทางขวา - ค่าเพิ่มขึ้น: %d -> %d (+%d)", prev_reading, adc_reading, diff);
                } else if (diff < -20) {
                    ESP_LOGI(TAG, "🔄 หมุนไปทางซ้าย - ค่าลดลง: %d -> %d (%d)", prev_reading, adc_reading, diff);
                } else if (abs(diff) < 5) {
                    ESP_LOGW(TAG, "⚠️  ค่าไม่เปลี่ยนแปลง (diff: %d) - ตรวจสอบการต่อวงจร!", diff);
                }
            }
            prev_reading = adc_reading;
        }
        
        loop_count++;
        vTaskDelay(pdMS_TO_TICKS(2000));  // หน่วงเวลา 2 วินาที
    }
}
