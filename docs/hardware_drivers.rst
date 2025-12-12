Hardware Drivers
================

Python classes to run the motors, encoders, IR sensor, and IMU


Motor Driver
-------------

.. automodule:: motor_driver
   :members:
   :undoc-members:
   :show-inheritance:


Encoder
-------

.. automodule:: Encoder
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: ticks_us, ticks_diff

IMU
---

.. automodule:: IMU_I2C
   :members: IMU_I2C
   :undoc-members:
   :show-inheritance:
   :exclude-members: eul_head_lsb, gyr_data_x_lsb, acc_data_x_lsb, op_mode_addr, calib_stat_addr, calib_coeff_addr, unit_sel_addr, unit_sel, config_op_mode, IMU_op_mode, compass_mode, m4g_mode, ndof_fmc_off_mode, ndof, full_sensor_fusion_op_mode


IR Sensor
----------

.. automodule:: ir_sensor
   :members:
   :undoc-members:
   :show-inheritance:

IR Sensor Array
---------------

.. automodule:: sensor_array
   :members:
   :undoc-members:
   :show-inheritance: