import socket


class NetworkUtils:
    @staticmethod
    def create_tracert_socket(host, port):
        """Creates socket for tracing"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                             socket.IPPROTO_ICMP)
        sock.settimeout(1)
        sock.bind((host, port))

        return sock

    @staticmethod
    def create_whois_socket(whois):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((whois, 43))

        return sock
