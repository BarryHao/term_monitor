#!/usr/bin/env python
#Author: Barry Hao, Tony Tsai
from sensor_monitor import *

def operation():
    # communication setting
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

    box3_sensors_id = Box3SensorAssignment(TEMP1_ID, TEMP2_ID)
    powerMeter_sensors_id = PowerMeterSensorAssignment(VOLTA_ID, VOLTB_ID, VOLTC_ID,\
        CURRENTA_ID, CURRENTB_ID, CURRENTC_ID, PFA_ID, PFB_ID, PFC_ID, KWA_ID, KWB_ID,\
        KWC_ID, KWHA_ID, KWHB_ID, KWHC_ID, FREQUENCY)

    monitor3 = Monitor3(PORT_NAME, BAUDRATE, BOX3_ID, box3_sensors_id)
    powerMeterMonitor = PowerMeterMonitor(PORT_NAME, BAUDRATE, PowerMeter_BOX_ID, powerMeter_sensors_id)

    # # test
    for i in range(5):
        box3_type_list = monitor3.modbus.checkIOBoardType(0xE0)
        print(" ")
        if box3_type_list == None:
            print("No answer form box3")
        else:
            print("box3 is ready")
            print("box3_type_list:")
            for type in box3_type_list:
                print("  ", type)

        # # power meter test
        print(" ")
        print("power meter list:")
        print("  VoltA:", powerMeterMonitor.readVoltA())
        print("  VoltB:", powerMeterMonitor.readVoltB())
        print("  VoltC:", powerMeterMonitor.readVoltC())
        print("  CurrentA:", powerMeterMonitor.readCurrentA())
        print("  CurrentB:", powerMeterMonitor.readCurrentB())
        print("  CurrentC:", powerMeterMonitor.readCurrentC())
        print("  PfA:", powerMeterMonitor.readPfA())
        print("  PfB:", powerMeterMonitor.readPfB())
        print("  PfC:", powerMeterMonitor.readPfC())
        print("  KWA:", powerMeterMonitor.readKWA())
        print("  KWB:", powerMeterMonitor.readKWB())
        print("  KWC:", powerMeterMonitor.readKWC())
        print("  KWHA:", powerMeterMonitor.readKWHA())
        print("  KWHB:", powerMeterMonitor.readKWHB())
        print("  KWHC:", powerMeterMonitor.readKWHC())
        print("  Frequency:", powerMeterMonitor.readFrequency())

def main():
    print("Thermal Monitor Drive!")
    operation()

if __name__ == "__main__":
    main()
