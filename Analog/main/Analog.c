// การทดลองที่ 1: อ่านค่า Potentiometer
// ตัวอย่างพื้นฐาน ADC ของ ESP32 โดยใช้ ESP-IDF v6.0

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"
#include "esp_log.h"
#include "driver/gpio.h"

// กำหนด pin ที่ใช้
#define POTENTIOMETER_CHANNEL ADC_CHANNEL_6  // GPIO34 (ADC1_CH6)
#define DEFAULT_VREF    1100        // ใช้ adc2_vref_to_gpio() เพื่อให้ได้ค่าประมาณที่ดีกว่า
#define NO_OF_SAMPLES   10          // ลดจำนวนตัวอย่างเพื่อ debug

static const char *TAG = "ADC_POT";
static adc_oneshot_unit_handle_t adc1_handle;
static adc_cali_handle_t adc1_cali_handle = NULL;

static bool adc_calibration_init(void)
{
    esp_err_t ret = ESP_FAIL;
    bool calibrated = false;

#if ADC_CALI_SCHEME_CURVE_FITTING_SUPPORTED
    if (!calibrated) {
        ESP_LOGI(TAG, "calibration scheme version is Curve Fitting");
        adc_cali_curve_fitting_config_t cali_config = {
            .unit_id = ADC_UNIT_1,
            .atten = ADC_ATTEN_DB_12,
            .bitwidth = ADC_BITWIDTH_12,
        };
        ret = adc_cali_create_scheme_curve_fitting(&cali_config, &adc1_cali_handle);
        if (ret == ESP_OK) {
            calibrated = true;
        }
    }
#endif

#if ADC_CALI_SCHEME_LINE_FITTING_SUPPORTED
    if (!calibrated) {
        ESP_LOGI(TAG, "calibration scheme version is Line Fitting");
        adc_cali_line_fitting_config_t cali_config = {
            .unit_id = ADC_UNIT_1,
            .atten = ADC_ATTEN_DB_12,
            .bitwidth = ADC_BITWIDTH_12,
        };
        ret = adc_cali_create_scheme_line_fitting(&cali_config, &adc1_cali_handle);
        if (ret == ESP_OK) {
            calibrated = true;
        }
    }
#endif

    return calibrated;
}

