from pyb import I2C
import time
import struct

"""! BNO055 Memory addresses !"""

op_mode_addr = 0x3D # Page 70 of the BNO055 data sheet
"""! Operation mode byte:
    Bits 4-7 reserved
    Bits 0-3 operation mode
    
    !"""

calib_stat_addr = 0x35 # Pg 67, Calibration Status Byte
calib_coeff_addr = 0x55 # Pg 50, Calibration Coefficients Starting Address
eul_head_lsb = 0x1A #Pg 52, Heading for Euler angle Starting Address


# """!
# Calibration Status Byte bit map;
# 3 indicates fully calibrated, 0 indicates not calibrated

# Bit 0 and 1 - Mag calib status
# Bit 2 and 3 - Acc
# Bit 4 and 5 - Gyr
# Bit 6 and 7 - Sys

# !"""

acc_data_x_lsb = 0x08 # Mem location where 
gyr_data_x_lsb = 0x14 # Pg 52, gyro data

    
"""! Data to write to BNO055 !"""


config_op_mode = 0b0000 # Page 21
IMU_op_mode = 0b1000 # Page 21
compass_mode = 0b1001 # Page 21
m4g_mode = 0b1010 # Page 21
ndof_fmc_off_mode = 0b1011 # Page 21
ndof = 0b1100 # Page 21
full_sensor_fusion_op_mode = 0x0C # Uses all sensors

unit_sel_addr = 0x3B
unit_sel = 0b010100 # sets angle units to rad instead of deg

class IMU_I2C:
    """
    A class to interface with a BNO055 IMU using pyb I2C protocol in order to obtain angular velocity and acceleration data
    
    """
    
    def __init__(self, I2Cobj, address): # Takes in I2C object configured in Controller mode
        """
        Initializes an IMU object using pyb I2C protocol
        
        Args:
            I2Cobj (pyb I2C object): pyb I2C object configured in controller mode
            address (int): operating address of IMU peripheral
        Returns:
            none
        """
    
        self.I2Cobj = I2Cobj
        self.address = address
        self.I2Cobj.mem_write(unit_sel, self.address, unit_sel_addr, timeout=5000, addr_size=8) # Sets 
        
    def changeOpMode(self, mode):  # Change operating mode
        """ 
        Change Operating mode of the IMU
        
        Args: 
            mode (int): byte to write to the IMU's operating mode byte
                
        Returns:
            none
        """
        self.I2Cobj.mem_write(config_op_mode, self.address, op_mode_addr, timeout=5000, addr_size=8)
        time.sleep(0.02)
        self.I2Cobj.mem_write(mode, self.address, op_mode_addr, timeout=5000, addr_size=8)
        time.sleep(0.02)
        
    def retrieveCalStatus(self): # Retrieve and parse calibration status byte
    # Must be in a fusion op mode
    
        """
        Retrieves and parses calibration status byte of the IMU
            
        Returns:
            tuple:
                A 4-tuple (sys, gyro, acc, mag) containing calibration states
                for the system, gyroscope, accelerometer, and magnetometer.
        """
        calStatus = self.I2Cobj.mem_read(1, self.address, calib_stat_addr, timeout=5000)[0]
        sys = (calStatus >> 6) & 0x03
        gyro = (calStatus >> 4) & 0x03
        acc = (calStatus >> 2) & 0x03
        mag = calStatus & 0x03
        return (sys, gyro, acc, mag)
        
    def retrieveCalCoefficients(self):  # Retrieve calibration coefficients from IMU as bianary data
    
        """
        Retrieves calibration coefficients from the IMU as bianary data
        
        Returns:
            bytearray:
                22-Byte bytearray containing calibration coefficients from the IMU
                
        """
        self.changeOpMode(config_op_mode) # must be in config op mode to read sensor data
    
        calData = bytearray(self.I2Cobj.mem_read(22, self.address, calib_coeff_addr, timeout=5000))
        self.changeOpMode(full_sensor_fusion_op_mode) # Changes back to a fusion op mode so calibration can take effect
        time.sleep_ms(20)
        return calData
    
    
    def writeCalCoefficients(self, calFileTxt): # Writes cal coefficients from pre-recorded bianary data
        # self.changeOpMode(config_op_mode) # must be in config op mode to write sensor data
        # time.sleep_ms(200)
        """
        Writes calibration coefficients to the IMU using previously recorded bianary data
        
        Args:
            calFileTxt (String): referencing a .txt file stored on the board that contains pre-recorded calibration coefficients
        Returns:
            none
        """
        with open(calFileTxt, "rb") as f: # calFileTxt is string of cal text file stored on the board
            calData = bytearray(f.read(22)) # Read text file and store into byte array
        self.I2Cobj.mem_write(calData, self.address, calib_coeff_addr, timeout=5000, addr_size=8)
        # time.sleep_ms(200)
        # self.changeOpMode(full_sensor_fusion_op_mode) # Changes back to a fusion op mode so calibration can take effect
        # time.sleep_ms(200)
    
    def readEulerAngles(self): # Reads Euler Angles from the IMU
    
        """
        Reads Euler Angles from the IMU
        
        Returns:
            tuple:
                A 3-tuple containing Euler angles in radians in the order heading, roll, pitch
                
        """
        get_eulers = self.I2Cobj.mem_read(6, self.address, eul_head_lsb)
        h, r, p = struct.unpack('<hhh', get_eulers)
        # Pg 35,  16 units per degree conversion
        return (h / 900, r / 900, p / 900)
    
    def readAngularVelocity(self): # Reads angular velocity from the IMU
    
        """
        Reads Anglular velocity from the IMU
        
        Returns:
            tuple:
                A 3-tuple containing anglular velocity in rad/s in the order heading, roll, pitch
        """
        get_ang_vel = self.I2Cobj.mem_read(6, self.address, gyr_data_x_lsb)
        x, y, z = struct.unpack('<hhh', get_ang_vel)
        return (x/900, y/900, z/900)
    
    def readLinearAcceleration(self): # Reads angular velocity from the IMU
    
        """
        Reads Linear acceleration data from the IMU
        
        Returns:
            tuple:
                A 3-tuple containing linear acceleration in m/s^2 in the order x, y, z
                
        """
        get_lin_acc = self.I2Cobj.mem_read(6, self.address, acc_data_x_lsb)
        x, y, z = struct.unpack('<hhh', get_lin_acc)
        return (x/100, y/100, z/100) # Divide by 100 to get m/s^2

