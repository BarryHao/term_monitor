#!/usr/bin/env python
#Author: Barry Hao, Tony Tsai
from modbus import *
import math

class Box1SensorAssignment():
    def __init__(self, ORP_id, PH_id, temp_id, oxygen_id, salt_id,\
        water1_high_id, water1_low_id, water2_high_id, water2_low_id):
        self.ORP = ORP_id
        self.PH = PH_id
        self.temp = temp_id
        self.oxygen = oxygen_id
        self.salt = salt_id
        self.water1_high = water1_high_id
        self.water1_low = water1_low_id
        self.water2_high = water2_high_id
        self.water2_low = water2_low_id

class Box1ActuatorAssignment():
    def __init__(self, pump_id, feeding_motor_id, filtering_motor_id, buzzer_id):
        self.pump = pump_id
        self.feeding_motor = feeding_motor_id
        self.filtering_motor = filtering_motor_id
        self.buzzer = buzzer_id

class Box2SensorAssignment():
    def __init__(self, group1_id, group2_id, group3_id, group4_id):
        self.group1_id = group1_id
        self.group2_id = group2_id
        self.group3_id = group3_id
        self.group4_id = group4_id

class Box2ActuatorAssignment():
    def __init__(self, heater_id, filling_motor_id, led_id, magnetic_door_id, group1_id, group2_id, group3_id, group4_id):
        self.heater = heater_id
        self.led = led_id
        self.filling_motor = filling_motor_id
        self.magnetic_door = magnetic_door_id
        self.group1_id = group1_id
        self.group2_id = group2_id
        self.group3_id = group3_id
        self.group4_id = group4_id

class Box3SensorAssignment():
    def __init__(self, temp1_id, temp2_id):
        self.temp1_id = temp1_id
        self.temp2_id = temp2_id

class PowerMeterSensorAssignment():
    def __init__(self, voltA_id, voltB_id, voltC_id,\
        currentA_id, currentB_id, currentC_id,\
        pfA_id, pfB_id, pfC_id,\
        kwA_id, kwB_id, kwC_id,\
        kwhA_id, kwhB_id, kwhC_id, frequency):
        self.voltA_id = voltA_id
        self.voltB_id = voltB_id
        self.voltC_id = voltC_id
        self.currentA_id = currentA_id
        self.currentB_id = currentB_id
        self.currentC_id = currentC_id
        self.pfA_id = pfA_id
        self.pfB_id = pfB_id
        self.pfC_id = pfC_id
        self.kwA_id = kwA_id
        self.kwB_id = kwB_id
        self.kwC_id = kwC_id
        self.kwhA_id = kwhA_id
        self.kwhB_id = kwhB_id
        self.kwhC_id = kwhC_id
        self.frequency = frequency

class Monitor1:
    def __init__(self, port_name, baudrate, box_id, sensors_id, actuators_id):
        self.modbus = Modbus(port_name, baudrate, box_id, serial.PARITY_EVEN)
        self.sensors_id = sensors_id
        self.actuators_id = actuators_id

    def readORP(self):
        answer = self.modbus.registerRead(self.sensors_id.ORP, signed = False)
        if answer == None:
            return
        else:
    	    # print("answer:",answer)
            if answer < 800:
                print("ORP sensor disconnect")
                return
            else:
                # answer = ((answer - 800.0) / 3200.0 * 2998.0) - 999.0
                answer = 0.3168 * answer - 255.02
                return answer

    def readPH(self):
        answer =  self.modbus.registerRead(self.sensors_id.PH, signed = False)
        if answer == None:
            return
        else:
            # print("answer:",answer)
            if answer < 800:
                print("PH sensor disconnect")
                return
            else:
                answer = 0.0044 * answer - 3.576
                return answer

    def readtemp(self):
        answer = self.modbus.registerRead(self.sensors_id.temp)
        if answer == None:
            return
        else:
            # print("answer:",answer)
            return answer / 10.0

    def readOxygen(self):
        answer = self.modbus.registerRead(self.sensors_id.oxygen, signed = False)
        if answer == None:
            return
        else:
            # print("answer:",answer)
            if answer < 800:
                print("Oxygen sensor disconnect")
                return
            else:
                # answer = ((answer/200.0 - 4.0) * 20.0 / 16.0)
                answer = 0.0063 * answer - 5.0807
                return answer

    def readSalt(self):
        answer = self.modbus.registerRead(self.sensors_id.salt)
        if answer == None:
            return
        else:
            # print("answer:",answer)
            if answer < 800:
                print("Salt sensor disconnect")
                return
            else:
                # answer = ((answer/200.0 - 4.0) * (66.7-1.32) / 16.0 + 1.32) * 10.0
                answer = 0.3862 * answer - 215.25
                return answer

    def readWater1High(self):
        return self.modbus.registerRead(self.sensors_id.water1_high)

    def readWater1Low(self):
        return self.modbus.registerRead(self.sensors_id.water1_low)

    def readWater2High(self):
        return self.modbus.registerRead(self.sensors_id.water2_high)

    def readWater2Low(self):
        return self.modbus.registerRead(self.sensors_id.water2_low)

    def writePump(self, value):
        if value == 0 or value == 1:
            return self.modbus.registerWrite(self.actuators_id.pump, value)
        else:
            print("Pump control parameter fault")
            return

    def writeFeedingMotor(self, value):
        if value == 0 or value == 1:
            return self.modbus.registerWrite(self.actuators_id.feeding_motor, value)
        else:
            print("FeedingMotor control parameter fault")
            return

    def writeFilteringMotor(self, value):
        if value == 0 or value == 1:
            return self.modbus.registerWrite(self.actuators_id.filtering_motor, value)
        else:
            print("FilteringMotor control parameter fault")
            return

    def writeBuzzer(self, value):
        if value == 0 or value == 1:
            return self.modbus.registerWrite(self.actuators_id.buzzer, value)
        else:
            print("Buzzer control parameter fault")
            return

