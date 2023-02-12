import requests
from pathlib import Path
from worker import work

def check_updates():
    url = 'https://raw.githubusercontent.com/pikvic/fefu-eco2ai/main/version.txt'
    file = Path() / 'version.txt'
    local_version = file.read_text()
    print("Local version:", local_version)
    response = requests.get(url)
    print("Remote version:", response.raw)
    


def update():
    print("Updating...")

    print("Update Finished")

def start():
    for i in work():
        print(i)
        if i["i"] == 10:
            break
    return True

if __name__ == "__main__":
    while True:
        print("Starting worker...")
        needsUpdate = start()
        if needsUpdate:
            check_updates()
            update()