#!/usr/bin/env python3
"""Program Start"""
# TODO: Add setting for configuration file location?
# TODO: Add logging file, maybe setting?
# TODO: Make host list editable in GUI

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


config_errors = []  # Text for error windows for the UI once it starts

# Set logging format and other configuration
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m-%d-%y %H:%M:%S')

# Set configuration path based on system type
if platform.system() in ['Linux', 'Unix', 'Darwin']:
    config.path = os.path.expanduser("~/netdash/")
elif platform.system() == 'Windows':
    config.path = os.path.expandvars("%USERPROFILE%\\netdash\\")
else:
    logging.critical("System type '" + platform.system() + "' not supported.")
    sys.exit(3)

# If a configuration file exists, read configuration in, otherwise create file with basic configuration
if os.path.isfile(config.path + config.file_name):
    logging.debug("Configuration file found, parsing it.")
    try:
        fd = open(config.path + config.file_name, 'r')
    except OSError as ex:
        logging.critical("Coult not open configuration file: " + str(ex))
        sys.exit(4)

    # Parse program configuration
    conf = fd.readline().split()

    if len(conf) == 0:
        msg = "Fist line in configuration file is empty, using default settings."
        logging.error(msg)
        config_errors.append(msg)

    # Parse cycle time
    if len(conf) >= 1:
        try:
            config.cycle_time = int(conf[0])
            if config.cycle_time <= 0:
                msg = "Cycle time specified in configuration file is not positive. Defaulting to " \
                      + str(config.DEFAULT_CYCLE_TIME) + "."
                logging.error(msg)
                config_errors.append(msg)
                config.cycle_time = config.DEFAULT_CYCLE_TIME
        except ValueError:
            msg = "Cycle time specified in configuration file is not positive. Defaulting to " \
                  + str(config.DEFAULT_CYCLE_TIME) + "."
            logging.error(msg)
            config_errors.append(msg)
    # Parse ping count
    if len(conf) >= 2:
        try:
            config.ping_count = int(conf[1])
            if config.ping_count <= 0:
                msg = "Ping count specified in configuration file is not positive. Defaulting to " \
                      + str(config.DEFAULT_PING_COUNT) + "."
                logging.error(msg)
                config_errors.append(msg)
                config.ping_count = config.DEFAULT_PING_COUNT
        except ValueError:
            msg = "Ping count specified in configuration file is not an integer. Defaulting to " \
                  + str(config.DEFAULT_PING_COUNT) + "."
            logging.error(msg)
            config_errors.append(msg)
    else:
        msg = "Configuration line in configuration file doesn't specifiy ping count or quiet mode settings, " \
              "using defaults."
        logging.error(msg)
        config_errors.append(msg)
    # Parse quiet mode setting
    if len(conf) >= 3:
        config.quiet = (conf[2].upper() == "TRUE")
        if conf[2].upper() == "TRUE":
            config.set_quiet(True)
        elif conf[2].upper() == "FALSE":
            config.set_quiet(False)
        else:
            msg = 'Quiet mode specified is not "True" or "False", defaulting to ' + str(config.DEFAULT_QUIET_MODE) + "."
            logging.error(msg)
            config_errors.append(msg)
    else:
        msg = "Configuration line in configuration file doesn't specifiy quiet mode setting, using default."
        logging.error(msg)
        config_errors.append(msg)
    # Ignore anything else on the first line
    if len(conf) > 3:
        msg = "Extraneous elements in first line of configuration file, ignoring them."
        logging.warning(msg)

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
            msg = "IP address on line " + str(line_num + 1) + " is not valid, skipping it."
            logging.error(msg)
            config_errors.append(msg)
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
    logging.info("Configuration file not found, creating it.")
    if not os.path.exists(config.path):
        try:
            os.mkdir(config.path)
        except OSError as ex:
            logging.critical("Could not create configuration file directory: " + str(ex))
            sys.exit(4)
    try:
        fd = open(config.path + config.file_name, 'x')
    except OSError as ex:
        logging.critical("Count not create configuration file: " + str(ex))
        sys.exit(4)
    fd.write(str(config.cycle_time) + " " + str(config.ping_count) + " " + str(config.quiet) + "\n\n")

fd.close()

# Start pinger thread
threading.Thread(target=pinger.ping_all, name="Pinger", daemon=True).start()

# Start GUI
ui.start_gui(config_errors)
