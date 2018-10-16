"""UI Handling"""

import logging
import sys

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    logging.critical("Can not import tkinter, may not be installed.")
    sys.exit(3)

import src.config as config
from src.host import hosts
from src.pinger import ping_all_event


class App:
    """GUI Application Class"""

    COLUMN_LIMIT = 5          # Maximum number of hosts displayed in a row
    STATUS_WIDTH = 100        # Width of status rectangle
    STATUS_HEIGHT = 50        # Height of status regtangle
    DEFAULT_COLOR = "gray45"  # Default status rectangle color

    def __init__(self, master):
        self.sett_win = None      # Settings window
        self.cycle_entry = None   # cycle entry widget in settings window
        self.count_entry = None   # count entry widget in settings window
        self.quiet = None         # Quiet mode variable for widget in settings window

        # Menu bar
        menu_bar = tk.Menu(master)
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Settings", command=self.settings_window)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=master.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_command(label="Refresh", command=ping_all_event.set)
        master.config(menu=menu_bar)

        # Widget for the resizable host elements
        row = -1
        column = 0

        for idx, host in enumerate(hosts):

            # Every 5 hosts, create a new row of hosts
            if idx % App.COLUMN_LIMIT == 0:
                row += 1
                column = 0

            # Host elements parent Frame
            host_frame = tk.Frame(master)
            host_frame.grid(row=row, column=column)

            # Host label and status widgets
            host_label = tk.Label(host_frame, text=host.label)
            host_label.pack(side=tk.TOP)
            host_status = tk.Canvas(host_frame, width=App.STATUS_WIDTH, height=App.STATUS_HEIGHT)
            host_status.create_rectangle(0, 0, App.STATUS_WIDTH, App.STATUS_HEIGHT, fill=App.DEFAULT_COLOR)
            host_status.pack(side=tk.BOTTOM)

            # Set host status_widget so it can be modified later
            host.status_widget = host_status

            column += 1

    def settings_window(self):
        """Settings window accessed through file menu in menu bar"""

        self.sett_win = tk.Toplevel()
        self.sett_win.title("Program Settings")

        # Setting labels
        tk.Label(self.sett_win, text="Update Cycle Time (seconds):").grid(row=0)
        tk.Label(self.sett_win, text="Ping Count:").grid(row=1)
        tk.Label(self.sett_win, text="Quiet Mode:").grid(row=2)

        # Entry fields
        self.cycle_entry = tk.Entry(self.sett_win)
        self.count_entry = tk.Entry(self.sett_win)

        # Quiet mode checkbutton
        self.quiet = tk.BooleanVar()
        quiet_check_button = tk.Checkbutton(self.sett_win, variable=self.quiet)

        # Apply button
        apply_button = tk.Button(self.sett_win, text="Apply", command=self.apply_settings)

        # Grid layout
        self.cycle_entry.grid(row=0, column=1)
        self.count_entry.grid(row=1, column=1)
        quiet_check_button.grid(row=2, column=1)
        apply_button.grid(row=3, column=1)

        # Default values
        self.cycle_entry.insert(0, str(config.cycle_time))
        self.count_entry.insert(0, str(config.ping_number))
        self.quiet.set(config.quiet)

    def apply_settings(self):
        """Check and apply settings from settings window"""

        # Ensure entered cycle_time is non-zero positive integer
        try:
            cycle_time = int(self.cycle_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Specified cycle time is not an integer.")
            logging.error("Cycle time specified in settings window is not an integer.")
            return

        if cycle_time <= 0:
            messagebox.showerror("Error", "Specified cycle time is not a positive integer.")
            logging.error("Cycle time specified in settings window is not a positive integer.")
            return

        config.cycle_time = cycle_time

        # Ensure entered ping_number is non-zero positive integer
        try:
            ping_number = int(self.count_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Specified ping number is not an integer.")
            logging.error("Ping number specified in settings window is not an integer.")
            return

        if ping_number <= 0:
            messagebox.showerror("Error", "Specified cycle ping number is not a positive integer.")
            logging.error("Ping number specified in settings window is not a positive integer.")
            return

        config.ping_number = ping_number

        config.set_quiet(self.quiet.get())

        self.sett_win.destroy()


def start_gui():
    """Initialize and start the tkinter GUI"""

    # Hopefully this will catch any startupt errors tk might have
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        logging.CRITICAL("Could not start GUI:" + exc)
        sys.exit(3)

    root.title("NetDash")
    app = App(root)
    root.mainloop()
