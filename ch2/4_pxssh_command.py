from pexpect import pxssh


def send_command(s, command):
    s.sendline(command)
    s.prompt()
    print s.before


def connect(host, port, user, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password, port=port)
        return s
    except:
        print '[-] Error Connecting'
        exit(0)


def main():
    s = connect('127.0.0.1', '22', 'root', 'toor')
    send_command(s, 'echo hello')


if __name__ == '__main__':
    main()
