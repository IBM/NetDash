#!/usr/bin/env python3
"""Program Start"""
# TODO: Add/correct docstrings

import platform
import logging
import sys
import os
import shlex
import ipaddress
import threading

import src.pinger as pinger
import src.ui as ui
import src.config as config
from src.host import Host, hosts

CONFIG_FILE_NAME = "config.txt"

config_errors = []  # Text for error windows for the UI once it starts

# Set configuration path based on system type
if platform.system() in ['Linux', 'Unix', 'Darwin']:
    config.path = os.path.expanduser("~/netdash/")
elif platform.system() == 'Windows':
    config.path = os.path.expandvars("%USERPROFILE%\\netdash\\")
else:
    logging.critical("System type '" + platform.system() + "' not supported.")
    sys.exit(3)

# TODO: Figure out what merits spawning an error window (add string to list) and what generally needs try catches
# If a configuration file exists, read configuration in, otherwise create file with basic configuration
if os.path.isfile(config.path + config.file_name):
    fd = open(config.path + config.file_name, 'r')

    # Parse program configuration
    conf = fd.readline().split()

    # TODO: Wrap these in try-catch, default each and add error string
    config.cycle_time = int(conf[0])
    config.ping_count = int(conf[1])
    config.quiet = (conf[2] == "True")

    # Parse host configuration
    # Format: IP_ADDRESS "LABEL"
    for line_num, line in enumerate(fd.readlines()):
        line = line.strip()

        # Skip blank lines and comments
        if not line or line[0] == '#':
            continue
        line_parts = shlex.split(line)

        # Check validity of ip address, otherwise, skip it
        try:
            addr = ipaddress.ip_address(line_parts[0])
        except ValueError:
            logging.error("IP address on line " + str(line_num + 1) + " is not valid, skipping it.")
            continue

        # Subsequent additions of optional fields will require a "None" value to be supported
        # If a label exists, use it
        label = None
        if len(line_parts) > 1:
            label = line_parts[1]

        # Add the host to the list
        hosts.append(Host(addr, label=label))
else:
    # Create the directory if it doesn't exist
    if not os.path.exists(config.path):
        os.mkdir(config.path)
    fd = open(config.path + config.file_name, 'x')
    fd.write(str(config.cycle_time) + " " + str(config.ping_count) + " " + str(config.quiet) + "\n\n")

fd.close()

# Start pinger thread
threading.Thread(target=pinger.ping_all, name="Pinger", daemon=True).start()

# Start GUI
ui.start_gui(config_errors)
