class Host:
    """Host class, holds list of all hosts"""

    hosts = []

    def __init__(self, ip_address, label=None):
        self.ip = ip_address
        self.label = str(self.ip)
        self.status = "UNKNOWN"
        self.status_widget = None

        if label:
            self.label = label

    def set_status_color(self, status_color):
        self.status_widget.delete("all")
        self.status_widget.create_rectangle(0, 0, 100, 50, fill=status_color)
