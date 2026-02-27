import psutil
import time
import joblib
import pandas as pd

model = joblib.load("anomaly_model.pkl")
scaler = joblib.load("scaler.pkl")

print("Improved Real-time Detection Started")
print("Press CTRL + C to stop.\n")

prev_disk = psutil.disk_io_counters()

while True:
    cpu = psutil.cpu_percent()
    current_disk = psutil.disk_io_counters()
    processes = len(psutil.pids())

    read_rate = current_disk.read_bytes - prev_disk.read_bytes
    write_rate = current_disk.write_bytes - prev_disk.write_bytes
    prev_disk = current_disk

    sample = pd.DataFrame([[cpu, read_rate, write_rate, processes]], columns=["cpu","disk_read","disk_write","process_count"])
    scaled_sample = scaler.transform(sample)
    prediction = model.predict(scaled_sample)

    if prediction[0] == -1:
        print("ALERT: Suspicious activity detected!")
    else:
        print("Normal Activity")

    time.sleep(1)
