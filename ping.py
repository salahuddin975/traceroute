"""
Implementation of ping.
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


MAX_NUM_HOPS = 240
TIME_OUT = 2.0

sequece_number = 0
rtt_cumulative = 0

def checksum(packet):
    sum = 0
    count_to = (len(packet) / 2) * 2
    for count in xrange(0, count_to, 2):
        this = ord(packet[count + 1]) * 256 + ord(packet[count])
        sum = sum + this
        sum = sum & 0xffffffff

    if count_to < len(packet):
        sum = sum + ord(packet[len(packet) - 1])
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
    raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', MAX_NUM_HOPS))

    return raw_socket


def send_data(raw_socket, dest_addr):
    data = get_packet()
    raw_socket.sendto(data, (dest_addr, 0))


def print_rtt_info(seq_no, addr, rtt):
    global rtt_cumulative
    rtt_cumulative = rtt_cumulative + rtt
    avg_ttl = rtt_cumulative/seq_no
    print str(seq_no) + ". ", addr, " time:", rtt, "ms,", " average:", avg_ttl, "ms"

    return avg_ttl


def find_avg_ttl(dest_name, dest_addr, num_of_test):
    try:
        raw_socket = get_socket()
    except:
        print "Can't create socket! Please use superuser mode."
        sys.exit()

    avg_ttl = 0
    hop_addr = dest_name + "(" + dest_addr + ")"

    for n in range(num_of_test):
        send_data(raw_socket, dest_addr)
        send_time = time.time()

        response = receive_response(raw_socket)

        if response == -1:
            rtt_info = 2000
        else:
            response_time = response[2]
            rtt = response_time - send_time
            rtt_info = rtt*1000

        avg_ttl = print_rtt_info(n+1, hop_addr, rtt_info)
        time.sleep(.1)

    raw_socket.close()
    return  avg_ttl


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "<Usage:>"
        print "sudo python ping.py [host_name] [num_of_experiment]"
        print "Ex. sudo python ping.py www.uh.edu 100"
        sys.exit()

    dest_name = sys.argv[1]
    num_of_test = int(sys.argv[2])

    try:
        dest_addr = socket.gethostbyname(dest_name)
    except:
        print dest_name + ": Name or service not known"
        print "Cannot handle \"host\" cmdline arg '" + dest_name + "' on position 1 (argc 1)"
        sys.exit()

    print "Ping to ", dest_name, "(", dest_addr, ")"

    avg_ttl = find_avg_ttl(dest_name, dest_addr, num_of_test)

    print "Average ttl: ", avg_ttl
