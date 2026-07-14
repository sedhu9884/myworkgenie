import os
import threading
import time


def delete_file(path):

    try:
        if os.path.exists(path):
            os.remove(path)
    except:
        pass


def delete_after_delay(path, seconds=15):

    def worker():

        time.sleep(seconds)

        delete_file(path)

    threading.Thread(
        target=worker,
        daemon=True
    ).start()