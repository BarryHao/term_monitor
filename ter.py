from sensor_monitor import *
from time import *
import os.path
import datetime
import time
import sys
import csv

#Sensor Info
PATH = "/Users/BarryHao/Desktop/monitor_system/"
PORT_NAME = '/dev/cu.usbserial-DN03VH5T'
BAUDRATE = 19200

# part id
# box 3
BOX3_ID = 99
TEMP1_ID = 4
TEMP2_ID = 3

# powerMeter
PowerMeter_BOX_ID = 1
VOLTA_ID = [0x11, 0x0, 0x11, 0x1]
VOLTB_ID = [0x11, 0x12, 0x11, 0x13]
VOLTC_ID = [0x11, 0x24, 0x11, 0x25]
CURRENTA_ID = [0x11, 0x2, 0x11, 0x3]
CURRENTB_ID = [0x11, 0x14, 0x11, 0x15]
CURRENTC_ID = [0x11, 0x26, 0x11, 0x27]
PFA_ID = [0x11, 0xA, 0x11, 0xB]
PFB_ID = [0x11, 0x1C, 0x11, 0x1D]
PFC_ID = [0x11, 0x2E, 0x11, 0x2F]
KWA_ID = [0x11, 0x4, 0x11, 0x5]
KWB_ID = [0x11, 0x16, 0x11, 0x17]
KWC_ID = [0x11, 0x28, 0x11, 0x29]
KWHA_ID = [0x11, 0xC, 0x11, 0xD]
KWHB_ID = [0x11, 0x1E, 0x11, 0x1F]
KWHC_ID = [0x11, 0x30, 0x11, 0x31]
FREQUENCY= [0x11, 0x48, 0x11, 0x49]

# init monitor
box3_sensors_id = Box3SensorAssignment(TEMP1_ID, TEMP2_ID)
powerMeter_sensors_id = PowerMeterSensorAssignment(VOLTA_ID, VOLTB_ID, VOLTC_ID,\
    CURRENTA_ID, CURRENTB_ID, CURRENTC_ID, PFA_ID, PFB_ID, PFC_ID, KWA_ID, KWB_ID,\
    KWC_ID, KWHA_ID, KWHB_ID, KWHC_ID, FREQUENCY)
monitor3 = Monitor3(PORT_NAME, BAUDRATE, BOX3_ID, box3_sensors_id)
powerMeterMonitor = PowerMeterMonitor(PORT_NAME, BAUDRATE, PowerMeter_BOX_ID, powerMeter_sensors_id)

#Read from perception sensors
gTemp1 = 0
gTemp2 = 0
gVoltALevel = 0
gVoltBLevel = 0
gVoltCLevel = 0
gCurrentALevel = 0
gCurrentBLevel = 0
gCurrentCLevel = 0
gPfALevel = 0
gPfBLevel = 0
gPfCLevel = 0
gKWALevel = 0
gKWBLevel = 0
gKWCLevel = 0
gKWHALevel = 0
gKWHBLevel = 0
gKWHCLevel = 0
gFrequencyLevel = 0

def create_csv(path, name):
    filePath = path + "/" + name + ".csv"
    with open(filePath,'w',newline='') as f:
        csv_write = csv.writer(f)
        csv_head = ["Time","VoltA","VoltB","VoltC",\
            "CurrentA","CurrentB","CurrentC",\
            "PfA","PfB","PfC",\
            "KWA","KWB","KWC",\
            "KWHA","KWHB","KWHC",\
            "Frequency","TEMP1","TEMP2"]
        csv_write.writerow(csv_head)

