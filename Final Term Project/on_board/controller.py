

from time import ticks_diff
class CLMotorController():
    """
    A closed-loop Proportional-Integral controller object that is used to set a desired wheel speed in mm/s
    
    """
    
    
    def __init__(self, target, old_ticks, old_state, Kp=1, Ki=1, min_sat=-100, max_sat=100, t_init=0,
                 v_nom=9.0, threshold=5.0, K3=0.06, use_integral=1):
        """
        Initializes a motor control object

        Parameters
        ----------
        target : int
            Desired motor speed in mm/s
        old_ticks : int
            System clock counter in microseconds
        old_state : int
            Not used, should remove
        Kp : float, optional
            Proportional gain constant. The default is 1.
        Ki : float, optional
            Integral gain constant. The default is 1.
        min_sat : int, optional
            Saturation lower limit for error accumulation. The default is -100.
        max_sat : int, optional
            Saturation upper limit for error accumulation. The default is 100.
        t_init N/A: , optional
            Unused, should remove
        v_nom : float, optional
            Nominal voltage of the batteries, used to correct for battery drain. The default is 9.0.
        threshold : int, optional
            Appears to be unused. The default is 5.0.
        K3 : float, optional
            Constant to convert velocity from ticks/s to mm/s; value found from motor step response test. The default is 0.61.
        use_integral : int, optional
            Indicates whether integral error should be used. The default is 1.

        Returns
        -------
        None.

        """
        
        
        self.target = target
        self.old_ticks = old_ticks
        self.old_state = old_state
        self.Kp = Kp
        self.Ki = Ki
        self.min_sat = min_sat
        self.max_sat = max_sat
        self.error = 0
        self.acc_error = 0
        self.dt = 0
        self.t_init = t_init
        self.v_nom = v_nom # expected/ideal battery level
        self.v_bat = self.v_nom
        self.bat_gain = self.v_nom/self.v_bat
        self.threshold = threshold # threshold for battery signal
        self.K1 = 1.637 # (wheel degrees/sec)/ mm/s
        self.K2 = 0.25 # wheel degrees per encoder count
        self.K3 = K3 # effort=%pwm / (wheel degrees/sec)
        self.KWindup = 0.1
        self.use_integral = use_integral
    def set_Kp(self, Kp):
        """
        Sets the proportional gain constant

        Parameters
        ----------
        Kp : float
            Proportional gain constant.

        Returns
        -------
        None.

        """
        
        self.Kp = Kp

    def set_Ki(self, Ki):
        """
        Sets the integral gain constant

        Parameters
        ----------
        Ki : float
            Integral gain constant.

        Returns
        -------
        None.

        """
        
        self.Ki = Ki

    def set_min_sat(self, min_sat):
        """
        Sets minimum saturation for error accumulation

        Parameters
        ----------
        min_sat : int
            Minumum saturation for error accumulation.

        Returns
        -------
        None.

        """
        self.min_sat = min_sat

    def set_target(self, target):
        """
        Sets target speed value, in mm/s

        Parameters
        ----------
        target : int
            Desired wheel speed in mm/s.

        Returns
        -------
        None.

        """
        self.target = target
    def set_battery(self, v_bat):
        
        """
        Sets the battery level and calculates the gain
        
        Args:
            v_bat (float): Measured battery voltage
        Returns:
            none
            
        """
        # sets the battery level and calculates the gain
        self.v_bat = v_bat
        self.bat_gain = self.v_nom/self.v_bat
    def disable_integral_error(self):
        
        """
        Disables integral error in the control loop
        
        Returns:
            none
        """
        self.use_integral = 0
    def enable_integral_error(self):
        """
        Enables integral error in the control loop

        Returns
        -------
        None.

        """
        
        self.use_integral = 1

    def get_action(self, new_ticks, new_state):
        
        """
        Runs a closed-loop Proportional-Integral controller to adjust motor speed to the desired setpoint (see Control Loops page). Returns necessary motor PWM percentage
        
        Parameters
        ----------
            new_ticks (int): Timer reading in microseconds
            new_state (int): Motor's encoder reading, in ticks
            
        Returns:
            float:
                PWM percentage the motor should run at to reach desired setpoint speed
                
        """
        # new_state is a velocity in counts/sec
        # new_ticks is a count in microseconds
        # To calculate error, first convert set point in mm/s to wheel deg/sec
        # Scale for battery droop
        raw_error = (self.target*self.K1 - new_state*self.K2) # error in WHEEL DEGREES/SEC
        if raw_error<5000 and raw_error>-5000: # hard-coded method of ignoring faulty encoder reading spikes
            self.error = raw_error
        else:
            self.error = 0
        if(self.old_ticks == 0):
            self.old_ticks = new_ticks
            # print(f"init!: self")
        else:
            self.dt = ticks_diff(new_ticks, self.old_ticks)/1E6
            self.acc_error = self.use_integral*(self.acc_error + self.error*self.dt) #Integral error, equivalent to degrees
            self.old_ticks = new_ticks
        # do control algorithm
        raw_ctrl_sig = (self.Kp*self.error + self.Ki*self.acc_error*self.use_integral) # control output in wheel degrees per second
        ctrl_sig = raw_ctrl_sig*self.K3
        # if ctrl_sig>self.max_sat:
        #     ctrl_sig -= self.KWindup*(ctrl_sig-self.max_sat)
        # elif ctrl_sig>self.max_sat:
        #     ctrl_sig -= self.KWindup*(ctrl_sig-self.max_sat)
        # Units: desired in deg/s, err in deg/s, acc in total deg, raw in deg/s, sig in %pwm=effort
        # print(f"desired: {self.target*self.K1}, curr: {new_state*self.K2},Err: {self.error}, Acc: {self.acc_error}, Raw: {raw_ctrl_sig}, Sig: {ctrl_sig}")
        # print(f"CTRL SIG: {ctrl_sig}, bat_gain: {self.bat_gain}")
        ctrl_sig = max(ctrl_sig, self.min_sat) # apply saturation
        ctrl_sig = min(ctrl_sig, self.max_sat)
        if abs(ctrl_sig) >= self.max_sat:
            # Stop integrating if saturated in same direction
            if (ctrl_sig > 0 and self.error > 0) or (ctrl_sig < 0 and self.error < 0):
                self.acc_error -= self.error*self.dt  # undo last integral term
                self.acc_error *= self.use_integral
        return ctrl_sig

