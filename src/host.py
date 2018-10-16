"""Holds the Host class"""

STATUS_COLORS = {         # Colors representing status
    "SUCCESS": "green2",
    "FAIL": "red2",
    "OTHER": "orange2"
}

hosts = []                # List of all hosts


class Host:
    """Host class"""

    def __init__(self, ip_address, label=None):
        self.ip = ip_address
        self.label = str(self.ip)
        self.status = "UNKNOWN"
        self.status_widget = None

        if label:
            self.label = label

    def set_status(self, status):
        """Set the status of the Host and update the status color (if applicable)"""

        self.status = status

        if self.status_widget is not None:
            self.status_widget.delete("all")
            self.status_widget.create_rectangle(0, 0, 100, 50, fill=STATUS_COLORS[status])
