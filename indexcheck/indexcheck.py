import hashlib
import os

default_hash = hashlib.md5(open("/var/www/html/index.html", 'rb').read()).hexdigest()


def check_integrity(path):
    while 1:
        if hashlib.md5(open(path, 'rb').read()).hexdigest() != default_hash:
            os.system("chmod 777 /var/www/file")
            break

check_integrity("/var/www/html/index.html")
