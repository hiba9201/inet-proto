#!/usr/bin/env python3

import re

import logic.network_utils as nu


def whois(host, whois):
    sock = nu.NetworkUtils.create_whois_socket(whois)
    sock.send(bytes(host, 'utf-8') + b'\r\n')
    msg = ''
    with sock.makefile() as s:
        for line in s:
            msg += line

    return msg


def parse_msg(msg):
    info = []

    netname = re.findall(r'netname:\s+([\w.\-]+)$', msg,
                         re.MULTILINE | re.IGNORECASE)
    if len(netname):
        info.append(netname[0])

    origin = re.findall(r'origin:\s+([\w.\-]+)$', msg,
                        re.MULTILINE | re.IGNORECASE)
    if len(origin):
        info.append(re.findall(r'\d+', origin[0])[0])

    country = re.findall(r'country:\s+([\w.]+)$', msg,
                         re.MULTILINE | re.IGNORECASE)
    if len(country):
        info.append(country[0])

    return info


def get_info_about(host):
    msg = whois(host, 'whois.arin.net')

    referer = re.findall(r'ResourceLink:\s+([\w.]+)$', msg,
                         re.MULTILINE | re.IGNORECASE)

    if len(referer):
        return parse_msg(whois(host, referer[0]))

    msg = whois(host, 'whois.iana.org')

    referer = re.findall(r'whois:\s+([\w.]+)$', msg,
                         re.MULTILINE | re.IGNORECASE)

    if len(referer):
        return parse_msg(whois(host, referer[0]))

    return ['local']
