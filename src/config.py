"""Configuration variables"""
import logging
import sys

try:
    from tkinter import messagebox
except ImportError:
    logging.critical("Can not import tkinter, may not be installed.")
    sys.exit(3)

DEFAULT_CONFIG_NAME = "config.txt"
DEFAULT_CYCLE_TIME = 30
DEFAULT_PING_COUNT = 1
DEFAULT_QUIET_MODE = False

path = ""
file_name = DEFAULT_CONFIG_NAME
cycle_time = DEFAULT_CYCLE_TIME
ping_count = DEFAULT_PING_COUNT
quiet = DEFAULT_QUIET_MODE


def set_quiet(state):
    """Set the quiet setting, adjust logging accordingly."""
    global quiet

    # If set, only show WARNING messages and above
    if state:
        quiet = True
        logging.getLogger().setLevel(logging.WARNING)
    else:
        quiet = False
        logging.getLogger().setLevel(logging.INFO)


def write_configuration():
    """Write configuration to file."""
    # Construct new program configuration line
    prog_line = str(cycle_time) + " " + str(ping_count) + " " + str(quiet) + "\n"

    # I REALLY don't like the inefficiency of this solution
    # Replace first line with new program configuration line
    try:
        with open(path + file_name) as file:
            lines = file.readlines()
        lines[0] = prog_line
        with open(path + file_name, 'w') as file:
            file.writelines(lines)
    except OSError as exc:
        # TODO: See if I can't move this back out to UI, get rid of the import in here
        messagebox.showerror("Error", "Could not write to configuration file:" + str(exc))
        logging.error("Could not write to configuration file: " + str(exc))
