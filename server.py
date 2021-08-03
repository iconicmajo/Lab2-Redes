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

from fletcher_checksum import Algoritmo_Checksum, Error_de_checksum

from hamming import * 

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


def accept_wrapper(sock):
    connection, info = sock.accept()  
    print("Conexion aceptada de ", info)
    connection.setblocking(False)
    data = types.SimpleNamespace(info=info, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(connection, events, data=data)

def server_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        received_data = sock.recv(1024)
        if received_data:
            data.outb += received_data
            received=  binary_conversion(new_bta)
            checked = binary_conversion(data.outb)
            error_check = Algoritmo_Checksum(received, checked)
            
            #chequear = hamming(recido, 2)S
            #algoritmo_check = Algoritmo_Checksum()
        else:
            received=  binary_conversion(new_bta)
            checked = binary_conversion(data.outb)
            error_check = Algoritmo_Checksum(received, checked )
            print("Check_sum indica que la transmision fue exitosa: ",error_check)
            print("Cerrando conexion con ", data.info)
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

try:
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
    sel.close()
