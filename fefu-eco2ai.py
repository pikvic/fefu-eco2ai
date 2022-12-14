import eco2ai
import os
import signal
import requests
import platform
from time import sleep
import time

def make_report_dict(attr_dict):
    return {
        "power_consumption": attr_dict["power_consumption(kWh)"][0],
        "co2_emissions": attr_dict["CO2_emissions(kg)"][0]
    }

def make_register_dict(attr_dict, room):
    return {
        "name": attr_dict["project_name"][0],
        "cpu_name": attr_dict["CPU_name"][0],
        "gpu_name": attr_dict["GPU_name"][0],
        "os": attr_dict["OS"][0],
        "description": attr_dict["experiment_description"][0],
        "room": room
    }

def handler(sig, frame):
    tracker.stop()
    exit(1)

signal.signal(signal.SIGINT, handler)

url = "http://localhost:8000"
MEASURE_PERIOD = 10
MACHINE_NAME = platform.node()
DESCRIPTION = "Test for eco2ai" 
ROOM = "G464"

tracker = eco2ai.Tracker(
    project_name=MACHINE_NAME,
    experiment_description=DESCRIPTION,
    measure_period=MEASURE_PERIOD,
    alpha_2_code="RU",
    region="Primorskiy Kray",
    cpu_processes="all"
    )

tracker.start()
attr_dict = tracker._construct_attributes_dict()
register_dict = make_register_dict(attr_dict, ROOM)
print(register_dict)
response = requests.post(f'{url}/v1/machine/', json=register_dict)

if response.ok:
    machine_id = response.json()["id"]

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
    send_dict = make_report_dict(attr_dict)
    print(send_dict)
    request = requests.post(f'{url}/v1/report/{MACHINE_NAME}/', json=send_dict)
    
    #print("Consumption:", tracker.emission_level())
    #print(tracker._construct_attributes_dict())
    #print("Consumption:", tracker.consumption(), "Emission:", tracker.emission_level())
