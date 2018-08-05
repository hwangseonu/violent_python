import optparse
from socket import *
from threading import *

screen_lock = Semaphore(value=1)


def conn_scan(host, port):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        s.send('Violent Python\r\n')
        result = s.recv(100)
        screen_lock.acquire()
        print '[+] %d/tcp open' % port
        print '[+] Result: ' + str(result)
    except:
        screen_lock.acquire()
        print '[-] %d/tcp closed' % port
    finally:
        screen_lock.release()
        s.close()


def port_scan(host, ports):
    try:
        ip = gethostbyname(host)
    except:
        print "[-] Cannot resolve '%s': Unkown host" % host
        return

    try:
        name = gethostbyaddr(ip)
        print '\n[+] Scan Results for: ' + name[0]
    except:
        print '\n[+] Scan Results for: ' + ip

    setdefaulttimeout(1)

    for port in ports:
        t = Thread(target=conn_scan, args=(host, int(port.strip())))
        t.start()


def main():
    parser = optparse.OptionParser('usage%prog -H <target host> -p <target port>')
    parser.add_option('-H', dest='host', type='string', help='specify target host')
    parser.add_option('-p', dest='ports', type='string', help='specify target port[s] separated by comma')

    options, args = parser.parse_args()

    host = options.host
    ports = str(options.ports).split(',')

    if (host is None) or (ports[0] is None):
        print parser.usage
        exit(0)
    port_scan(host, ports)


if __name__ == '__main__':
    main()
