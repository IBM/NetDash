import tkinter as tk

from src.host import Host


class App:

    COLUMN_LIMIT = 5    # Maximum number of hosts displayed in a row
    STATUS_WIDTH = 100  # Width of status rectangle
    STATUS_HEIGHT = 50  # Height of status regtangle

    def __init__(self, master):

        # Widget for the resizable host elements
        row = -1
        column = 0

        for idx, host in enumerate(Host.hosts):

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
            host_status.create_rectangle(0, 0, App.STATUS_WIDTH, App.STATUS_HEIGHT, fill="gray45")
            host_status.pack(side=tk.BOTTOM)

            # Set host status_widget so it can be modified later
            host.status_widget = host_status

            column += 1


def start_gui():
    # Initialize and start the tkinter GUI
    root = tk.Tk()
    root.title("NetDash")
    app = App(root)
    root.mainloop()


# TODO: Add start_tui() function, likely use curses
