import subprocess


def start_service(service_name):
    try:
        cmd = "/usr/bin/sudo /bin/systemctl start " + service_name
        subprocess.run(cmd, shell=True, check=True)
        print(f"{service_name} started successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to start {service_name}.")

def stop_service(service_name):
    try:
        cmd = "/usr/bin/sudo /bin/systemctl stop " + service_name
        subprocess.run(cmd, shell=True, check=True)
        print(f"{service_name} stopped successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to stop {service_name}.")