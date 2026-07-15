import os
import threading
import time


def delete_file(path):

    try:

        if os.path.exists(path):

            os.remove(path)

    except:

        pass


def delete_after_delay(

    path,

    seconds=300

):

    """
    Deletes file after 5 minutes.

    Useful for Render temporary storage.
    """

    def worker():

        time.sleep(seconds)

        delete_file(path)

    threading.Thread(

        target=worker,

        daemon=True

    ).start()