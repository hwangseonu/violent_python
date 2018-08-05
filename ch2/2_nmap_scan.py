import nmap
import optparse


def nmap_scan(host, port):
    scanner = nmap.PortScanner()
    scanner.scan(host, port)
    state = scanner[host]['tcp'][int(port)]['state']
    print '[+] %s tcp/%s %s' % (host, port, state)


def main():
    parser = optparse.OptionParser('usage %prog -H <target host> -p <target port>')
    parser.add_option('-H', dest='host', type='string', help='specify target host')
    parser.add_option('-p', dest='ports', type='string', help='specify target port[s] separated by comma')

    options, args = parser.parse_args()

    host = options.host
    ports = str(options.ports).split(',')

    if (host is None) or (ports[0] is None):
        print parser.usage
        exit(0)

    for port in ports:
        nmap_scan(host, port.strip())


if __name__ == '__main__':
    main()
