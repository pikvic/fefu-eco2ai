import eco2ai
import os
import signal
import platform
from time import sleep

tracker = eco2ai.Tracker(
    project_name=platform.node(),
    experiment_description="Test",
    measure_period=10,
    alpha_2_code="RU",
    region="Primorskiy Kray",
    cpu_processes="all"
    )

tracker.start()

def handler(sig, frame):
    tracker.stop()
    exit(1)

signal.signal(signal.SIGINT, handler)

while True:
    sleep(10)
    print("Consumption:", tracker.consumption())
    #print(tracker._construct_attributes_dict())
    #print("Consumption:", tracker.consumption(), "Emission:", tracker.emission_level())
