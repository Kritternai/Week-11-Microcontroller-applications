// การทดลองที่ 2: เซนเซอร์แสง LDR
// Light Sensor with ESP32 ADC using ESP-IDF v6.0

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"
#include "esp_log.h"

// กำหนด pin ที่ใช้
#define LDR_CHANNEL ADC_CHANNEL_7  // GPIO35 (ADC1_CH7)
#define DEFAULT_VREF    1100        // ใช้ adc2_vref_to_gpio() เพื่อให้ได้ค่าประมาณที่ดีกว่า
#define NO_OF_SAMPLES   64          // การสุ่มสัญญาณหลายครั้ง

static const char *TAG = "ADC_LDR";
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
    ESP_LOGI(TAG, "=== เริ่มต้นการทดลอง ADC LDR ===");
    
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
    ESP_ERROR_CHECK(adc_oneshot_config_channel(adc1_handle, LDR_CHANNEL, &config));

    // เริ่มต้นการปรับเทียบ
    bool do_calibration = adc_calibration_init();

    ESP_LOGI(TAG, "ทดสอบเซนเซอร์แสง LDR ของ ESP32");
    ESP_LOGI(TAG, "Pin: GPIO35 (ADC1_CH7)");
    ESP_LOGI(TAG, "ช่วง: 0-3.3V");
    ESP_LOGI(TAG, "ความละเอียด: 12-bit (0-4095)");
    ESP_LOGI(TAG, "Attenuation: 12dB");
    ESP_LOGI(TAG, "การปรับเทียบ: %s", do_calibration ? "เปิดใช้งาน" : "ปิดใช้งาน");
    ESP_LOGI(TAG, "------------------------");

    // อ่านค่า ADC จาก LDR อย่างต่อเนื่อง
    while (1) {
        int adc_reading = 0;
        
        // การสุ่มสัญญาณหลายครั้ง
        for (int i = 0; i < NO_OF_SAMPLES; i++) {
            int raw;
            ESP_ERROR_CHECK(adc_oneshot_read(adc1_handle, LDR_CHANNEL, &raw));
            adc_reading += raw;
        }
        adc_reading /= NO_OF_SAMPLES;
        
        // แปลง adc_reading เป็นแรงดัน
        int voltage_mv = 0;
        if (do_calibration) {
            esp_err_t ret = adc_cali_raw_to_voltage(adc1_cali_handle, adc_reading, &voltage_mv);
            if (ret != ESP_OK) {
                ESP_LOGW(TAG, "การแปลงแรงดันล้มเหลว: %s", esp_err_to_name(ret));
                voltage_mv = (adc_reading * 3300) / 4095;
            }
        } else {
            voltage_mv = (adc_reading * 3300) / 4095;
        }
        float voltage = voltage_mv / 1000.0;
        
        // แปลงเป็นระดับแสง (สมมติ)
        float lightLevel = (adc_reading / 4095.0) * 100.0;
        
        // กำหนดสถานะแสง
        const char* lightStatus;
        if (lightLevel < 20) {
            lightStatus = "มืด";
        } else if (lightLevel < 50) {
            lightStatus = "แสงน้อย";
        } else if (lightLevel < 80) {
            lightStatus = "แสงปานกลาง";
        } else {
            lightStatus = "แสงจ้า";
        }
        
        // แสดงผลลัพธ์แบบ Serial Plotter
        printf("ADC:%d,Voltage:%.2f,LightLevel:%.1f\n", adc_reading, voltage, lightLevel);
        
        // แสดงผลลัพธ์แบบปกติ
        ESP_LOGI(TAG, "ADC: %d | แรงดัน: %.2fV | ระดับแสง: %.1f%% | สถานะ: %s", 
                 adc_reading, voltage, lightLevel, lightStatus);
        
        vTaskDelay(pdMS_TO_TICKS(1000));  // หน่วงเวลา 1 วินาที
    }
}
