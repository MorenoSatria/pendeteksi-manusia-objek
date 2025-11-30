# Iot (hcsr04) /w dashboard
Tugas akhir semester, Mapel Pemrograman Web Tingkat Lanjut. Dibimbing oleh P. Panca Wardani.

## Instalasi Project
Bagaimana cara menjalankan project ini? Ikuti langkah-langkah dibawah ini.

### pertama-tama siapkan alat-alat dulu
- esp32
- HCSR04
- kabel
- buzzer
  
### pada bagian wiring
-HC-SR04 VCC  → 3.3V ESP32 (bisa juga 5V tergantung modul)
-HC-SR04 GND  → GND ESP32
-HC-SR04 TRIG → GPIO 5
-HC-SR04 ECHO → GPIO 18
Buzzer + (warna putih) → GPIO 4
Buzzer - (warna hitam) → GND ESP32

### jika sudah clone branch ini

```bash
git clone -b main https://github.com/MorenoSatria/pendeteksi-manusia-objek.git
```

### jalankan manusia.py di thonny atau sejenisnya
###jika sudah jalankan, klik ip yang muncul

## Screenshots
![Dashboard]
(https://github.com/user-attachments/assets/90f00fc1-4cab-4ff5-a0f3-08db857b4bda)
