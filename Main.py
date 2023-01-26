import json
from TMC2209_Raspberry_Pi.src.TMC_2209.TMC_2209_StepperDriver import *
from adafruit_servokit import ServoKit
import time

class kathy:
    def __init__(self):
        self.LiquorSupply = json.load(open("LiquorSupply.json"))
        self.currentStepPosition = 0
        self.currentSlot = 0
        self.servoKit = ServoKit(channels=16)

    def saveLiquorSupply(self):
        json.dump(self.LiquorSupply, open("LiquorSupply.json", 'w'))

    def changeLiquor(self, slot, type = "Empty", mL = 0):
        self.LiquorSupply["Liquor Slots"][str(slot)]["type"] = type
        self.LiquorSupply["Liquor Slots"][str(slot)]["mL"] = mL
        self.saveLiquorSupply()

    def moveToLiquorSlot(self, slot):
        location = self.LiquorSupply["Liquor Slots"][str(slot)]["steps"]
        self.moveStepper(location - self.currentStepPosition)
        self.currentSlot = int(slot)
        print( self.currentStepPosition, location,location - self.currentStepPosition)
        self.currentStepPosition = location

    def moveStepper(self, steps):
        tmc = TMC_2209(21, 16, 20)
        tmc.set_loglevel(Loglevel.DEBUG)
        tmc.set_movement_abs_rel(MovementAbsRel.ABSOLUTE)
        tmc.set_direction_reg(False)
        tmc.set_current(300)
        tmc.set_interpolation(True)
        tmc.set_spreadcycle(False)
        tmc.set_microstepping_resolution(2)
        tmc.set_internal_rsense(False)
        tmc.readIOIN()
        tmc.readCHOPCONF()
        tmc.readDRVSTATUS()
        tmc.readGCONF()
        tmc.set_acceleration(2000)
        tmc.set_max_speed(500)
        def my_callback(channel):
            pass
        tmc.set_stallguard_callback(26, 80, my_callback)

        tmc.set_motor_enabled(True)
        tmc.run_to_position_steps(steps, MovementAbsRel.RELATIVE)
        tmc.set_motor_enabled(False)
        tmc.deinit()

    def triggerServo(self, slot):
        servoID = self.LiquorSupply["Liquor Slots"][str(slot)]["servo"]
        servoAnglePoor, servoAngleStandby = self.LiquorSupply["Servo Angles"]["poor"],self.LiquorSupply["Servo Angles"]["standby"]
        self.servoKit.servo[servoID].angle = servoAnglePoor
        time.sleep(1)
        self.servoKit.servo[servoID].angle = servoAngleStandby

    def triggerMixer(self, slot):
        pass

    def makeDrink(self, drinkName):
        pass

    def customDrink(self, name, liquors, mixers):
        pass


    def Full_Test(self):
        for key in self.LiquorSupply["Liquor Slots"].keys():
            self.moveToLiquorSlot(key)
            self.triggerServo(key)

if __name__ == "__main__":
    kathy = kathy()
    kathy.Full_Test()
    #kathy.changeLiquor(0, type = "Vodka", mL = 750)
