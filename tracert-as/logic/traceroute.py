import socket
import struct
import random

import logic.network_utils as nu
import logic.utils as u
import logic.whois as w


class Traceroute:
    ID = random.randint(0, 65535)

    def __init__(self, args):
        self.args = args
        self.port = random.choice(range(33434, 33535))
        self.ttl = 1
        self.sock = nu.NetworkUtils.create_tracert_socket('', self.port)
        self.address = socket.gethostbyname(self.args.host)
        self.output = []
        self.current_res = []

    def trace(self):
        """Method traces the route to the chosen destination"""
        print(u.Utils.create_start_tracing(self.args.host, self.address,
                                           self.args.hops), end='\r\n')

        while self.ttl < self.args.hops:
            packet = u.Utils.create_packet(self.ttl)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL,
                                 struct.pack('I', self.ttl))
            received_addr = self.trace_one_packet(packet)

            print('\r\n'.join(self.current_res), end='\r\n\r\n')
            self.current_res = []

            if received_addr == self.address:
                print('Tracing complete!')
                break
            self.ttl += 1

    def trace_one_packet(self, packet):
        """Main tracert algorithm"""
        self.sock.sendto(packet, (self.address, self.port))

        try:
            data, received_addr = self.sock.recvfrom(1024)
            received_addr = received_addr[0]

        except socket.timeout:
            received_addr = '*'

        self.current_res.append(f'{self.ttl}. {received_addr}')

        if received_addr != '*':
            info = w.get_info_about(received_addr)
            self.current_res.append(', '.join(info))

        return received_addr
