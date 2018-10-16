"""Pinging hosts"""

import platform
import subprocess
import logging
import threading

import src.config as config
from src.host import hosts

ping_all_event = threading.Event()  # Threading event for pinging all hosts


def ping(host, count):
    """Ping IP address 'count' times"""

    ip_addr = str(host.ip)
    version = host.ip.version
    command = 'ping'   # Ping command, default to ipv4
    count_parm = '-c'  # Count flag, default to unix

    # Platform specific modifications
    # Use ping6 command for Linux, some distributions require it
    if platform.system() == 'Linux' and version == 6:
        command = 'ping6'
    # Change count flag if on Windows system
    elif platform.system() == 'Windows':
        count_parm = '-n'

    result = subprocess.call([command, count_parm, str(count), ip_addr], stdout=subprocess.DEVNULL)

    # Update status of host based on ping result
    if not result:
        host.set_status("SUCCESS")
    elif result == 1:
        host.set_status("FAIL")
    else:
        host.set_status("OTHER")

    logging.info("Host: " + str(host.ip) + " Result: " + host.status)


def ping_all():
    """Spawn a thread to ping each host, then sleep for cycle_time seconds"""

    while True:
        threads = []

        # Ping all of the addresses in a thread
        for idx, host in enumerate(hosts):
            name = "Ping-" + str(idx)
            thread = threading.Thread(target=ping, args=(host, config.ping_number), name=name, daemon=True)
            threads.append(thread)
            thread.start()

        # Sleep for cycle_time seconds before pinging again
        ping_all_event.clear()
        ping_all_event.wait(config.cycle_time)

        # Don't start pinging again until all threads are done
        for thread in threads:
            thread.join()
