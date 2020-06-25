#!/usr/bin/env python3

import argparse
import socket
import concurrent.futures
import random


rand = random.randint(2**16, 2**64 - 1).to_bytes(8, 'little')


def get_proto(bin_data):
    if bin_data.startswith(b'HTTP'):
        return 'HTTP'

    if b'SMTP' in bin_data:
        return 'SMTP'

    if b'POP3' in bin_data:
        return 'POP3'

    if b'IMAP' in bin_data:
        return 'IMAP'

    if (len(bin_data) >= 48 and 7 & bin_data[0] == 4 and
            bin_data[24:32] == rand):
        return 'NTP'

    if (len(bin_data) >= 12 and bin_data[:2] == b'\17\0' and
            bin_data[3] & 7 == 1):
        return 'DNS'

    return ''


def scan_tcp(port, ip):
    scanner = socket.socket()
    scanner.settimeout(0.5)
    try:
        scanner.connect((ip, port))
        scanner.send(b'0' * 250 + b'\r\n\r\n')
        data = scanner.recv(1024)
        print(f'TCP {port} {get_proto(data)}')
    except:
        pass
    finally:
        scanner.close()


def scan_udp(port, ip):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    scanner.settimeout(3)

    try:
        scanner.sendto(b'\17' + b'\0' * 39 + rand, (ip, port))
        data, _ = scanner.recvfrom(1024)
    except socket.error:
        pass
    except ConnectionResetError:
        pass
    else:
        print(f'UDP {port} {get_proto(data)}')
    finally:
        scanner.close()


def scan(ip, port, tcp, udp):
    if tcp:
        scan_tcp(port, ip)

    if udp:
        scan_udp(port, ip)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='udp/tcp simple port scanner')

    parser.add_argument('host', type=str, help='host to scan')
    parser.add_argument('-t', dest='is_tcp', action='store_true',
                        default=False, help='''scan tcp ports. scans both 
                        types of ports by default''')
    parser.add_argument('-u', dest='is_udp', action='store_true',
                        default=False, help='''scan udp ports. scans both 
                        types of ports by default''')
    parser.add_argument('-p', '--ports', dest='ports', nargs=2,
                        default=(1, 1000), type=int, help='ports range')

    args = parser.parse_args()

    if args.is_tcp == args.is_udp:
        args.is_tcp = True
        args.is_udp = True

    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as pool:
        for port in range(args.ports[0], args.ports[1] + 1):
            pool.submit(scan, args.host, port, args.is_tcp, args.is_udp)
