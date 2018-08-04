import zipfile
import optparse
from threading import *


def extract_file(zip_file, password):
    try:
        zip_file.extractall(pwd=password)
        print '[+] Found Password: ' + password + '\n'
    except:
        pass


def main():
    parser = optparse.OptionParser('usage%prog -f <zipfile> -d <dictionary>')
    parser.add_option('-f', dest='zname', type='string', help='specify zip file')
    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
    options, args = parser.parse_args()

    zname = options.zname
    dname = options.dname

    if (zname is None) or (dname is None):
        print parser.usage
        exit(0)

    zip_file = zipfile.ZipFile(zname)
    pass_file = open(dname)
    
    for line in pass_file.readlines():
        password = line.strip('\n')
        t = Thread(target=extract_file, args=(zip_file, password))
        t.start()


if __name__ == '__main__':
    main()
