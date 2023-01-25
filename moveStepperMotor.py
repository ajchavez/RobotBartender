from TMC2209_Raspberry_Pi.src.TMC_2209.TMC_2209_StepperDriver import *


class StepperMotor():
    def __init__(self):
        self.tmc = TMC_2209(21,16,20)
        
    def setup(self):
        self.tmc.set_loglevel(Loglevel.DEBUG)
        self.tmc.set_movement_abs_rel(MovementAbsRel.ABSOLUTE)
        self.tmc.set_direction_reg(False)
        self.tmc.set_current(300)
        self.tmc.set_interpolation(True)
        self.tmc.set_spreadcycle(False)
        self.tmc.set_microstepping_resolution(2)
        self.tmc.set_internal_rsense(False)
        self.tmc.readIOIN()
        self.tmc.readCHOPCONF()
        self.tmc.readDRVSTATUS()
        self.tmc.readGCONF()
        self.tmc.set_acceleration(2000)
        self.tmc.set_max_speed(500)
        self.tmc.set_stallguard_callback(26,80,self.my_callback)

    def my_callback(self, channel):
        self.tmc.stop()
        
    def move(self, steps):
        return self.tmc.run_to_position_steps(steps, MovementAbsRel.RELATIVE)
        
    def kill(self):
        self.tmc.set_motor_enabled(False)
        self.tmc.deinit()
        
        
if __name__ == "__main__":
    stepper = StepperMotor()
    stepper.setup()
    print(stepper.move(1000))
    stepper.kill()
        
