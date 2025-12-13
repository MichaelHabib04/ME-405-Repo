Control Loops Used
===================
This project utilizes Proportional-Integral control for adjusting motor speed, line following, and position tracking. All of these controllers use the same basic structure and are implemented as objects into the main program. These Class definitions are contained in the file controller.py.

In the left and right operations tasks, the motor controllers run to determine a needed PWM motor effort for each motor based on a setpoint in mm/s. If line following or position following is active, these controllers output a speed differential in mm/s, which is then used to adjust the setpoints for the left and right motor controllers.

Control Loop Diagrams
----------------------
Motor Controllers
~~~~~~~~~~~~~~~~~~~


Line Follow Controller
~~~~~~~~~~~~~~~~~~~~~~~


Position Follow Controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~


Tuning Approach
----------------
