"""Pinging hosts"""

import platform
import subprocess
import logging
import threading

import src.config as config
from src.host import Host

ping_all_event = threading.Event()


def ping(ip_addr, count, version):
    """Ping IP address 'count' times"""

    command = 'ping'   # Ping command, default to ipv4
    count_parm = '-c'  # Count flag, default to unix

    # Platform specific modifications
    # Use ping6 command for Linux, some distributions require it
    if platform.system() == 'Linux' and version == 6:
        command = 'ping6'
    # Change count flag if on Windows system
    elif platform.system() == 'Windows':
        count_parm = '-n'

    return subprocess.call([command, count_parm, str(count), ip_addr], stdout=subprocess.DEVNULL)


def ping_host(host, count):
    """Ping all hosts 'count' times"""

    result = ping(str(host.ip), count, host.ip.version)

    # Update status of hosts based on ping result
    if not result:
        host.status = "SUCCESS"
        status_color = "green2"
    elif result == 1:
        host.status = "FAIL"
        status_color = "red2"
    else:
        host.status = "OTHER"
        status_color = "orange2"
    # Update widget if GUI
    if host.status_widget is not None:
        host.set_status_color(status_color)

    logging.info("Host " + str(host.ip) + " Result " + host.status)


def refresh():
    """Set ping_all_event to trigger ping_all"""
    ping_all_event.set()


def ping_all():
    """Spawn a thread to ping each host, then sleep for cycle_time seconds"""

    while True:
        threads = []

        # Ping all of the addresses in a thread
        for idx, host in enumerate(Host.hosts):
            name = "Ping-" + str(idx)
            thread = threading.Thread(target=ping_host, args=(host, config.ping_number), name=name, daemon=True)
            threads.append(thread)
            thread.start()

        # Sleep for cycle_time seconds before pinging again
        ping_all_event.clear()
        ping_all_event.wait(config.cycle_time)

        # Don't start pinging again until all threads are done
        for thread in threads:
            thread.join()
