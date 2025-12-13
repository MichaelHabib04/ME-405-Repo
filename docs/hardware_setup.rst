Hardware Setup
==============

Pin Connection Diagrams
------------------------

This section describes the physical wiring of the robot, including encoder pins,
motor driver pins, IMU communication lines, IR sensor analog channels, bump sensors,
and Bluetooth UART connections. Each pin is configured for the correct STM32 mode
(analog, input with pull-up, alternate function, encoder interface, or PWM output).

The Nucleo Board has two headers, labeled as CN7 and CN10. A full map of the locations of the utilized pins are shown below. The dynamic connection guide and schematic is included in the project GitHub Repository as an excel file.

CN7 Connections
~~~~~~~~~~~~~~~
.. image:: /_static/CN7_connections.png
   :alt: IMU sensor image
   :width: 170px
   :align: center


CN10 Connections
~~~~~~~~~~~~~~~~
.. image:: /_static/CN10_connections.png
   :alt: IMU sensor image
   :width: 170px
   :align: center

Software Initialization of Hardware and Controller Objects
-----------------------------------------------------------
To run our mutlitasking script succesfully, needed objects had to be initialized. These include objects of the hardware and action drivers we wrote, as well as pyb Pin, Timer, and other objects.

Bluetooth / UART Setup
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Bluetooth and UART Objects
   :widths: 20 25 55
   :header-rows: 1

   * - Name
     - Type
     - Purpose

   * - Pin.cpu.A2
     - Pin (ANALOG)
     - Deconfigured to analog to free default pin function for Bluetooth UART use.

   * - Pin.cpu.A3
     - Pin (ANALOG)
     - Deconfigured to analog to free default pin function for Bluetooth UART use.

   * - Pin.cpu.B6
     - Pin (ALT, AF7)
     - Configured as UART TX pin for Bluetooth module.

   * - Pin.cpu.B7
     - Pin (ALT, AF7)
     - Configured as UART RX pin for Bluetooth module.

   * - uart
     - UART(1)
     - UART interface for Bluetooth communication (115200 baud, 8-N-1).


Encoders and Timer Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Encoder Hardware and Objects
   :widths: 20 25 55
   :header-rows: 1

   * - Name
     - Type
     - Purpose

   * - PA8
     - Pin (OUT_PP)
     - Left encoder A signal (Timer1 Channel 1).

   * - PA9
     - Pin (OUT_PP)
     - Left encoder B signal (Timer1 Channel 2).

   * - timLeft
     - Timer(1)
     - Left wheel encoder timer (16-bit, prescaler=0, period=0xFFFF).

   * - ch1Left
     - Timer channel
     - Left encoder channel A configured in ENC_AB mode.

   * - ch2Left
     - Timer channel
     - Left encoder channel B configured in ENC_AB mode.

   * - left_encoder
     - Encoder
     - Encoder driver for left wheel (position and speed in counts).

   * - PB4
     - Pin (OUT_PP)
     - Right encoder A signal (Timer3 Channel 1).

   * - PB5
     - Pin (OUT_PP)
     - Right encoder B signal (Timer3 Channel 2).

   * - timRight
     - Timer(3)
     - Right wheel encoder timer (16-bit, prescaler=0, period=0xFFFF).

   * - ch1Right
     - Timer channel
     - Right encoder channel A configured in ENC_AB mode.

   * - ch2Right
     - Timer channel
     - Right encoder channel B configured in ENC_AB mode.

   * - right_encoder
     - Encoder
     - Encoder driver for right wheel (position and speed in counts).


Motors and Closed-Loop Controllers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Motor Drivers and Controllers
   :widths: 20 25 55
   :header-rows: 1

   * - Name
     - Type
     - Purpose

   * - mot_left
     - motor_driver
     - Left motor driver (direction + PWM using Timer17 at 60 kHz).

   * - mot_right
     - motor_driver
     - Right motor driver (direction + PWM using Timer16 at 60 kHz).

   * - cl_ctrl_mot_left
     - CLMotorController
     - Closed-loop controller for left motor (PI control, mm/s setpoint).

   * - cl_ctrl_mot_right
     - CLMotorController
     - Closed-loop controller for right motor (PI control, mm/s setpoint).


Battery Measurement
~~~~~~~~~~~~~~~~~~~

.. list-table:: Battery Sensor Objects
   :widths: 20 25 55
   :header-rows: 1

   * - Name
     - Type
     - Purpose

   * - PC2
     - Pin (ANALOG)
     - Analog input pin for battery voltage sensing.

   * - BAT_READ
     - ADC
     - ADC channel used to read battery voltage.


IR Sensors and Line Following
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: IR Sensor Channels and Controllers
   :widths: 20 25 55
   :header-rows: 1

   * - Name
     - Type
     - Purpose

   * - ir_ch1
     - IR_sensor
     - IR sensor at pin C3.

   * - ir_ch3
     - IR_sensor
     - IR sensor at pin A4.

   * - ir_ch5
     - IR_sensor
     - IR sensor at pin B0.

   * - ir_ch7
     - IR_sensor
     - IR sensor at pin C1.

   * - ir_ch9
     - IR_sensor
     - IR sensor at pin C0.

   * - ir_ch11
     - IR_sensor
     - IR sensor at pin C4.

   * - ir_ch13
     - IR_sensor
     - IR sensor at pin C5.

   * - channels
     - list[IR_sensor]
     - Odd-numbered IR sensors in the array.

   * - ir_sensor_array
     - sensor_array
     - IR sensor array (7 channels) used for line following.

   * - centroid_set_point
     - float
     - Target centroid location for line following (-1.5).

   * - ir_controller
     - IRController
     - Controller for IR-based line tracking.

   * - position_controller
     - PositionController
     - Higher-level position control loop.


IMU (BNO055) Configuration and Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: IMU Configuration and Objects
   :widths: 25 20 55
   :header-rows: 1

   * - Name
     - Type
     - Purpose

   * - op_mode_addr
     - int
     - BNO055 operating mode register (0x3D).

   * - calib_stat_addr
     - int
     - Calibration status register (0x35).

   * - calib_coeff_addr
     - int
     - Calibration coefficient base address (0x55).

   * - eul_head_lsb
     - int
     - Euler heading LSB address (0x1A).

   * - acc_data_x_lsb
     - int
     - Accelerometer X LSB address (0x08).

   * - gyr_data_x_lsb
     - int
     - Gyroscope X LSB address (0x14).

   * - config_op_mode
     - int
     - Configuration mode byte for BNO055.

   * - full_sensor_fusion_op_mode
     - int
     - Full sensor fusion mode value (0x0C).

   * - IMU_addr
     - int
     - BNO055 I2C device address (0x28).

   * - PB10
     - Pin (ALT, AF4)
     - I2C2 SCL pin for IMU.

   * - PB11
     - Pin (ALT, AF4)
     - I2C2 SDA pin for IMU.

   * - i2c
     - I2C(2)
     - I2C controller used for IMU communication.

   * - IMU
     - IMU_I2C
     - IMU interface providing orientation and motion data.


Bump Sensors
~~~~~~~~~~~~

.. list-table:: Bump Sensor Pins
   :widths: 20 25 55
   :header-rows: 1

   * - Name
     - Type
     - Purpose

   * - PB12
     - Pin (IN, PULL_UP)
     - Right bump sensor input.

   * - PB13
     - Pin (IN, PULL_UP)
     - Left bump sensor input.
