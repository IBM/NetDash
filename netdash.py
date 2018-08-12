#!/usr/bin/env python3
import logging
import argparse
import sys
import ipaddress
import threading

from src.host import Host
import src.pinger as pinger


def positive_int(in_value):
    try:
        value = int(in_value)
    except ValueError:
        raise argparse.ArgumentTypeError(in_value + " is not a valid positive integer")

    if value <= 0:
        raise argparse.ArgumentTypeError(in_value + " is not a valid positive integer")

    return value


DEFAULT_TIME = 30     # Default update cycle time
DEFAULT_PING_NUM = 1  # Default number of pings to send

# Format log, remove username and insert a space
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Network monitoring dashboard")
parser.add_argument('path', help="path to configuration file")
parser.add_argument('-t', '-time', nargs=1, type=positive_int, default=[DEFAULT_TIME], help="update cycle time")
parser.add_argument('-c', '-count', nargs=1, type=positive_int, default=[DEFAULT_PING_NUM], help="num of pings to send")
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
    line = line.strip()

    if not line or line[0] == '#':
        continue

    try:
        addr = ipaddress.ip_address(line)
    except ValueError:
        logging.error("IP address on line " + str(line_num + 1) + " is not valid, skipping it.")
        continue

    Host.hosts.append(Host(addr))

file.close()

# Start pinger thread
threading.Thread(target=pinger.ping_all, args=(args.c[0], args.t[0]), name="Pinger", daemon=True).start()

while True:
    # TODO: Start UI here
    pass

