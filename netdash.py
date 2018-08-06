#!/usr/bin/env python3
import argparse
import logging
import sys
import ipaddress
import platform
import subprocess


def ping(ip_addr, count, version):
    """Ping specified IP address 'count' times"""

    command = 'ping'
    count_parm = '-c'  # Count flag, default to unix usage
    count_num = count  # Number of pings to send

    # Platform specific modifications
    # Use ping6 command for Linux, some distributions require it
    if platform.system() == 'Linux' and version == 6:
        command = 'ping6'
    # Change count flag if on Windows system
    elif platform.system() == 'Windows':
        count_parm = '-n'

    return subprocess.call([command, count_parm, str(count_num), ip_addr]) == 0


addresses = []  # List of IP addresses

# Format log, remove username and insert a space
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Network monitoring dashboard")
parser.add_argument('path', help="path to configuration file")
parser.add_argument('-c', '-count', nargs=1, type=int, default=[1], help="number of pings to send")
args = parser.parse_args()

# Open configuration file at specified path
try:
    file = open(args.path)
except FileNotFoundError:
    logging.critical("File does not exist.")
    sys.exit(2)
except IsADirectoryError:
    logging.critical("Path is to a directory.")
    sys.exit(2)

# Parse configuration file
for line_num, line in enumerate(file.readlines()):
    try:
        addr = ipaddress.ip_address(line.strip())
    except ValueError:
        logging.error("IP address on line " + str(line_num + 1) + " is not valid, skipping it.")
        continue

    addresses.append(addr)

file.close()

# Ping all of the addresses
for address in addresses:
    ping(str(address), args.c[0], address.version)
