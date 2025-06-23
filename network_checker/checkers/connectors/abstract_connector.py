from abc import ABC, abstractmethod
import socket
from typing import Tuple

from checkers.exceptions import AccessError, NetworkError

class BaseConnector(ABC):
    @abstractmethod
    def check_network(self, config):
        pass

    @abstractmethod
    def check_connection(self, check_connection):
        pass

    def check(self, config) -> Tuple[str, str]:
        try:
            self.check_network(config)
        except NetworkError as e:
            return (str(e), "")

        try:
            self.check_connection(config)
        except AccessError as e:
            return ("✅ OK", str(e))
        
        return ("✅ OK", "✅ OK")



    def check_port_connectivity(self, host: str, port: int, timeout: int = 10) -> tuple[bool, str]:
        """Check if a port is reachable on a host."""
        try:
            sock = socket.create_connection((host, port), timeout)
            sock.close()
        except socket.timeout:
            raise NetworkError("❌ Connection timed out")
        except socket.error:
            raise NetworkError("❌ Connection failed")