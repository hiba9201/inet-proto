#!/usr/bin/env python3

import argparse
import socket
import sys

import logic.traceroute as tr


def create_args():
    parser = argparse.ArgumentParser(
        description='Python3.7 implementation of traceroute utility.')
    parser.add_argument('host', type=str,
                        help='Destination to which utility traces route')
    parser.add_argument('-m', '--max', type=int,
                        default=64, dest='hops', action='store',
                        help='Max "ttl"')

    return parser.parse_args()


def main():
    args = create_args()
    try:
        traceroute = tr.Traceroute(args)
    except PermissionError as e:
        sys.stderr.write(e.strerror + '\n')
        sys.exit(1)
    except socket.gaierror:
        sys.stderr.write('Destination address is unknown\n')
        sys.exit(2)

    traceroute.trace()


if __name__ == '__main__':
    main()
