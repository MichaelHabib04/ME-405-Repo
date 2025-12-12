Hardware Overview
=================
This project uses a Pololu Romi differential drive robot. The motors and motor encoders used are the ones that come with the Pololu chasis kit. Important specifications for the Romi are listed below:

Chassis Diameter:				163 mm
Track Width (Wheel Center to Wheel Center):	141 mm
Wheel Radius:					35 mm
Gear Ratio (Exact):				119.76:1
Encoder Resolution (at Motor):			12 counts/rev
Motor Voltage (Rated):				4.5 V

To interface with the Romi, we used a STM32L476RGT6 microcontroller embeded on a NUCLEO-L476RG board. This board was interfaced with using a Shoe of Brian board. More information about the Shoe of Brian board can be found on the ME405 Library: https://spluttflob.github.io/ME405-Support/shoe_info.html 

In addition to the base Romi chasis, we used an IR sensor array, inertial measurement unit (IMU), and snap-action bumper switches to sense the environment and provide feedback. A bluetooth module was also used to communicate with Romi wirelessly.

Fully Assembled Romi:
=====================

.. image:: /_static/Romi_side_1.jpg
   :alt: Fully Assembled Romi
   :width: 900px
   :align: center

This is Romi fully assembled as used for the final project

.. image:: /_static/Romi_side_2_schematic.drawio.png
   :alt: Labeled Romi assembly - top
   :width: 900px
   :align: center
This image shows the locations of the bump sensors, Bluetooth module, Nucleo board, and Shoe of Brian board on the full Romi assembly


.. image:: /_static/Romi_bottom_schematic.drawio.png
   :alt: Romi Bottom Schematic
   :width: 1000px
   :align: center

This image shows the locations of the IMU sensor and IR sensor arrays, which are located on the bottom of the Romi chassis.

IR Sensor Array:
================
.. image:: /_static/Pololu_IR_sensor.jpg
   :alt: Pololu IR sensor
   :width: 900px
   :align: center
The IR sensor array used was the Pololu QTR-HD-13A Reflectance Sensor Array: 13-channel, 4mm pitch, Analog POutput

IMU sensor:
============
.. image:: /_static/IMU_image.jpg
   :alt: IMU sensor image
   :width: 900px
   :align: center
The IMU sensor used is the adafruit BNO055 Absolute Orientation IMU

Bumper switches:
================
.. image:: /_static/Bump_sensor.jpg
   :alt: Pololu Bump sensor
   :width: 900px
   :align: center
To interact with the wall, the Pololu Romi bump sensor modules were used, one for the left side of Romi and one for the right side. The output pins for each were soldered together, since we did not care about which particular bump sensor was activated for our purposes.

Bluetooth Module:
=================
.. image:: /_static/Bluetooth_module.jpg
   :alt: HC-05 Bluetooth module
   :width: 500px
   :align: center
The HC-05 Bluetooth module was used to interact with Romi wirelessly. The module communicates with the STM board over a UART protocol.

Voltage Divider Circuit:
========================
.. image:: /_static/Voltage_divider_circuit.png
   :alt: HC-05 Bluetooth module
   :width: 1000px
   :align: center
In order to correct for battery drainage, a task was created to read the battery voltage and correct it to a setpoint. In order to accomplish this, a reading of current battery voltage was needed. We accomplished this by using a voltage divider circuit in our power connection from the Romi chasis to the Nucleo board. The schematic for this circuit is shown above; the schematic was provided by the course instructor (Charlie Refvem) on the ME405 Canvas page.

MCU Pin map:
============
.. image:: /_static/Pin_out_diagram.jpg
   :alt: HC-05 Bluetooth module
   :width: 700px
   :align: center
Our selected Pins for connecting our hardware to the MCU are shown in the table above. We opted to create a "common 3.3V connection" for all of our hardware that required 3.3V of power. This connection is three wires soldered together, with connections to the MCU 3.3V output, the IMU power input, and the IR sensor array power input.