class IRController():
    """
    A closed-loop Proportional-Integral controller that is used to adjust the IR sensor to have it's centroid centered at the target value (0 for center of sensor)
    
    """
    def __init__(self, target, old_ticks, old_state, K3, Kp=1, Ki=1, min_sat=-4, max_sat=4, t_init=0,use_integral=1):
        """
        Initializes an IRController Object

        Parameters
        ----------
        target : float
            Desired centroid setpoint for the IR sensor array.
         old_ticks : int
             System clock counter in microseconds
         old_state : int
             Not used, should remove
        K3 : float
            Sensitivity or scaling factor used to translate controller output to a wheel speed difference in mm/s.
        Kp : float, optional
            Proportional gain constant. The default is 1.
        Ki : float, optional
            Integral gain constant. The default is 1.
        min_sat : float, optional
            Minimum value for error saturation. The default is -4.
        max_sat : float, optional
            Maximum value for error saturation. The default is 4.
        t_init : N/A, optional
            unused, should remove. The default is 0.
        use_integral : int, optional
            Indicates whether integral error should be used. The default is 1.

        Returns
        -------
        None.

        """
        # super().__init__(target, old_ticks, old_state, Kp, Ki, min_sat, max_sat, t_init)
        self.target = target
        self.old_ticks = old_ticks
        self.old_state = old_state
        self.Kp = Kp
        self.Ki = Ki
        self.min_sat = min_sat
        self.max_sat = max_sat
        self.error = 0
        self.acc_error = 0
        self.dt = 0
        self.t_init = t_init
        self.K1 = 1 # no scaling needed since sensor reading and setpoint are both milimeters of deviation
        self.K2 = 1 # no scaling needed, ^
        self.K3 = K3 # sensitivity relation between PI signal and motor speed differential in mm/s
        self.use_integral = use_integral
    def set_Kp(self, Kp):
        """
        Sets the proportional gain constant

        Parameters
        ----------
        Kp : float
            Proportional gain constant.

        Returns
        -------
        None.

        """
        self.Kp = Kp

    def set_Ki(self, Ki):
        """
        Sets the integral gain constant

        Parameters
        ----------
        Ki : float
            Integral gain constant.

        Returns
        -------
        None.

        """
        self.Ki = Ki

    def set_min_sat(self, min_sat):
        """
        Sets minimum saturation for error accumulation

        Parameters
        ----------
        min_sat : int
            Minumum saturation for error accumulation.

        Returns
        -------
        None.

        """
        self.min_sat = min_sat

    def set_target(self, target):
        """
        Sets target centroid location, in mm with 0 defined as the center of the array

        Parameters
        ----------
        target : float
            Desired centroid location, with 0 defined as the center of the array

        Returns
        -------
        None.

        """
        self.target = target
    def disable_integral_error(self):
        """
        Disables integral error in the control loop
        
        Returns:
            none
        """
        self.use_integral = 0
    def enable_integral_error(self):
        """
        Enables integral error in the control loop

        Returns
        -------
        None.

        """
        self.use_integral = 1

    def get_action(self, new_ticks, new_state): # ticks in us, state in mm (centroid location)
        # new_ticks is a count in microseconds
        """
        Determines a necessary adjustment to locate the centroid of the sensor array at the specified target value
        
        Args:
            new_ticks (int): Timer reading in microseconds
            new_state (float): Current centroid location of the line in the sensor array
            
        Returns:
            (float): Difference between actual and desired centroid location, in mm
                
        """
        self.error = (self.target*self.K1 - new_state*self.K2) # mm difference of centroid location
        if(self.old_ticks == 0):
            self.old_ticks = new_ticks
        else:
            self.dt = ticks_diff(new_ticks, self.old_ticks)/1E6 # time step passed
            self.acc_error = self.use_integral*(self.acc_error + self.error*self.dt) #Integral error, equivalent to mm of centroid
            self.old_ticks = new_ticks
        # do control algorithm
        raw_ctrl_sig = (self.Kp*self.error + self.Ki*self.acc_error*self.use_integral) # control output in
        ctrl_sig = raw_ctrl_sig*self.K3
        
        ctrl_sig = max(ctrl_sig, self.min_sat) # apply saturation
        ctrl_sig = min(ctrl_sig, self.max_sat)
        return ctrl_sig

