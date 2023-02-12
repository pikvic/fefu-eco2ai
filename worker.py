import time


def work():
    i = 0
    while True:
        print('start')
        time.sleep(1)
        i = i + 1
        yield {'i': i}