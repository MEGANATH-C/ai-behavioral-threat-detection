import psutil
import time
import threading
import os
from datetime import datetime

# Shared data dictionary
system_data = {}
lock = threading.Lock()

last_disk = psutil.disk_io_counters()
last_time = time.time()


def calculate_threat(cpu, disk_rate):
    score = (cpu * 0.5) + (disk_rate * 0.5)

    if score > 80:
        return round(score, 2), "HIGH"
    elif score > 50:
        return round(score, 2), "MEDIUM"
    else:
        return round(score, 2), "LOW"


def get_top_process():
    try:
        processes = sorted(
            psutil.process_iter(['name', 'cpu_percent']),
            key=lambda p: p.info['cpu_percent'] if p.info['cpu_percent'] else 0,
            reverse=True
        )
        if processes:
            return processes[0].info['name']
    except:
        return "Unknown"
    return "Idle"


def monitor_system():
    global last_disk, last_time

    while True:
        start_time = time.time()

        cpu = psutil.cpu_percent(interval=1)

        current_disk = psutil.disk_io_counters()
        current_time = time.time()

        time_diff = current_time - last_time
        if time_diff <= 0:
            time_diff = 1

        disk_rate = ((current_disk.write_bytes - last_disk.write_bytes)
                     / (1024 * 1024)) / time_diff

        threat_prob, risk = calculate_threat(cpu, disk_rate)
        top_process = get_top_process()

        response_time = (time.time() - start_time) * 1000
        memory_usage = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
        engine_cpu = psutil.Process(os.getpid()).cpu_percent(interval=0)

        with lock:
            system_data.update({
                "cpu": cpu,
                "disk": disk_rate,
                "threat_probability": threat_prob,
                "risk_level": risk,
                "top_process": top_process,
                "response_time": round(response_time, 2),
                "memory_usage": round(memory_usage, 2),
                "engine_cpu": engine_cpu,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        last_disk = current_disk
        last_time = current_time


def get_metrics():
    with lock:
        return system_data.copy()


def start_engine():
    thread = threading.Thread(target=monitor_system, daemon=True)
    thread.start()