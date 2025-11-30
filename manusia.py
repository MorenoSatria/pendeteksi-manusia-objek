# pendeteksi-manusia-objek

import network
import socket
import time
from machine import Pin, time_pulse_us, PWM

# ==========================
# KONFIGURASI SENSOR & BUZZER
# ==========================
trigger = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

# Buzzer pasif pakai PWM
buzzer = PWM(Pin(4))
buzzer.freq(1500)  # frekuensi bunyi
buzzer.duty(0)     # awalnya mati

threshold = 20  # cm (batas deteksi manusia)

# ==========================
# FUNGSI BACA JARAK HC-SR04
# ==========================
def get_distance():
    trigger.value(0)
    time.sleep_us(5)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    duration = time_pulse_us(echo, 1, 30000)

    if duration < 0:
        return 999

    distance = (duration / 2) / 29.1
    return distance

# ==========================
# KONEKSI KE WIFI
# ==========================
ssid = "Lab Telkom"
password = ""

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

print("Menghubungkan ke WiFi...")
while not wifi.isconnected():
    time.sleep(0.5)

print("Connected! IP:", wifi.ifconfig()[0])

# ==========================
# HALAMAN WEB
# ==========================
def web_page(distance, status):
    color = "red" if status == "TERDETEKSI" else "green"
    emoji = "⚠️" if status == "TERDETEKSI" else "✅"
    
    html = f"""
    <html>
    <head>
        <title>Pendeteksi Manusia ESP32</title>
        <meta http-equiv="refresh" content="1">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                background: linear-gradient(to right, #a8edea, #fed6e3);
                margin: 0;
                padding: 0;
            }}
            h1 {{
                margin-top: 30px;
                color: #333;
                font-size: 32px;
            }}
            .box {{
                display: inline-block;
                padding: 30px;
                margin-top: 40px;
                background: #fff;
                border-radius: 20px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                min-width: 300px;
            }}
            .distance {{
                font-size: 36px;
                font-weight: bold;
                color: #333;
                margin: 10px 0;
            }}
            .status {{
                font-size: 28px;
                font-weight: bold;
                color: {color};
            }}
            .emoji {{
                font-size: 40px;
            }}
            p {{
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <h1>Sistem Pendeteksi Manusia</h1>
        <div class="box">
            <p class="distance">Jarak: <b>{distance:.2f} cm</b></p>
            <p class="status">Status: {status}</p>
        </div>
    </body>
    </html>
    """
    return html


# ==========================
# FUNGSI START SERVER (ANTI PORT BENTROK)
# ==========================
def start_server():
    global server
    try:
        server.close()
    except:
        pass

    time.sleep(0.3)  # beri waktu port dibersihkan

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(1)
    print("Web server berjalan di port 80")

start_server()

# ==========================
# LOOP UTAMA
# ==========================
while True:
    distance = get_distance()

    if distance < threshold:
        status = "TERDETEKSI"
        # Double beep
        for _ in range(2):
            buzzer.duty(512)  # bunyi
            time.sleep(0.2)   # durasi beep 200 ms
            buzzer.duty(0)    # mati
            time.sleep(0.1)   # jeda antar beep
    else:
        status = "AMAN"
        buzzer.duty(0)

    # Debug serial
    print("Jarak:", distance, "cm | Status:", status)

    # Handle request web
    conn, addr = server.accept()
    request = conn.recv(1024)
    response = web_page(distance, status)
    conn.send("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n")
    conn.send(response)
    conn.close()

