import eco2ai
import os
import requests
import platform
from time import sleep
import time


def make_report_dict(attr_dict: dict):
    return {
        "power_consumption": attr_dict["power_consumption(kWh)"][0],
        "co2_emissions": attr_dict["CO2_emissions(kg)"][0]
    }

def make_register_dict(attr_dict: dict, room: str):
    return {
        "name": attr_dict["project_name"][0],
        "cpu_name": attr_dict["CPU_name"][0],
        "gpu_name": attr_dict["GPU_name"][0],
        "os": attr_dict["OS"][0],
        "description": attr_dict["experiment_description"][0],
        "room": room
    }

def register(tracker: eco2ai.Tracker):
    attr_dict = tracker._construct_attributes_dict()
    register_dict = make_register_dict(attr_dict, ROOM)
    try:
        response = requests.post(f'{URL}/v1/machine/', json=register_dict)
        if response.ok:
            machine_id = response.json()["id"]
    except Exception as e:
        print(f"ERROR: can't register. {e}")
    
def send_data(tracker: eco2ai.Tracker, prev: float) -> float:
    attr_dict = tracker._construct_attributes_dict()
    consumption = tracker.consumption() - prev
    prev = tracker.consumption()
    emission_level = tracker.emission_level()
    attr_dict["power_consumption(kWh)"] = [consumption]
    attr_dict["CO2_emissions(kg)"] = [consumption * emission_level / 1000]
    send_dict = make_report_dict(attr_dict)
    try:
        response = requests.post(f'{URL}/v1/report/{MACHINE_NAME}/', json=send_dict)
        if response.status_code == 404:
            register(tracker)
    except Exception as e:
        print(f"ERROR: can't send data. {e}")
    return prev

URL = os.getenv('BACKEND_URL', "http://194.58.109.30/api")
MEASURE_PERIOD = 10
MACHINE_NAME = platform.node()
DESCRIPTION = "Test for eco2ai" 
ROOM = "G464"


def work():
    i = 0
    tracker = eco2ai.Tracker(
            project_name=MACHINE_NAME,
            experiment_description=DESCRIPTION,
            measure_period=MEASURE_PERIOD,
            alpha_2_code="RU",
            region="Primorskiy Kray",
            cpu_processes="all"
            )

    tracker.start()
    register(tracker)

    prev = tracker.consumption()
    prev_time = time.time()
    send_counter = 0
    while True:
        sleep(5)
        if time.time() - prev_time < MEASURE_PERIOD:
            continue
        prev_time = time.time()
        prev = send_data(tracker, prev)
        send_counter += 1
        context = yield {'send_counter': send_counter}
        if context is not None:
            tracker.stop()
            yield {'status': 'stopped'}

        
        