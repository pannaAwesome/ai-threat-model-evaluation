from threading import Thread
from time import time

def result_time(seconds):
    time_pretty = ""
    if seconds > 3600:
        time_pretty += f"{seconds // 3600} hours "
        seconds = seconds % 3600
    if seconds > 60:
        time_pretty += f"{seconds // 60} min "
        seconds = seconds % 60
    time_pretty += f"{seconds} sec"
    return time_pretty

def progress_monitor(start_time, futures, interval):
    while not all(f.done() for f in futures):
        time.sleep(interval)
        done_count = sum(f.done() for f in futures)
        print(f"[STATUS] Time elapsed: {result_time(time()-start_time)} Progress: {done_count} out of {len(futures)}")

def concurrent_progress_monitor(start_time, futures, info_interval):
    monitor_threads = Thread(target=progress_monitor, args=(start_time, futures, info_interval))
    monitor_threads.daemon = True
    monitor_threads.start()