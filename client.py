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

outb = bitarray()
#investigar que hace
sel = selectors.DefaultSelector()


#ingreso de data
port = int(input('Ingrese puerto: '))
host = input('Ingrese host: ')
nc = int(input('Ingrese numero de conexion: '))
msj  = input('Ingrese mensaje: ')

msj = ascii(msj)
#mensaje = mensaje.encode("ascii", "ignore")
msj_ascii = bytes(msj, 'ASCII')
msjs = [msj_ascii]

""" El mensaje se parsea a bytes 
msj_ascii = bytes(msj, 'utf-8')
msjs = [msj_ascii]
print(msjs) """
#print(str(msj_ascii))
# El mensaje en bytes se convierte a un bitarray (arreglo de boolean values) 
# ESTO VA EN EL SERVER
#outb.frombytes(msj_ascii)
#print(outb)

"""a_bytes = bytes(msj, "ascii")
msjs = [a_bytes]
#print(a_bytes)
outb.frombytes(a_bytes)
binary_converted=(' '.join(["{0:b}".format(x) for x in a_bytes]))
print("The Binary Representation is:", binary_converted) """


#Funciones para hacer la conexion con el server

def connection(host, port, nc):
  server_info = (host, port)
  for i in range(0, nc):
    i += 1
    print('Conectando ... ', )
    print('Numero de conexion', i)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_info)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        connection_id = i,
        full_msj=sum(len(m) for m in msjs),
        received_total=0,
        messages=list(msjs),
        outb=b"",
    )
    sel.register(sock, events, data=data)

def server_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        received_data = sock.recv(1024)  
        if received_data:
            print("La conexion con id ", data.connection_id, "recibio:", received_data)
            data.received_total += len(received_data)
        if not received_data or data.received_total == data.full_msj:
            print("Cerrando conexion ", data.connection_id)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print("Enviando ", repr(data.outb), " -> ",  "a la conexion", data.connection_id)
            sent = sock.send(data.outb)  
            data.outb = data.outb[sent:]


# Se verifica que toda la info haya sido ingresada para crear la conexion
if port == "" or  host == "" or nc == "" or msj  == "":
    print("Invalid data!\n")
    print("Ruta: <host: {}> <port: {}> <connections: {}>".format(host, port, nc))
    sys.exit(1)

print("Ruta: <host: {}> <port: {}> <connections: {}>".format(host, port, nc))
#host, port, num_conns = sys.argv[1:4]
connection(host, int(port), int(nc))

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                server_connection(key, mask)
                
        if not sel.get_map():
            break

except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()