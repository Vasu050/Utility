import platform
import psutil
import shutil
import requests
import json
import datetime

def get_system_details():
    print("[*] Scanning system details...")
    vm = psutil.virtual_memory()
    ram_gb = round(vm.total / (1024**3), 2)

    disk = shutil.disk_usage("C:\\")
    total_storage_gb = round(disk.total / (1024**3), 2)

    details = {
        "Name": platform.node(),
        "Operating System": f"{platform.system()} {platform.release()} {platform.version()}",
        "Processor": platform.processor(),
        "Cores": psutil.cpu_count(logical=False),
        "Threads": psutil.cpu_count(logical=True),
        "RAM (GB)": ram_gb,
        "Storage Total (GB)": total_storage_gb,
    }

    print("[*] System details collected successfully.")
    print(json.dumps(details, indent=4))
    return details


def build_process_tree():
    print("[*] Collecting processes...")
    proc_map = {}
    for proc in psutil.process_iter(['pid', 'name', 'ppid', 'memory_info', 'cpu_percent']):
        try:
            proc_map[proc.pid] = {
                "pid": proc.pid,
                "name": proc.info['name'],
                "ppid": proc.info['ppid'],
                "memory_mb": round(proc.info['memory_info'].rss / (1024*1024), 2),
                "cpu_percent": proc.info['cpu_percent'],
                "children": []
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # link children to parents
    tree = []
    for pid, proc in proc_map.items():
        ppid = proc['ppid']
        if ppid in proc_map:
            proc_map[ppid]['children'].append(proc)
        else:
            tree.append(proc)

    print(f"[+] Found {len(proc_map)} processes")
    return tree


API_ENDPOINT = "http://127.0.0.1:8000/collect/"
API_KEY = "utility_api_key"
HEADERS = {"API-KEY": API_KEY, "Content-Type": "application/json"}

if __name__ == "__main__":
    print("=== Agent Started ===")

    system_details = get_system_details()
    process_tree = build_process_tree()

    print("[+] Process tree collected:")
    print(json.dumps(process_tree, indent=4))

    payload = {
        "hostname": system_details["Name"],
        "system_details": system_details,
        "process_details": process_tree,
        "timestamp": datetime.datetime.now().isoformat()
    }

    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=HEADERS)
        print("Response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending data:", e)

    print("=== Agent Finished ===")
    input("\nPress Enter to exit...")
