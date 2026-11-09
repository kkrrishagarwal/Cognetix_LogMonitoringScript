import time
import re
import os

LOG_FILE = "server.log"

def simulate_log_entry(entry):
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def monitor_logs():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("System startup completed.\n")

    print(f"[*] Monitoring log file: {LOG_FILE} (Press Ctrl+C to stop)...", flush=True)
    
    # Patterns to detect
    pattern = re.compile(r"FAILED LOGIN|UNAUTHORIZED|500 INTERNAL ERROR|INVALID PASSWORD|DISK FULL", re.IGNORECASE)

    alert_count = 0
    try:
        with open(LOG_FILE, "r") as f:
            # Move to end of file for tail -f behavior
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue

                clean_line = line.strip()
                print(f"[LOG] {clean_line}", flush=True)
                if pattern.search(clean_line):
                    alert_count += 1
                    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"🚨 ALERT! Suspicious activity detected: {clean_line}", flush=True)
                    with open("alerts.log", "a") as alert_file:
                        alert_file.write(f"[{stamp}] ALERT: {clean_line}\n")
    except KeyboardInterrupt:
        print(f"\n[*] Monitoring stopped. {alert_count} alert(s) written to alerts.log")

def main():
    print("==========================================")
    print("      LOG MONITORING & ALERT SCRIPT       ")
    print("==========================================")
    print("1. Start Monitoring Logs")
    print("2. Simulate Test Suspicious Log Entry")
    print("3. Exit")
    
    choice = input("Choose option (1-3): ").strip()
    if choice == "1":
        monitor_logs()
    elif choice == "2":
        entry = input("Enter log message to simulate: ").strip()
        simulate_log_entry(entry)
        print("✅ Simulated entry added to server.log")

if __name__ == "__main__":
    main()
