class Command():
    """
    A class containing information needed to execute pathing commands while navigating an obstacle course
    
    """
    def __init__(self, mode: str, end_condition: float, lin_speed: float, x_coord=0, y_coord=0):
        """
        Initializes an object to execute a pathing command
        
        Args:
            mode (string): mode to parse command type
            end_condition (float): indicates when command is done
            lin_speed (float): desired speed while command is executed
            x_coord (float): desired ending global x-coordinate
            y_coord (float): desired ending global y-coordinate
            
        Returns:
            none
        Modes: 
            "lin" for line follower mode
            "pos" for position follower mode
            "bmp" for bump sensor mode
            "rev" for blind reverse mode 
            
        End Conditions:
            Line follower mode: linear distance travelled in mm (s)
            Position follower mode: distance between Romi's current position and the target coordinates
            Blind reverse mode:linear distance travelled in mm (s)
        """
        
        self.mode = mode
        """
        modes: 
        "lin" for line follower mode
        "pos" for position follower mode
        "bmp" for bump sensor mode
        "rev" for blind reverse mode 
        "fwd" for forward mode
        "tip" for turn in place
        """
        self.end_condition = end_condition
        self.x_coord = x_coord #X coordinate. Can be ignored for modes other than 1
        self.y_coord = y_coord #Y coordinate. Can be ignored for modes other than 1
        self.lin_speed = lin_speed # desired linear speed of romi in mm/s
        
        
    def check_end_condition(self, state): # returns 1 if the end condition has been reached
        """
        Parameters
        ----------
        state (float):
            Argument from robot position tracker to compare against command end condition

        Returns
        -------
        int
            Indicates whether end condition is met

        """
    
        if self.mode == "pos":
            if state <= self.end_condition: # check that Romi is closer than the threshold
                return 1
        else:
            if self.end_condition > 0:
                if state >= self.end_condition: # for other states, the command has been fulfilled when the threshold is passed
                    return 1
            else:
                if state <= self.end_condition: # for other states, the command has been fulfilled when the threshold is passed
                    return 1
        return 0