"""
Multithreaded congestion creator
Salah Uddin
Python 2.7
"""

import socket
import time
import thread


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


def send_512KB():
    for i in range(0, 25):
        try:
            thread.start_new_thread( send_data, (i, data_size, sender_addr) )
            print "Start thread: ", i
            time.sleep(0.15)
        except:
            print "Unable to start thread: ", i


if __name__ == '__main__':
    data_size = 1024
    sender_addr = ('96.120.16.33', 10000)

    try:
        sending_rate = 0
        while True:
            print "current sending rate: ", sending_rate, " KB"
            print "add sending rate:",
            add_rate = raw_input()

            if (add_rate == 'yes') or (add_rate == 'y'):
                send_512KB()
                sending_rate += 512
            elif add_rate == 'exit':
                break

    except:
       print "Error: unable to send more datas"
