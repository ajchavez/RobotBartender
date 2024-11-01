from TMC2209_Raspberry_Pi.src.TMC_2209.TMC_2209_StepperDriver import *
import time, sys
def my_callback(channel):
    pass

def moveStepper(steps):
    tmc = TMC_2209(21,16,20)
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
    tmc.set_stallguard_callback(26,80,my_callback)
        
    tmc.set_motor_enabled(True)
    tmc.run_to_position_steps(steps, MovementAbsRel.RELATIVE) 
    tmc.set_motor_enabled(False)
    tmc.deinit()
def triggerServo():
    from adafruit_servokit import ServoKit
    kit = ServoKit(channels=16)
    kit.servo[7].angle = 30
    time.sleep(2)
    kit.servo[7].angle = 90    
if __name__ == "__main__":
    #import sys
    print(sys.argv[1])
    stepper = moveStepper(int(sys.argv[1]))
    triggerServo()
    #stepper = moveStepper(-1000)
        
