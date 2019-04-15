"""
Implementation of Traceroute.
Salah Uddin
Python 2.7
"""

from socket import *
import socket
import struct
import time
import random
import sys
import geolocation


MAX_NUM_HOPS = 30
TIME_OUT = 2.0
NUM_OF_TEST = 3

sequece_number = 0

def checksum(packet):
    sum = 0
    count_to = (len(packet) / 2) * 2
    for count in xrange(0, count_to, 2):
        this = ord(packet[count + 1]) * 256 + ord(packet[count])
        sum = sum + this
        sum = sum & 0xffffffff

    if count_to < len(packet):
        sum = sum + ord(packet[len(source_string) - 1])
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff

    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def get_packet():
    icmp_req_type = 8
    code = 0
    check_sum = 0
    packet_id = random.randint(4000, 6000) & 0xFFFF
    global sequece_number
    sequece_number = sequece_number + 1

    header = struct.pack("bbHHh", icmp_req_type, code, check_sum, packet_id, sequece_number)

    sending_time = time.time()
    data = struct.pack("d", sending_time)

    check_sum = checksum(header + data)
    check_sum = htons(check_sum)

    header = struct.pack("bbHHh", icmp_req_type, code, check_sum, packet_id, sequece_number)
    packet = header + data

    return packet


def receive_response(raw_socket):
    try:
        packet, addr = raw_socket.recvfrom(1024)
        receive_time = time.time()
    except socket.timeout:
        return -1

    return (packet, addr, receive_time)


def get_socket():
    icmp = socket.getprotobyname("icmp")
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    raw_socket.settimeout(TIME_OUT)

    return raw_socket


def send_data(raw_socket, dest_addr):
    data = get_packet()
    raw_socket.sendto(data, (dest_addr, 0))


def print_route(ttl, hop_addr, rtt_info):
    hostname = ""
    try:
        hostaddr = socket.gethostbyaddr(hop_addr)
        hostname = hostaddr[0]
    except Exception:
        hostname = hop_addr

    print ttl, "  ",
    if hop_addr != "":
        hop_addr = "(" + hop_addr + ")"
        print hostname, hop_addr, "  ",

    for x in rtt_info:
        if x == "*":
            print x, " ",
        else:
            sys.stdout.write('%.03f ms  ' % x)
    print ""


def find_route(raw_socket, dest_addr):
    route_info = []
    for ttl in range(1, MAX_NUM_HOPS):
        raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))

        hop_addr = ""
        rtt_info = []
        for n in range(NUM_OF_TEST):
            send_data(raw_socket, dest_addr)
            send_time = time.time()

            response = receive_response(raw_socket)

            if response == -1:
                rtt_info.append("*")
            else:
                response_time = response[2]
                rtt = response_time - send_time
                rtt_info.append(rtt*1000)
                hop_addr = response[1][0]

        print_route(ttl, hop_addr, rtt_info)
        route_info.append((ttl, hop_addr, rtt_info))

        if dest_addr == hop_addr:
            return route_info;

    return route_info


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "<Usage:>"
        print "sudo python traceroute.py [host_name]"
        print "Ex. sudo python traceroute.py www.uh.edu"
        sys.exit()

    dest_name = sys.argv[1]

    try:
        dest_addr = socket.gethostbyname(dest_name)
    except:
        print dest_name + ": Name or service not known"
        print "Cannot handle \"host\" cmdline arg '" + dest_name + "' on position 1 (argc 1)"
        sys.exit()

    print "Traceroute to ", dest_name, "(", dest_addr, ")", MAX_NUM_HOPS, "hops max", "16 bytes packets"

    try:
        raw_socket = get_socket()
    except:
        print "Can't create socket! Please use superuser mode."
        sys.exit()

    route_info = find_route(raw_socket, dest_addr)
    raw_socket.close()

    print "\n\t Geolocation sequence of the route:"
    print "======================================================"
    geolocation.print_geolocation(route_info)
