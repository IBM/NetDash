#!/usr/bin/env python3
import argparse
import logging
import sys
import ipaddress
import platform
import subprocess


def ping(ip_addr):
    """Ping specified IP address"""

    count_parm = '-c'  # Count flag, default to unix usage

    # Change count flag if on Windows system
    if platform.system() == 'Windows':
        count_parm = '-n'

    return subprocess.call(['ping', count_parm, '1', ip_addr]) == 0


addresses = []  # List of IP addresses

# Remove username from log output, insert space
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Network monitoring dashboard")
parser.add_argument('path', help="path to configuration file")
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
    ping(str(address))
