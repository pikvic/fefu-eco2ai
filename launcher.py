from pathlib import Path
from importlib import reload
import sys
import subprocess

# implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', '<packagename>'])

def check_installation():
    print("Checking Installed Modules...")
    result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], capture_output=True)
    if 'eco2ai' in str(result.stdout):
        print("Modules Installed.")
        return True
    print("Needed modules aren't installed.")
    return False

def install():
    print("Installing Modules...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'eco2ai'], capture_output=True)
    print("Modules Installed.")
    
def init():
    try:
        if not version_file.exists() or not worker_file.exists():
            remote_version = requests.get(version_raw_url).text
            worker_script = requests.get(worker_raw_url).text
            with version_file.open("wt") as f:
                f.write(remote_version)
            with worker_file.open("wt") as f:
                f.write(worker_script)    
    except Exception as e:
        print(e)

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
    for i, v in enumerate(work):
        print(v)
        if i % 5 == 0:
            if check_updates():
                print("Need to update")
                work.send('stop')
                break
            else:
                work.send(None)    
        else:
            work.send(None)
    return True

if __name__ == "__main__":
    init()
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