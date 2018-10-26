"""Configuration variables"""
import logging

path = ""
cycle_time = 30
ping_count = 1
quiet = False


def set_quiet(state):
    """Set the quiet setting, adjust logging accordingly"""
    global quiet

    # If set, only show WARNING messages and above
    if state:
        quiet = True
        logging.getLogger().setLevel(logging.WARNING)
    else:
        quiet = False
        logging.getLogger().setLevel(logging.INFO)
