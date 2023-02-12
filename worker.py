import time


def work():
    i = 0
    while True:
        data = yield
        print('start1', data)
        time.sleep(1)
        i = i + 1
        yield {'i': i}