import tkinter as tk

from src.host import Host


class App:

    def __init__(self, master):

        status_pane = tk.PanedWindow(master, orient=tk.HORIZONTAL, showhandle=True)
        status_pane.pack(fill=tk.BOTH, expand=1)

        for host in Host.hosts:
            host_status = tk.Label(status_pane, text=host.status)
            status_pane.add(host_status)
            host.widget = host_status


def start_gui():
    root = tk.Tk()
    root.title("NetDash")
    app = App(root)
    root.mainloop()


# TODO: Add start_tui() function, likely use curses
