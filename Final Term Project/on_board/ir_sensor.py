from pyb import Pin, Timer, ADC

class IR_sensor:
    """
    Python class object for controlling a single IR sensor within an IR sensor Array
    
    """
    def __init__(self, input_pin: Pin):
        
        """
        Initializes an IR sensor object
        
        Args:
            input_pin (pyb Pin object): Pin should be initialized in Analog mode
            
        Returns:
            none
        """
        self.input_pin = input_pin
        self.ADC = ADC(input_pin)
        self.black_val = 0
        self.white_val  =0

    def read(self):
        """
        Reads the value from the sensor using pyb ADC protocol

        Returns
        -------
        float
            IR sensor reading value.

        """
        return self.ADC.read()

    def set_white(self, white_val):
        """
        Sets a baseline reference value for the IR sensor reading over white areas of the game board

        Parameters
        ----------
        white_val : float
            IR sensor reading when over a white area on the game board.

        Returns
        -------
        None.

        """
        self.white_val = white_val

    def set_black(self, black_val):
        """
        Sets a baseline reference value for the IR sensor reading over black areas of the game board

        Parameters
        ----------
        black_val : float
            IR sensor reading when over a black area on the game board.

        Returns
        -------
        None.

        """
        self.black_val = black_val
    # def sensor_on:

    # def sensor_off:
