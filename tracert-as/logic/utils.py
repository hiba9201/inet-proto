import struct
import enum
import logic.traceroute as tr


class OutputType(enum.Enum):
    SUCCESS = 'OK'
    ERROR = 'ERROR'


class Utils:
    @staticmethod
    def create_start_tracing(host, addr, max_ttl):
        return (f'Tracing route to {host} ({addr}). ' +
                f'Max hops: {max_ttl}')

    @staticmethod
    def unpack_packet_header(header):
        return struct.unpack('!BBHHH', header)

    @staticmethod
    def get_checksum(packet):
        """Counts checksum for icmp-packet"""
        unpacked = struct.unpack('!LLLLLLLLLLLLL', packet)
        res = sum(unpacked)
        res += (res >> 16)

        return ~res & 0xffff

    @staticmethod
    def create_packet(sequence_number):
        """
        Creates echo request icmp-packet with chosen sequence number and ID
        """
        icmp_header = struct.pack('!BBHHH', 8, 0, 0, tr.Traceroute.ID,
                                  sequence_number)
        icmp_data = struct.pack('!QQQQQL', 2, 0, 0, 0, 0, 0)
        checksum = Utils.get_checksum(icmp_header + icmp_data)
        icmp_header = struct.pack('!BBHHH', 8, 0, checksum, tr.Traceroute.ID,
                                  sequence_number)

        return icmp_header + icmp_data
