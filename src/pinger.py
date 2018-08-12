import platform
import subprocess
import time

from src.host import Host


def ping(ip_addr, count, version):
    """Ping IP address 'count' times"""

    command = 'ping'   # Ping command, default to ipv4
    count_parm = '-c'  # Count flag, default to unix usage

    # Platform specific modifications
    # Use ping6 command for Linux, some distributions require it
    if platform.system() == 'Linux' and version == 6:
        command = 'ping6'
    # Change count flag if on Windows system
    elif platform.system() == 'Windows':
        count_parm = '-n'

    return subprocess.call([command, count_parm, str(count), ip_addr])


def ping_all(count, cycle_time):
    """Ping all hosts 'count' times every 'cycle_time' seconds"""

    while True:
        # Ping all of the addresses
        for host in Host.hosts:
            result = ping(str(host.ip), count, host.ip.version)

            # Update status of hosts based on ping result
            if not result:
                host.status = "SUCCESS"
            elif result == 1:
                host.status = "FAIL"
            else:
                host.status = "OTHER"

        # Sleep for cycle_time seconds before pinging again
        time.sleep(cycle_time)
