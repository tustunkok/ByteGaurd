import psutil
import time
import os
import sys
import argparse

# ==== CONFIGURATION ====
PROCESS_NAME = "chrome.exe"   # Target process name
IDLE_TIME_LIMIT = 30          # Seconds of no significant activity before shutdown
BYTE_THRESHOLD = 1024         # Ignore increases smaller than this (1 KB)
CHECK_INTERVAL = 2            # Seconds between checks
# ========================

def find_process_by_name(name):
    """Find the first process matching the given name."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            return proc
    return None

def get_all_related_procs(main_proc):
    """Get the main process + all child processes recursively, fresh each time."""
    procs = []
    try:
        procs.append(main_proc)
        procs.extend(main_proc.children(recursive=True))
    except psutil.NoSuchProcess:
        pass
    return procs

def get_total_read_bytes(procs):
    """Sum read_bytes for a list of processes."""
    total = 0
    for p in procs:
        try:
            total += p.io_counters().read_bytes
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return total

def main():
    parser = argparse.ArgumentParser(description="Monitor download activity and shut down if no significant activity.")
    parser.add_argument('--process-name', default=PROCESS_NAME, help='Target process name')
    parser.add_argument('--idle-time-limit', type=int, default=IDLE_TIME_LIMIT, help='Seconds of no significant activity before shutdown')
    parser.add_argument('--byte-threshold', type=int, default=BYTE_THRESHOLD, help='Ignore increases smaller than this (in bytes)')
    parser.add_argument('--check-interval', type=int, default=CHECK_INTERVAL, help='Seconds between checks')

    args = parser.parse_args()

    PROCESS_NAME = args.process_name
    IDLE_TIME_LIMIT = args.idle_time_limit
    BYTE_THRESHOLD = args.byte_threshold
    CHECK_INTERVAL = args.check_interval

    proc = find_process_by_name(PROCESS_NAME)
    if not proc:
        print(f"Process {PROCESS_NAME} not found.")
        sys.exit(1)

    print(f"Monitoring {PROCESS_NAME} (PID: {proc.pid}) and all dynamic children for download activity...")

    # Initial byte count
    last_bytes = get_total_read_bytes(get_all_related_procs(proc))
    last_active = time.time()

    while True:
        try:
            # Refresh list of processes each loop (catches new children)
            all_procs = get_all_related_procs(proc)
            current_bytes = get_total_read_bytes(all_procs)
            diff = current_bytes - last_bytes
            last_bytes = current_bytes

            if diff >= BYTE_THRESHOLD:
                last_active = time.time()
                print(f"Downloading... +{diff} bytes (total: {current_bytes})")
            else:
                idle_time = time.time() - last_active
                print(f"Only {diff} bytes in last check — idle for {idle_time:.1f} seconds.")
                if idle_time >= IDLE_TIME_LIMIT:
                    print("Download finished. Shutting down...")
                    os.system("shutdown /s /t 0")
                    break

            time.sleep(CHECK_INTERVAL)

        except psutil.NoSuchProcess:
            print("Main process closed.")
            break

if __name__ == "__main__":
    main()