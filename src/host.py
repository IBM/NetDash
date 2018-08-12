class Host:
    """Host class, holds list of all hosts"""

    hosts = []

    def __init__(self, ip_address):
        self.ip = ip_address
        self.status = "UNKNOWN"
