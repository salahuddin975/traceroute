import sys
import ping
import congestion_client


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "<Usage:>"
        print "sudo python congestion_automated_tester.py [ping_ip] [data_sender_ip] [data_sender_port] " \
              "[num_of_ping_for_avg] [max_data_rate_in_Mb]"
        print "Ex. sudo python congestion_automated_tester.py  192.168.0.1  172.217.9.174  6969  50  50"
        sys.exit()

    ping_ip = sys.argv[1]
    dest_ip = sys.argv[2]
    dest_port = int(sys.argv[3])
    num_of_ping = int(sys.argv[4])
    max_data_rate = int(sys.argv[5])

    cur_data_rate = 0
    dest_addr = (dest_ip, dest_port)

    fd = open("ping_stats.txt", "w")
    info = "congestion_size_in_Mb" + "    " + "avg_ttl\n"
    fd.write(info)

    while cur_data_rate <= max_data_rate:
        avg_ttl = ping.find_avg_ttl(ping_ip, ping_ip, num_of_ping)
        info = str(cur_data_rate) + "\t\t\t" + str(avg_ttl) + "\n"
        fd.write(info)

        congestion_client.send_512KB(dest_addr)
        cur_data_rate = cur_data_rate + 4

    fd.close()
