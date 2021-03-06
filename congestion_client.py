"""
Multithreaded congestion creator
Salah Uddin
Python 2.7
"""

import socket
import time
import thread
import sys

DATA_SIZE = 1024


def get_dummy_data(size):
    data = ""
    for x in range(0, size):
        data = data + 's'

    return data


def send_data(thread_no, packet_size, sender_addr):
    data = get_dummy_data(packet_size)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    i = 0

    while True:
        sent = sock.sendto(data, sender_addr)
#        print thread_no, " sent data: ", sent
        time.sleep(50.0 / 1000.0);    # 20 KB / second

    sock.close()


def send_512KB(sender_addr):
    for i in range(0, 25):
        try:
            thread.start_new_thread( send_data, (i, DATA_SIZE, sender_addr) )
            print "Start thread: ", i
            time.sleep(0.15)
        except:
            print "Unable to start thread: ", i


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "<Usage:>"
        print "sudo python congestion_client.py [dest_ip] [dest_port]"
        print "Ex. sudo python congestion_client.py 96.120.16.33 5555"
        sys.exit()

    dest_ip = sys.argv[1]
    dest_port = int(sys.argv[2])
    sender_addr = (dest_ip, dest_port)

    try:
        sending_rate = 0
        while True:
            print "current sending rate: ", sending_rate, " Mb"
            print "add sending rate(y/exit):",
            add_rate = raw_input()

            if (add_rate == 'yes') or (add_rate == 'y'):
                send_512KB(sender_addr)
                sending_rate += 4
            elif add_rate == 'exit':
                break

    except:
       print "Error: unable to send more datas"
