Mutlitasking Implementation
============================
The code for our project runs using a priority-based cooperative multitasking structure. We used the open source cotask.py to create tasks and run them in a task scheduler. Each task references a generator function in our main.pyb file that is loaded onto the MCU. In general, each task is implemented as a finite state machine, although some of our tasks align with this structure more closely than others.

Inter-task communication
-------------------------
Information is communicated between tasks using Share and Queue objects from the open source taskshare.py. A Queue is made of a series of Shares. Shares are defined as a certain data type, and information of that data type is stored in the share object and can be referenced in other tasks. Below is a tabulated version of all of the shares we used. In general, we used uint16 shares for true/false flags and data that would only count in positive whole numbers (such as encoder counts). For other shares where decimal values were needed or desired, float was used.

List of shares
~~~~~~~~~~~~~~
.. list-table:: Share Variables
   :widths: 20 10 10 60
   :header-rows: 1

   * - Variable
     - Type
     - Size
     - Description
   * - L_lin_spd
     - f
     - 32-bit float
     - Left motor linear speed setpoint (mm/s)
   * - L_voltage_share
     - f
     - 32-bit float
     - Left motor effective voltage (V)
   * - L_en_share
     - H
     - 16-bit unsigned
     - Left encoder count
   * - L_pos_share
     - f
     - 32-bit float
     - Left wheel position (encoder counts)
   * - L_vel_share
     - f
     - 32-bit float
     - Left wheel velocity (counts/s)
   * - L_time_share
     - H
     - 16-bit unsigned
     - Timestamp (µs)
   * - R_dir_share
     - H
     - 16-bit unsigned
     - Right motor direction
   * - R_lin_spd
     - f
     - 32-bit float
     - Right wheel linear speed setpoint (mm/s)
   * - R_voltage_share
     - f
     - 32-bit float
     - Right motor effective voltage (V)
   * - R_en_share
     - H
     - 16-bit unsigned
     - Right encoder count
   * - R_pos_share
     - f
     - 32-bit float
     - Right wheel position
   * - R_vel_share
     - f
     - 32-bit float
     - Right wheel velocity
   * - R_time_share
     - H
     - 16-bit unsigned
     - Timestamp (µs)
   * - run
     - H
     - 16-bit unsigned
     - Global run flag
   * - print_out
     - H
     - 16-bit unsigned
     - Debug print flag
   * - bat_share
     - f
     - 32-bit float
     - Battery voltage
   * - bat_flag
     - H
     - 16-bit unsigned
     - Low battery flag
   * - calib_black
     - H
     - 16-bit unsigned
     - Black calibration value
   * - calib_white
     - H
     - 16-bit unsigned
     - White calibration value
   * - line_follow
     - H
     - 16-bit unsigned
     - Line follower enable
   * - position_follow
     - H
     - 16-bit unsigned
     - Position follower enable
   * - wheel_diff
     - f
     - 32-bit float
     - Wheel speed difference
   * - yaw_angle_share
     - f
     - 32-bit float
     - IMU yaw angle
   * - yaw_rate_share
     - f
     - 32-bit float
     - IMU yaw rate
   * - dist_traveled_share
     - f
     - 32-bit float
     - Integrated forward distance
   * - IMU_time_share
     - H
     - 16-bit unsigned
     - IMU timestamp
   * - time_start_share
     - H
     - 16-bit unsigned
     - Motion segment start timestamp
   * - X_coords_share
     - f
     - 32-bit float
     - Current global X position
   * - Y_coords_share
     - f
     - 32-bit float
     - C


Task Diagram
-------------

List of Tasks
--------------
.. list-table:: Task List
   :widths: 15 20 10 10 45
   :header-rows: 1

   * - Task Name
     - Description
     - Priority
     - Period (ms)
     - Shares Used

   * - Left ops
     - left_ops()
     - 3
     - 20
     - L_lin_spd, L_en_share, L_pos_share, L_vel_share, L_time_share, wheel_diff, line_follow, L_voltage_share, position_follow

   * - Right ops
     - right_ops()
     - 4
     - 20
     - R_lin_spd, R_en_share, R_pos_share, R_vel_share, R_time_share, wheel_diff, line_follow, R_voltage_share, position_follow

   * - UI
     - run_UI()
     - 1
     - 100
     - L_lin_spd, R_lin_spd, run, print_out, time_start_share, start_pathing

   * - Battery
     - battery_read()
     - 0
     - 2000
     - bat_share, bat_flag

   * - IR sensor
     - IR_sensor()
     - 0
     - 50
     - calib_black, calib_white, line_follow, L_lin_spd, R_lin_spd, wheel_diff

   * - state estimator
     - IMU_OP()
     - 10
     - 50
     - L_pos_share, R_pos_share, L_voltage_share, R_voltage_share, L_vel_share, R_vel_share, yaw_angle_share, yaw_rate_share, dist_traveled_share, IMU_time_share, time_start_share, X_coords_share, Y_coords_share

   * - Commander
     - commander()
     - 0
     - 20
     - X_coords_share, Y_coords_share, start_pathing, position_follow, line_follow, X_target, Y_target, dist_from_target, dist_traveled_share, R_lin_spd, L_lin_spd

   * - Pos CTRL
     - PositionControl()
     - 0
     - 20
     - X_coords_share, Y_coords_share, position_follow, IMU_time_share, yaw_angle_share, wheel_diff, dist_from_target, X_target, Y_target

Task Descriptions
------------------

FSM and short blurb for each task

commander
~~~~~~~~~~

Task Generator Functions
-------------------------
.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:




