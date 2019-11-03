import serial                          # import the module

def banner_top():
	print('   +-------------------------------------------+')
	print('   |   USB2SERIAL RS485 Read in Python 3.x     |')
	print('   +-------------------------------------------+')

def Usage():
	print('   | Windows -> COMxx     eg COM32             |')
	print('   | Linux   ->/dev/ttyS* eg /dev/ttyUSB0      |')
	print('   +-------------------------------------------+')

def banner_bottom():
	print('   +-------------------------------------------+')
	print('   |          Press Any Key to Exit            |')
	print('   +-------------------------------------------+')

banner_top()                           # Display the top banner
Usage()
COM_PortName = input('\n    Enter the COM Port Name ->')

#Opening the serial port

COM_Port = serial.Serial(COM_PortName) # open the COM port
print('\n   ',COM_PortName,'Opened')

COM_Port.baudrate = 9600               # set Baud rate
COM_Port.bytesize = 8                  # Number of data bits = 8
COM_Port.parity   = 'N'                # No parity
COM_Port.stopbits = 1                  # Number of Stop bits = 1

print('\n    Baud rate = ',COM_Port.baudrate)
print('    Data bits = ',COM_Port.bytesize)
print('    Parity    = ',COM_Port.parity)
print('    Stop bits = ',COM_Port.stopbits)

#Controlling DTR and RTS pins to put USB2SERIAL in Receive mode

COM_Port.setRTS(1) #RTS=1,~RTS=0 so ~RE=0,Receive mode enabled for MAX485
COM_Port.setDTR(1) #DTR=1,~DTR=0 so  DE=0,(In FT232 RTS and DTR pins are inverted)
                   #~RE and DE LED's on USB2SERIAL board will be off

print('\n    DTR = 1,~DTR = 0 so  DE = 0')
print('    RTS = 1,~RTS = 0 so ~RE = 0,Receive mode enabled for MAX485')

print('\n    Waiting for data.....\n')

RxedData = COM_Port.readline()
print('   ',RxedData, '\n')

COM_Port.close()                       # Close the Serial port

banner_bottom()                        # Display the bottom banner
dummy = input()                        # press any key to close
