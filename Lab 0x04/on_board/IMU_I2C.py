



class IMU_I2C:
    def __init__(self, I2Cobj): # Takes in I2C object configured in Controller mode
        self.I2Cobj = I2Cobj
    
    def changeOpMode():  # Change operating status to "fusion" mode provided by BNO055
        
        
    def retrieveCalStatus(): # Retrieve and parse calibration status byte
        
        
        
    def retrieveCalCoefficients():  # Retrieve calibration coefficients from IMU as bianary data
    
    
    
    
    def writeCalCoefficients(): # Writes cal coefficients from pre-recorded bianary data
    
    
    def readEulerAngles(): # Reads Euler Angles from the IMU
    
    
    def readAngluarVelocity(): # Reads angular velocity from the IMU
        