class Monitor2:
    def __init__(self, port_name, baudrate, box_id, sensors_id, actuators_id):
        self.modbus = Modbus(port_name, baudrate, box_id, serial.PARITY_EVEN)
        self.sensors_id = sensors_id
        self.actuators_id = actuators_id

    def readFillingMotorStatus(self):
        return self.modbus.registerHighDataRead(self.sensors_id.group1_id)

    def readHeaterStatus(self):
        return self.modbus.registerLowDataRead(self.sensors_id.group1_id)

    def readMagneticDoorStatus(self):
        return self.modbus.registerHighDataRead(self.sensors_id.group2_id)

    def readPumpStatus(self):
        return self.modbus.registerHighDataRead(self.sensors_id.group3_id)

    def readFeedingMotorStatus(self):
        return self.modbus.registerLowDataRead(self.sensors_id.group3_id)

    def readFilteringMotorStatus(self):
        return self.modbus.registerHighDataRead(self.sensors_id.group4_id)

    def writeHeater(self, value):
        if value == 0 or value == 1:
            return self.modbus.registerWrite(self.actuators_id.heater, value)
        else:
            print("Heater control parameter fault")
            return

    def writeFillingMotor(self, value):
        if value == 0 or value == 1:
            return self.modbus.registerWrite(self.actuators_id.filling_motor, value)
        else:
            print("FillingMotor control parameter fault")
            return

    def writeMagneticDoor(self, value):
        if value == 0 or value == 1:
            return self.modbus.registerWrite(self.actuators_id.magnetic_door, value)
        else:
            print("MagneticDoor control parameter fault")
            return

    def writeLED(self, value):
        if value == 0 or value == 1:
            return self.modbus.registerWrite(self.actuators_id.led, value)
        else:
            print("LED control parameter fault")
            return

class Monitor3:
    def __init__(self, port_name, baudrate, box_id, sensors_id):
        self.modbus = Modbus(port_name, baudrate, box_id, serial.PARITY_NONE)
        self.sensors_id = sensors_id

    def readTemp1(self):
        answer = self.modbus.registerRead(self.sensors_id.temp1_id, signed = False)
        if answer == None:
            return
        else:
            # answer = 0.3168 * answer - 255.02
            return answer

    def readTemp2(self):
        answer = self.modbus.registerRead(self.sensors_id.temp2_id, signed = False)
        if answer == None:
            return
        else:
            answer = 0.3168 * answer - 255.02
            return answer

class PowerMeterMonitor:
    def __init__(self, port_name, baudrate, box_id, sensors_id):
        self.modbus = Modbus(port_name, baudrate, box_id, serial.PARITY_NONE)
        self.sensors_id = sensors_id

    def readVoltA(self):
        return self.modbus.registerRead_PM(self.sensors_id.voltA_id)

    def readVoltB(self):
        return self.modbus.registerRead_PM(self.sensors_id.voltB_id)

    def readVoltC(self):
        return self.modbus.registerRead_PM(self.sensors_id.voltC_id)

    def readCurrentA(self):
        return self.modbus.registerRead_PM(self.sensors_id.currentA_id)

    def readCurrentB(self):
        return self.modbus.registerRead_PM(self.sensors_id.currentB_id)

    def readCurrentC(self):
        return self.modbus.registerRead_PM(self.sensors_id.currentC_id)

    def readPfA(self):
        return self.modbus.registerRead_PM(self.sensors_id.pfA_id)

    def readPfB(self):
        return self.modbus.registerRead_PM(self.sensors_id.pfB_id)

    def readPfC(self):
        return self.modbus.registerRead_PM(self.sensors_id.pfC_id)

    def readKWA(self):
        return self.modbus.registerRead_PM(self.sensors_id.kwA_id)

    def readKWB(self):
        return self.modbus.registerRead_PM(self.sensors_id.kwB_id)

    def readKWC(self):
        return self.modbus.registerRead_PM(self.sensors_id.kwC_id)

    def readKWHA(self):
        return self.modbus.registerRead_PM(self.sensors_id.kwhA_id)

    def readKWHB(self):
        return self.modbus.registerRead_PM(self.sensors_id.kwhB_id)

    def readKWHC(self):
        return self.modbus.registerRead_PM(self.sensors_id.kwhC_id)

    def readFrequency(self):
        return self.modbus.registerRead_PM(self.sensors_id.frequency)
