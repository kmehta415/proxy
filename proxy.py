#creating a  python tool to be used a as a proxy

import sys
import threading
import socket

def server_loop(local_host,local_port,remote_host,remote_port ,recv_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host,local_port))

    except:
        
        print('[*] Unahndled exception caught.....!!!')
        print('[*] Could not establish connection at %s:%d....!!!!' %(local_host,local_port))
        sys.exit(0)

    print('[*] Connected to the localhost at port %d ' %(local_port))

    server.listen(5)

    while True:
        
        client_socket , addr = server.accept()
        print('[*] [<== got connected at %s:%d' %(addr[0],addr[1]))
        client_thread = threading.Thread(target = proxy_handler , args = (client_socket,remote_host,remote_port,rev_first))
        client_thread.start()

def main():

    if len(sys.argv[1:]) != 5 :
           print('Usage: ./proxy.py [local_host] [local_port] [remote_host] [remote_port] [recv_first]')
           print('Examples:')
           print(' ./proxy.py 127.0.0.1 9000 192.168.68.131 9000 True')
           sys.exit(0)

    local_host = sys.argv[1]
    local_port = sys.argv[2]

    #declaring the remote hosts accordingly in the process

    remote_host = sys.argv[3]
    remote_port = sys.argv[4]

    recv_first = sys.argv[5]

    if "True" in rev_first:
        recv_first = True

    else:
        recv_first = False

    server_loop(local_host,local_port,remote_host,remote_port,recv_first)

main()
#calling the main function by default


def proxy_handler(client_socket,remote_host,remote_port,recv_first):

    remote_socket = socket.socket(socket.F_INET ,socket.SOCK_STREAM)

    remote_socket.connect((remote_host,remote_port))

    if recv_first :
        
        remote_buffer = recv_from(remote_socket)
        hexdump(remote_buffer)

        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer) :
            print('[<==] Sending %d bytes to the localhost' %(len(remot_buffer)))
            client_socket.send(remote_buffer)

    while True:
        
        local_buffer = recv_from(client_socket)

        if len(local_handler):
            
            print('[==>] Recieved %d bytes from remote' %(len(local_buffer)))
            hexdump(local_buffer)
        
            local_buffer =  request_handler(local_buffer)

            remote_socket.send(local_buffer)
            print('[==>] Sent to remote.')

        remote_buffer = recv_from(remote_socket)

        if len(remote_buffer):

            print('[<==] Recieved %d bytes from the remote' %(len(remote_buffer)))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)

            client_socket.send(remote_buffer)

            print('[<==] Sent to the localhost.')


        if not len(local_buffer) or not len(remote_buffer):

            client_socket.close()
            remote_socket.close()
            print('[*] No more data.Closing connection')

            break

def hexdump(src, length=16):
    
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in range(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines)

def recv_from(connection):
    buffer = ""
    connection.settimeout(2)

    while True:
        
        try:
            data = connection.recv(4096)

            if not data :
                break

            buffer += data

        except:
            pass

        return buffer

def response_handler(buffer):
    return buffer

def request_handler(buffer):
    return buffer
