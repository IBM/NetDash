#!/usr/bin/env python3
import platform
import subprocess


def ping(ip_addr):
    """Ping specified IP address"""

    count_parm = '-c'  # Count flag, default to unix usage

    # Change count flag if on Windows system
    if platform.system() == 'Windows':
        count_parm = '-n'

    return subprocess.call(['ping', count_parm, '1', ip_addr]) == 0


ipaddr = "192.168.1.23"
ping(ipaddr)
