#!/usr/bin/env python3
import argparse
import socket
import concurrent.futures
import time
import bitstring
import select

YEARS_CONST = 2208988800
HEADER_FORMAT = '''uint:2, uint:3, uint:3, uint:8, uint:8, int:8, float:32, 
                   float:32, uint:32, uint:32, uint:32, uint:32, uint:32,
                   uint:32, uint:32, uint:32, uint:32'''
HEADER_SIZE = 384


def get_seconds(time_since_epoch):
    return int(time_since_epoch + YEARS_CONST)


def get_split_seconds(time_since_epoch):
    return int(time_since_epoch % 1 * 1000000)


def process_client(server, delay):
    data, addr = server.recvfrom(HEADER_SIZE)
    receive_time = time.time()
    print(f'new client – {addr[0]}:{addr[1]}')

    bin_data = bitstring.BitArray(data)
    unpacked_request = bin_data.unpack(HEADER_FORMAT)

    receive_time_secs = get_seconds(receive_time) + delay
    receive_time_split = get_split_seconds(receive_time)

    start_time_secs = unpacked_request[15]
    start_time_split = unpacked_request[16]

    send_time = time.time()
    send_time_secs = get_seconds(send_time) + delay
    send_time_split = get_split_seconds(send_time)

    server.sendto(bitstring.pack(
        HEADER_FORMAT,
        0, 4, 4, 1, 0, 0, 0.0, 0.0, 0, 0, 0,
        start_time_secs, start_time_split,
        receive_time_secs, receive_time_split,
        send_time_secs, send_time_split
    ).bytes,
                  addr)


def main(args):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
            server.bind(('localhost', args.port))
            print(f'server started on localhost:{args.port}')
            while True:
                r, _, _ = select.select([server], [], [], 1)
                if r:
                    pool.submit(process_client, server, args.delay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delay', action='store', default=0, type=int,
                        dest='delay',
                        help='Delay of lying to clients in seconds')
    parser.add_argument('-p', '--port', action='store', default=123, type=int,
                        dest='port',
                        help='Server port. Default – 123')
    main(parser.parse_args())
