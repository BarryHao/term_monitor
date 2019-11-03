#!/usr/bin/env python
import modbus_library
import struct
from builtins import bytes
import binascii
import serial
import math
import time

def twos_complement(hexstr,bits):
     value = int(hexstr,16)
     if value & (1 << (bits-1)):
         value -= 1 << bits
     return value

class Modbus:
    def __init__(self, port_name, baudrate, box_ID, parity):
        modbus_library.BAUDRATE = baudrate
        self.instrument = modbus_library.Instrument(port_name, box_ID, mode ='rtu')
        self.instrument.debug = False
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = parity
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout  = 0.5   # seconds

    def optionalRead(self, request):
        answer = self.instrument._performCommand(3, request)
        if answer == None:
            return
        else:
            return answer

    def optionalWrite(self, request):
        answer = self.instrument._performCommand(6, request)
        if answer == None:
            return
        else:
            return answer

    def checkIOBoardType(self,registeraddress):
        # box address is 224~235
        request = '\x00'
        request += chr(int(registeraddress))
        request += '\x00\x04'
        answer = self.instrument._performCommand(3, request)

        if answer == None:
            return
        else:
            IOBoardType = []
            for i in answer:
                IOBoardType.append(hex(ord(i)))

            return IOBoardType

    def sensorON(self, registeraddress):
        request = '\x00'
        request += chr(int(registeraddress))
        request += '\x00\x01'
        answer = self.instrument._performCommand(6, request)

        if answer == None:
            return
        else:
            return answer

    def sensorOFF(self, registeraddress):
        request = '\x00'
        request += chr(int(registeraddress))
        request += '\x00\x00'
        answer = self.instrument._performCommand(6, request)

        if answer == None:
            return
        else:
            return answer

    def registerRead(self, registeraddress, signed = True):
        request = '\x00'
        request += chr(int(registeraddress))
        request += '\x00\x01'
        answer = self.instrument._performCommand(3, request)

        if answer == None:
            return
        else:
            value = 0
            data_num = int(ord(answer[0]))
            for i in range(data_num):
                value = value + int(ord(answer[i+1])) * math.pow( 256, data_num - 1 - i)
                # value = hex(value) & 0xffff

            if signed == True:
                value = twos_complement(hex(int(value)), 16)

            if self.instrument.debug:
                print("response value:", value)
            return value

    def registerHighDataRead(self, registeraddress, signed = True):
        request = '\x00'
        request += chr(int(registeraddress))
        request += '\x00\x01'
        answer = self.instrument._performCommand(3, request)

        if answer == None:
            return
        else:
            data_num = int(ord(answer[0]))
            value = int(ord(answer[1]))

            if signed == True:
                value = twos_complement(hex(int(value)), 16)

            if self.instrument.debug:
                print("response value:", value)
            return value

    def registerLowDataRead(self, registeraddress, signed = True):
        request = '\x00'
        request += chr(int(registeraddress))
        request += '\x00\x01'
        answer = self.instrument._performCommand(3, request)

        if answer == None:
            return
        else:
            value = 0
            data_num = int(ord(answer[0]))
            value = int(ord(answer[2]))

            if signed == True:
                value = twos_complement(hex(int(value)), 16)

            if self.instrument.debug:
                print("response value:", value)
            return value

    def registerRead_PM(self, registeraddress, signed = True):
        request1 = chr(int(registeraddress[0]))
        request1 += chr(int(registeraddress[1]))
        request1 += '\x00\x01'
        answer1 = self.instrument._performCommand(4, request1)

        request2 = chr(int(registeraddress[2]))
        request2 += chr(int(registeraddress[3]))
        request2 += '\x00\x01'
        answer2 = self.instrument._performCommand(4, request2)
        # print(registeraddress[0])
        # print(registeraddress[1])
        # print(registeraddress[2])
        # print(registeraddress[3])

        if answer1 == None:
            return
        elif answer2 == None:
            return
        else:
            data1 = str(hex(ord(answer1[1])))
            data2 = str(hex(ord(answer1[2])))
            data3 = str(hex(ord(answer2[1])))
            data4 = str(hex(ord(answer2[2])))

            # print("1dd: ", data1)
            # print("1ff: ", data2)
            # print("1ee: ", data3)
            # print("1gg: ", data4)

            if len(data1) < 4:
                data1 = '0' + data1[2:3]
            else:
                data1 = data1[2:4]

            if len(data2) < 4:
                data2 = '0' + data2[2:3]
            else:
                data2 = data2[2:4]

            if len(data3) < 4:
                data3 = '0' + data3[2:3]
            else:
                data3 = data3[2:4]

            if len(data4) < 4:
                data4 = '0' + data4[2:3]
            else:
                data4 = data4[2:4]

            # print("2dd: ", data1)
            # print("2ff: ", data2)
            # print("2ee: ", data3)
            # print("2gg: ", data4)
            data = data3 + data4 + data1 + data2
            value = struct.unpack('>f', binascii.unhexlify(data))
            time.sleep(0.05)

            return value[0]

    def registerWrite(self, registeraddress, value):
        if value > 65535 or value < 0:
            print("value parameter fault")

        else:
            request = '\x00'
            request += chr(int(registeraddress))
            request += chr(int(value/256))
            request += chr(int(value%256))

            if self.instrument.debug:
                print("output value:",value)
                print("(hex)dataH:",hex(int(value/256)))
                print("(hex)dataL:",hex(int(value%256)))
            answer = self.instrument._performCommand(6, request)

            if answer == None:
                return
            else:
                return answer
