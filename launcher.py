import requests
from pathlib import Path
import worker
from importlib import reload


version_raw_url = 'https://raw.githubusercontent.com/pikvic/fefu-eco2ai/main/version.txt'
version_file = Path() / 'version.txt'
worker_file = Path() / 'worker.py'
worker_raw_url = 'https://raw.githubusercontent.com/pikvic/fefu-eco2ai/main/worker.py'

def check_updates():
    local_version = version_file.read_text()
    remote_version = requests.get(version_raw_url).text
    print("Local version:", local_version, "Remote Version:", remote_version)
    if local_version != remote_version:
        return True
    return False

def update():
    print("Updating...")
    local_version = version_file.read_text()
    remote_version = requests.get(version_raw_url).text
    worker_file.write_text(requests.get(worker_raw_url).text)
    reload(worker)
    version_file.write_text(remote_version)
    print("Update Finished")

def start():
    for i, v in enumerate(worker.work()):
        print(v)
        if i % 5 == 0:
            if check_updates():
                break
    return True

if __name__ == "__main__":
    while True:
        print("Starting worker...")
        needsUpdate = start()
        if needsUpdate:
            update()