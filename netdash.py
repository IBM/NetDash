#!/usr/bin/env python3
import logging
import argparse
import sys
import ipaddress
import threading

from src.host import Host
import src.pinger as pinger
import src.ui as ui


DEFAULT_TIME = 30     # Default update cycle time
DEFAULT_PING_NUM = 1  # Default number of pings to send

TIME_HELP = "update cycle time (in seconds)"  # Time argument help message
COUNT_HELP = "number of pings to send"        # Count argument help message


def positive_int(in_value):
    """Check if argument is a positive integer"""

    try:
        value = int(in_value)
    except ValueError:
        raise argparse.ArgumentTypeError(in_value + " is not a valid positive integer")

    if value <= 0:
        raise argparse.ArgumentTypeError(in_value + " is not a valid positive integer")

    return value


# Format log, remove username and insert a space
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')

# Parse command line arguments
parser = argparse.ArgumentParser(description="Network monitoring dashboard")
parser.add_argument('path', help="path to configuration file")
parser.add_argument('-t', '-time', nargs=1, type=positive_int, default=[DEFAULT_TIME], help=TIME_HELP)
parser.add_argument('-c', '-count', nargs=1, type=positive_int, default=[DEFAULT_PING_NUM], help=COUNT_HELP)
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

    # Skip blank lines and comments
    if not line or line[0] == '#':
        continue

    # Check validity of ip address, otherwise, skip it
    try:
        addr = ipaddress.ip_address(line)
    except ValueError:
        logging.error("IP address on line " + str(line_num + 1) + " is not valid, skipping it.")
        continue

    Host.hosts.append(Host(addr))

file.close()

# Start pinger thread
threading.Thread(target=pinger.ping_all, args=(args.c[0], args.t[0]), name="Pinger", daemon=True).start()

# Start GUI
# TODO: Needs check if X is running in Linux, something similar for Windows, probably add TUI flag (look into curses)
ui.start_gui()

