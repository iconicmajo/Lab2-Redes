"""
LABORATORIO 2 - REDES
Maria Jose Castro 181202
Paula Camila Gonzalez 18398
"""

import sys
import struct

if sys.version_info > (3,):
    long = int

class Error_de_checksum(Exception):

    def __init__(self, checksum0, checksum1):
        Exception.__init__(self, "si los checksum son diferentes: {} vs {}".format(
            hex(checksum0.a) + hex(checksum0.a),
            hex(checksum1.a) + hex(checksum1.b)))
        self.checksum0 = checksum0
        self.checksum1 = checksum1


class Algoritmo_Checksum:

    checksum_struct = struct.Struct("<B")
    def __init__(self, a=0, b=0):
        if not isinstance(a, (int, long)):
            raise TypeError("El argumento de checksum es de diferente tipo pero es un {}.".format(
                type(a)))
        if not isinstance(b, (int, long)):
            raise TypeError("el argumento b debe ser diferente tipo pero es un {}.".format(
                type(b)))
        self.a = int(a & 0xFF)
        self.b = int(b & 0xFF)

    if sys.version_info > (3,):
        @staticmethod
        def from_bytestrings(*args):
            a = 0
            b = 0
            for arg in args:
                for x in arg:
                    a += x
                    b += a
            return Algoritmo_Checksum(a & 0xFF, b & 0xFF)
    else:
        @staticmethod
        def from_bytestrings(*args):
            a = 0
            b = 0
            for arg in args:
                for byte in arg:
                    a += ord(byte)
                    b += a
            return Algoritmo_Checksum(a & 0xFF, b & 0xFF)
    def update(self, byte):
        self.a = (self.a + ord(byte)) & 0xFF
        self.b = (self.b + self.a) & 0xFF

    def __repr__(self):
        return "Algoritmo_Checksum({}, {})".format(self.a, self.b)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not self == other
        
    def bytes(self):
        return self.checksum_struct.pack(self.a)\
             + self.checksum_struct.pack(self.b)

    def check_equal(self, other):
        if self != other:

            raise Error_de_checksum(self, other)