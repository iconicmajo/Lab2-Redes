#Maria Jose Castro 181202
#Paula Camila Gonzalez #18398

import sys
import socket
import selectors
import types
from bitarray import bitarray

bta = bitarray()
#investigar que hace
sel = selectors.DefaultSelector()

#ingreso de data
port = input('Ingrese puerto: ')
host = input('Ingrese host: ')
nc = input('Ingrese numero de coneccion: ')
msj_ascii  = input('Ingrese mensaje: ')

#aqui vamos a convertir a ASCII el mensaje
#msj_ascii = ascii(msj_ascii)
#msj = bytes(msj_ascii, 'ASCII')
#print(msj)
#bta.frombytes(b'%msj_ascii')
#print(str(bta))

arr = bytes(msj_ascii, 'utf-8')
print("hola")
#arr2 = bytes(msj_ascii, 'ascii')

print(str(arr))
bta.frombytes(arr)
print(bta)

#Funcion para hacer la conecxion con el server
def conection(host, port, nc):
  server_info = (host, port)
  for i in range(0, nc):
    conection_id = i + 1
    print('Conectando ... ', )
    print('Numero de conexion', conection_id)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_info)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        conection_id=conection_id,
        msg_total=sum(len(m) for m in messages),
        recv_total=0,
        messages=list(messages),
        outb=b"",
    )
    sel.register(sock, events, data=data)
