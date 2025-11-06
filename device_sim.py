import requests, time, random

URL = "http://127.0.0.1:8000/ingest"
DEVICE_ID = "dev-001"

while True:
    temp = round(random.uniform(25, 35), 2)   # 25–35 °C
    humidity = round(random.uniform(40, 80), 1)
    data = {"deviceId": DEVICE_ID, "temp_c": temp, "humidity": humidity}
    try:
        r = requests.post(URL, json=data, timeout=2)
        print("sent:", data, "status:", r.status_code)
    except Exception as e:
        print("error sending:", e)
    time.sleep(2)