void app_main(void)
{
    ESP_LOGI(TAG, "=== เริ่มต้นการทดลอง ADC Potentiometer ===");
    
    // กำหนดค่า ADC
    adc_oneshot_unit_init_cfg_t init_config1 = {
        .unit_id = ADC_UNIT_1,
    };
    esp_err_t ret = adc_oneshot_new_unit(&init_config1, &adc1_handle);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "ADC unit init failed: %s", esp_err_to_name(ret));
        return;
    }
    ESP_LOGI(TAG, "✅ ADC unit initialized successfully");

    // กำหนดค่า channel
    adc_oneshot_chan_cfg_t config = {
        .bitwidth = ADC_BITWIDTH_12,
        .atten = ADC_ATTEN_DB_12,
    };
    ret = adc_oneshot_config_channel(adc1_handle, POTENTIOMETER_CHANNEL, &config);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "ADC channel config failed: %s", esp_err_to_name(ret));
        return;
    }
    ESP_LOGI(TAG, "✅ ADC channel configured successfully");

    // เริ่มต้นการปรับเทียบ
    bool do_calibration = adc_calibration_init();
    ESP_LOGI(TAG, "การปรับเทียบ: %s", do_calibration ? "เปิดใช้งาน" : "ปิดใช้งาน");

    ESP_LOGI(TAG, "=== ข้อมูลการตั้งค่า ===");
    ESP_LOGI(TAG, "Pin: GPIO34 (ADC1_CH6)");
    ESP_LOGI(TAG, "ช่วงแรงดัน: 0-3.3V");
    ESP_LOGI(TAG, "ความละเอียด: 12-bit (0-4095)");
    ESP_LOGI(TAG, "Attenuation: 12dB");
    ESP_LOGI(TAG, "จำนวนตัวอย่าง: %d", NO_OF_SAMPLES);
    ESP_LOGI(TAG, "=========================================");

    // ทดสอบการอ่านค่า ADC แบบง่าย
    ESP_LOGI(TAG, "🔍 เริ่มทดสอบการอ่านค่า ADC...");
    
    // อ่านค่า ADC1 อย่างต่อเนื่อง
    int loop_count = 0;
    while (1) {
        int adc_reading = 0;
        int min_val = 4095;
        int max_val = 0;
        
        // การสุ่มสัญญาณหลายครั้ง
        for (int i = 0; i < NO_OF_SAMPLES; i++) {
            int raw;
            ret = adc_oneshot_read(adc1_handle, POTENTIOMETER_CHANNEL, &raw);
            if (ret != ESP_OK) {
                ESP_LOGE(TAG, "ADC read failed: %s", esp_err_to_name(ret));
                continue;
            }
            adc_reading += raw;
            if (raw < min_val) min_val = raw;
            if (raw > max_val) max_val = raw;
        }
        adc_reading /= NO_OF_SAMPLES;
        
        // แปลง adc_reading เป็นแรงดัน
        int voltage_mv = (adc_reading * 3300) / 4095;
        float voltage = voltage_mv / 1000.0;
        
        // แปลงเป็นเปอร์เซ็นต์
        float percentage = (adc_reading / 4095.0) * 100.0;
        
        // แสดงผลลัพธ์การวัด
        ESP_LOGI(TAG, "📊 การวัดครั้งที่ %d:", loop_count + 1);
        ESP_LOGI(TAG, "   ADC Raw: %4d (ช่วง: %d-%d)", adc_reading, min_val, max_val);
        ESP_LOGI(TAG, "   แรงดัน: %5.2fV (%.1f%%)", voltage, percentage);
        ESP_LOGI(TAG, "   ความละเอียด: %.2fmV", voltage * 1000);
        
        // แสดงตำแหน่ง Potentiometer
        if (percentage < 5) {
            ESP_LOGI(TAG, "   ตำแหน่ง: ซ้ายสุด (0%)");
        } else if (percentage < 25) {
            ESP_LOGI(TAG, "   ตำแหน่ง: 1/4 (25%)");
        } else if (percentage < 50) {
            ESP_LOGI(TAG, "   ตำแหน่ง: 1/2 (50%)");
        } else if (percentage < 75) {
            ESP_LOGI(TAG, "   ตำแหน่ง: 3/4 (75%)");
        } else {
            ESP_LOGI(TAG, "   ตำแหน่ง: ขวาสุด (100%)");
        }
        
        // ตรวจสอบการเปลี่ยนแปลง
        if (loop_count > 0) {
            static int prev_reading = -1;
            if (prev_reading != -1) {
                int diff = adc_reading - prev_reading;
                float voltage_diff = (diff * 3.3) / 4095.0;
                if (abs(diff) > 10) {
                    ESP_LOGI(TAG, "   🔄 การเปลี่ยนแปลง: %d -> %d (diff: %d, %.2fV)", 
                             prev_reading, adc_reading, diff, voltage_diff);
                } else {
                    ESP_LOGW(TAG, "   ⚠️  ค่าไม่เปลี่ยนแปลงมาก (diff: %d)", diff);
                }
            }
            prev_reading = adc_reading;
        }
        
        // แสดงสถานะการทำงาน
        if (adc_reading < 100) {
            ESP_LOGI(TAG, "   สถานะ: ต่ำมาก (Low) - ใกล้ GND");
        } else if (adc_reading < 1000) {
            ESP_LOGI(TAG, "   สถานะ: ต่ำ (Low) - ใกล้ GND");
        } else if (adc_reading < 2000) {
            ESP_LOGI(TAG, "   สถานะ: ปานกลาง (Medium) - กลาง");
        } else if (adc_reading < 3000) {
            ESP_LOGI(TAG, "   สถานะ: สูง (High) - ใกล้ 3.3V");
        } else {
            ESP_LOGI(TAG, "   สถานะ: สูงมาก (Very High) - ใกล้ 3.3V");
        }
        
        // แสดงข้อมูลการวัดเพิ่มเติม
        ESP_LOGI(TAG, "   📈 ข้อมูลการวัด:");
        ESP_LOGI(TAG, "      - ความละเอียด ADC: 12-bit (0-4095)");
        ESP_LOGI(TAG, "      - ความละเอียดแรงดัน: %.3fV", 3.3/4095.0);
        ESP_LOGI(TAG, "      - ความละเอียดเปอร์เซ็นต์: %.2f%%", 100.0/4095.0);
        ESP_LOGI(TAG, "      - จำนวนตัวอย่าง: %d", NO_OF_SAMPLES);
        ESP_LOGI(TAG, "      - ช่วงการวัด: %d - %d", min_val, max_val);
        
        loop_count++;
        vTaskDelay(pdMS_TO_TICKS(1000));  // หน่วงเวลา 1 วินาที
    }
}