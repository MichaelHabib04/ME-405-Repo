from pyb import Pin, Timer


class motor_driver:
    '''A motor driver interface encapsulated in a Python class. Works with
       motor drivers using separate PWM and direction inputs such as the DRV8838
       drivers present on the Romi chassis from Pololu.'''

    def __init__(self, PWM_pin: Pin, DIR_pin: Pin, nSLP_pin: Pin, tim: Timer, chan: int):
        """
        Initializes a Motor object
        
        Args:
            PWM_Pin (pyb Pin object): Pin used for PWM control; used to initialize a timerchannel
            DIR_pin (pyb Pin object): Pin used to control motor direction
            nSLP_pin (pyb Pin object): SLP Pin used to enable/disable motor
            tim (pyb Timer object): Timer used for PWM timerchannel
            chan (int): Timer channel number used to initialize PWM timerchannel
        
        Returns:
            none

        """
        self.DIR_pin = Pin(DIR_pin, mode=Pin.OUT_PP)
        self.nSLP_pin = Pin(nSLP_pin, mode=Pin.OUT_PP)
        self.PWM_chan = tim.channel(chan, pin=PWM_pin, mode=Timer.PWM, pulse_width_percent=0)

    def set_effort(self, effort):
        """
        Sets the present effort requested from the motor based on an input value between -100 and 100
        
        Args:
            effort (int): Desired motor effort, as PWM percentage
        Returns:
            none
           
           """
        if (effort > 0):
            self.DIR_pin.low()
            self.PWM_chan.pulse_width_percent(effort)
        else:
            self.DIR_pin.high()
            self.PWM_chan.pulse_width_percent(-effort)
        pass

    def enable(self):
        """
        Enables the motor driver by taking it out of sleep mode into brake mode
        
        Returns:
            none
        """
        # self.PA0.high()
        self.nSLP_pin.high()
        # self.PC8.high()
        pass

    def disable(self):
        """
        Disables the motor driver by taking it into sleep mode
        
        Returns: none
        """
        # self.PA0.low()
        self.nSLP_pin.low()
        # self.PC8.low()
    
