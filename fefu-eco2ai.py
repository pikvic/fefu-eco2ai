import eco2ai
import os
import signal
import requests
import platform
from time import sleep
import time

def make_dict(attr_dict):
    return {
        "project_name": attr_dict["project_name"],
        "epoch": attr_dict["epoch"],
        "start_time": attr_dict["start_time"],
        "duration(s)": attr_dict["duration(s)"],
        "power_consumption(kWh)": attr_dict["power_consumption(kWh)"],
        "CO2_emissions(kg)": attr_dict["CO2_emissions(kg)"],
        "CPU_name": attr_dict["CPU_name"],
        "GPU_name": attr_dict["GPU_name"],
        "OS": attr_dict["OS"]
    }

def handler(sig, frame):
    tracker.stop()
    exit(1)


signal.signal(signal.SIGINT, handler)

url = "http://localhost:8000"
MEASURE_PERIOD = 10

tracker = eco2ai.Tracker(
    project_name=platform.node(),
    experiment_description="Test",
    measure_period=10,
    alpha_2_code="RU",
    region="Primorskiy Kray",
    cpu_processes="all"
    )

response = requests.post(f'{url}/v1/machine/', json={"name": platform.node()})

if response.ok:
    machine_id = response.json()["id"]
else:
    response = requests.get(f'{url}/v1/machine/{platform.node()}')
    machine_id = response.json()["id"]

tracker.start()
print(tracker._construct_attributes_dict())
prev = tracker.consumption()
emission_level = tracker.emission_level()
prev_time = time.time()
while True:
    sleep(1)
    if time.time() - prev_time < MEASURE_PERIOD:
        continue
    prev_time = time.time()
    attr_dict = tracker._construct_attributes_dict()
    consumption = tracker.consumption() - prev
    prev = tracker.consumption()
    attr_dict["power_consumption(kWh)"] = [consumption]
    attr_dict["CO2_emissions(kg)"] = [consumption * emission_level / 1000]
    send_dict = make_dict(attr_dict)
    print(send_dict)
    request = requests.post(f'{url}/v1/report/', json=send_dict)
    
    #print("Consumption:", tracker.emission_level())
    #print(tracker._construct_attributes_dict())
    #print("Consumption:", tracker.consumption(), "Emission:", tracker.emission_level())
