"""
LABORATORIO 2 - REDES
Maria Jose Castro 181202
Paula Camila Gonzalez 18398
"""
import sys
import socket
import selectors
import types
from bitarray import bitarray

sel = selectors.DefaultSelector()

new_bta = bitarray()

#ingreso de data
port = int(input('Ingrese puerto: ') ) #8080
host = input('Ingrese host: ') #127.0.0.1

def binary_conversion(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def server_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        received_data = sock.recv(1024)
        if received_data:
            data.outb += received_data
            received=  binary_conversion(new_bta)
            checked = binary_conversion(data.outb)            
        else:
            received=  binary_conversion(new_bta)
            checked = binary_conversion(data.outb)
            sel.unregister(sock)
            sock.close()
            
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("echoing", data.outb, "to", data.info)
            sent = sock.send(data.outb)  
            data.outb = data.outb[sent:]

# Se utilizan las funciones para activar el server
if port == "" or  host == "":
    print("Servidor para: <host: {}> <port: {}>".format(host, port))
    sys.exit(1)

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

#Esto aun no funciona jeje pero eso lo miro manana 

'''try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                server_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()'''