def sensorPerception():
    global gTemp1
    global gTemp2
    global gVoltALevel
    global gVoltBLevel
    global gVoltCLevel
    global gCurrentALevel
    global gCurrentBLevel
    global gCurrentCLevel
    global gPfALevel
    global gPfBLevel
    global gPfCLevel
    global gKWALevel
    global gKWBLevel
    global gKWCLevel
    global gKWHALevel
    global gKWHBLevel
    global gKWHCLevel
    global gFrequencyLevel

    startTime = time.time()
    gTemp1 = monitor3.readTemp1()
    gTemp2 = monitor3.readTemp2()
    gVoltALevel = powerMeterMonitor.readVoltA()
    gVoltBLevel = powerMeterMonitor.readVoltB()
    gVoltCLevel = powerMeterMonitor.readVoltC()
    gCurrentALevel = powerMeterMonitor.readCurrentA()
    gCurrentBLevel = powerMeterMonitor.readCurrentB()
    gCurrentCLevel = powerMeterMonitor.readCurrentC()
    gPfALevel = powerMeterMonitor.readPfA()
    gPfBLevel = powerMeterMonitor.readPfB()
    gPfCLevel = powerMeterMonitor.readPfC()
    gKWALevel = powerMeterMonitor.readKWA()
    gKWBLevel = powerMeterMonitor.readKWB()
    gKWCLevel = powerMeterMonitor.readKWC()
    gKWHALevel = powerMeterMonitor.readKWHA()
    gKWHBLevel = powerMeterMonitor.readKWHB()
    gKWHCLevel = powerMeterMonitor.readKWHC()
    gFrequencyLevel = powerMeterMonitor.readFrequency()
    print("spent time: ",time.time() - startTime , " (s)")

def CheckStatusAndRecord():
    global gTemp1
    global gTemp2
    global gVoltALevel
    global gVoltBLevel
    global gVoltCLevel
    global gCurrentALevel
    global gCurrentBLevel
    global gCurrentCLevel
    global gPfALevel
    global gPfBLevel
    global gPfCLevel
    global gKWALevel
    global gKWBLevel
    global gKWCLevel
    global gKWHALevel
    global gKWHBLevel
    global gKWHCLevel
    global gFrequencyLevel

    sensorPerception()

    fileDate = strftime("%m_%d_%Y")
    print("fileDate: ", fileDate)
    print("Check Status And Record")

    folderPath = PATH + fileDate
    if not os.path.isdir(folderPath):
        print("no file")
        os.mkdir(folderPath)

    fileExist = os.path.isfile(folderPath + "/monitor_data.csv")
    if fileExist:
        f = open(folderPath + "/monitor_data.csv", "a")
        f.write(strftime("%H:%M:%S") + ', ' + str(gVoltALevel) + ', ' + str(gVoltBLevel)\
            + ', ' + str(gVoltCLevel) + ', ' + str(gCurrentALevel) + ', ' + str(gCurrentBLevel)\
            + ', ' + str(gCurrentCLevel) + ', ' + str(gPfALevel) + ', ' + str(gPfBLevel)\
            + ', ' + str(gPfCLevel) + ', ' + str(gKWALevel) + ', ' + str(gKWBLevel)\
            + ', ' + str(gKWCLevel) + ', ' + str(gKWHALevel) + ', ' + str(gKWHBLevel)\
            + ', ' + str(gKWHCLevel) + ', ' + str(gFrequencyLevel) + ', ' + str(gTemp1)\
            + ', ' + str(gTemp2) + '\n')
        f.close()
    else:
        print("File monitor_data not created")
        create_csv(folderPath, "monitor_data")

def main(s = 5):
    global gTemp1
    global gTemp2
    global gVoltALevel
    global gVoltBLevel
    global gVoltCLevel
    global gCurrentALevel
    global gCurrentBLevel
    global gCurrentCLevel
    global gPfALevel
    global gPfBLevel
    global gPfCLevel
    global gKWALevel
    global gKWBLevel
    global gKWCLevel
    global gKWHALevel
    global gKWHBLevel
    global gKWHCLevel
    global gFrequencyLevel

    operationFlag = False
    print("Monitor System!")

    box3_type_list = monitor3.modbus.checkIOBoardType(0xE0)
    print(" ")
    if box3_type_list == None:
        print("No answer form box3")
        sys.exit()
    if powerMeterMonitor.readVoltA() == None:
        print("No answer form Power Meter")
        sys.exit()

    while True:
        try:
            while True:
                now = datetime.datetime.now()
                print("now.second: ", now.second)
                if now.second % s < 0.001 and operationFlag == False:
                    break
                else:
                    operationFlag = False

                time.sleep(1)

            if operationFlag == False:
                CheckStatusAndRecord()
                operationFlag = True

        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    main()
