"""Configuration variables"""
import logging

cycle_time = 0
ping_number = 0
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