class PositionController():
    """
    A closed-loop Proportional-Integral controller that is used to adjust the heading angle to a desired value
    """
    
    def __init__(self, target, old_ticks, old_state, K3, Kp=1, Ki=1, min_sat=-30, max_sat=30, t_init=0, use_integral=1):
        # super().__init__(target, old_ticks, old_state, Kp, Ki, min_sat, max_sat, t_init)
        """
        
        Initializes a PositionController Object

        Parameters
        ----------
        target : float
            Desired heading angle, in radians.
         old_ticks : int
             System clock counter in microseconds
         old_state : int
             Not used, should remove
        K3 : float
            Sensitivity or scaling factor used to translate controller output to a wheel speed difference in mm/s.
        Kp : float, optional
            Proportional gain constant. The default is 1.
        Ki : float, optional
            Integral gain constant. The default is 1.
        min_sat : float, optional
            Minimum value for error saturation. The default is -30.
        max_sat : float, optional
            Maximum value for error saturation. The default is 30.
        t_init : N/A, optional
            unused, should remove. The default is 0.
        use_integral : int, optional
            Indicates whether integral error should be used. The default is 1.

        Returns
        -------
        None.

        
        
        
        """
        self.target = target
        self.old_ticks = old_ticks
        self.old_state = old_state
        self.Kp = Kp
        self.Ki = Ki
        self.min_sat = min_sat
        self.max_sat = max_sat
        self.error = 0
        self.acc_error = 0
        self.dt = 0
        self.t_init = t_init
        self.K1 = 1 # no scaling needed since sensor reading and setpoint are both milimeters of deviation
        self.K2 = 1 #
        self.use_integral = use_integral
        self.K3 = K3 # sensitivity relation between PI signal and motor speed differential in mm/s
    def set_Kp(self, Kp):
        """
        Sets the proportional gain constant

        Parameters
        ----------
        Kp : float
            Proportional gain constant.

        Returns
        -------
        None.

        """
        self.Kp = Kp

    def set_Ki(self, Ki):
        """
        Sets the integral gain constant

        Parameters
        ----------
        Ki : float
            Integral gain constant.

        Returns
        -------
        None.

        """
        self.Ki = Ki

    def set_min_sat(self, min_sat):
        """
        Sets minimum saturation for error accumulation

        Parameters
        ----------
        min_sat : int
            Minumum saturation for error accumulation.

        Returns
        -------
        None.

        """
        self.min_sat = min_sat

    def set_target(self, target):
        """
        Sets target yaw error in radians. In general, the target

        Parameters
        ----------
        target : float
            Desired centroid location, with 0 defined as the center of the array

        Returns
        -------
        None.

        """
    # Error is calculated by yaw_error_method, target should always be zero
        self.target = target

    def disable_integral_error(self):
        """
        Disables integral error in the control loop
        
        Returns:
            none
        """
        self.use_integral = 0

    def enable_integral_error(self):
        """
        Enables integral error in the control loop

        Returns
        -------
        None.

        """
        self.use_integral = 1

    def get_action(self, new_ticks, new_state): # ticks in us, 
        # new_ticks is a count in microseconds
        """
        Determines a necessary adjustment to bring heading angle to specified target value
        
        Args:
            new_ticks (int): Timer reading in microseconds
            new_state (float): Calculated heading angle difference needed to point in the direction of the desired endpoints
            
        Returns:
            (float): Angle adjustment needed to get to target value, in radians. This value is then scaled to create a wheel speed difference.
                
        """
        
        self.error = (self.target*self.K1 - new_state*self.K2) # mm difference of centroid location
        if(self.old_ticks == 0):
            self.old_ticks = new_ticks
            # print(f"init!: self")
        else:
            self.dt = ticks_diff(new_ticks, self.old_ticks)/1E6 # time step passed
            self.acc_error = self.use_integral*(self.acc_error + self.error*self.dt) #Integral error, equivalent to mm of centroid
            self.old_ticks = new_ticks
        # do control algorithm
        raw_ctrl_sig = (self.Kp*self.error + self.Ki*self.acc_error*self.use_integral) # control output in
        ctrl_sig = raw_ctrl_sig*self.K3
        # Units: desired in deg/s, err in deg/s, acc in total deg, raw in deg/s, sig in %pwm=effort
        # print(f"desired: {self.target*self.K1}, curr: {new_state*self.K2},Err: {self.error}, Acc: {self.acc_error}, Raw: {raw_ctrl_sig}, Sig: {ctrl_sig}")
        # print(f"CTRL SIG: {ctrl_sig}, bat_gain: {self.bat_gain}")
        ctrl_sig = max(ctrl_sig, self.min_sat) # apply saturation
        ctrl_sig = min(ctrl_sig, self.max_sat)
        return ctrl_sig