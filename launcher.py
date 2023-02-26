from pathlib import Path
from importlib import reload
import sys
import subprocess

# implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', '<packagename>'])

def check_installation():
    result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], capture_output=True)
    if 'eco2ai' in str(result.stdout):
        return True
    return False

def install():
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'eco2ai'], capture_output=True)
    

version_raw_url = 'https://raw.githubusercontent.com/pikvic/fefu-eco2ai/main/version.txt'
version_file = Path() / 'version.txt'
worker_file = Path() / 'worker.py'
worker_raw_url = 'https://raw.githubusercontent.com/pikvic/fefu-eco2ai/main/worker.py'

def check_updates():
    try:
        local_version = version_file.read_text()
        remote_version = requests.get(version_raw_url).text
        print("Local version:", local_version, "Remote Version:", remote_version)
        if local_version != remote_version:
            return True
        return False
    except Exception as e:
        print(e)
        return False

def update():
    try:
        print("Updating...")
        local_version = version_file.read_text()
        remote_version = requests.get(version_raw_url).text
        worker_file.write_text(requests.get(worker_raw_url).text)
        reload(worker)
        version_file.write_text(remote_version)
        print("Update Finished")
    except Exception as e:
        print(e)

def start():
    work = worker.work()
    work.send(None)
    for i, v in enumerate(work):
        print(v)
        if i % 5 == 0:
            work.send(i)
            if check_updates():
                break
        else:
            work.send(None)
    return True

if __name__ == "__main__":
    if not check_installation():
        install()
    if not check_installation():
        print("Eco2AI is not installed. Exit")
        exit(0)
    import requests
    import worker
    while True:
        print("Starting worker...")
        needsUpdate = start()
        if needsUpdate:
            update()