Course Navigation
==================
Game Board Overview
--------------------
.. image:: /_static/Game_Board.jpg
   :alt: Game board picture
   :width: 1000px
   :align: center

The game board is a circuit that is 1x1.8 meters, with five required checkpoints that the robot must reach. The circular outline in the top left corner indicates where the robot begins the course. The game board also indicates areas where a wall is located, a structure with barriers in the lower left hand corner (the "parking garage"), and "bonus" areas where plastic cups are located. The robot is explicitly required to follow the line path until the diamond-shape before checkpoint 1, and the robot is required to interact with the wall in some manner. Challenging areas of the course include disruptions in the line (such as forks, dashes, or zig-zags), the "parking garage" area with no line to follow, and navigation around the wall back to the starting area of the course.

Navigational Approach
----------------------
The course is navigated in two primary ways: Line following and position tracking. Line following is done using an IR sensor array to center the robot over the line. Position tracking is done using a state estimator to determine the robot's total distance traveled and global position on the game board. Both the line following and position tracking use a closed-loop proportional-integral controller to set a speed difference between wheels in order to alter the robot's heading angle.

The command class was created for navigation around the course, allowing the course to be broken into segments of line following and position tracking. A command object specifies the type of navigation, a setpoint speed, an end condition, and an end X and Y global coordinate. The commander task in the mutlitasking structure parses these commands and enables and disables the line follow or position tracking task for the conditions specified in the command objects.

We broke the course into 13 segments:

.. list-table::
   :widths: 10 10 15 10 40
   :header-rows: 1

   * - Command
     - Mode
     - End Condition
     - Lin Speed
     - Description
   * - com_1
     - lin
     - 930
     - 100
     - Line follow from start to first fork
   * - com_2
     - fwd
     - 100
     - 100
     - Go past the diamond
   * - com_3
     - lin
     - 480
     - 100
     - Line follow around half circle
   * - com_4
     - lin
     - 250
     - 200
     - Quickly line follow through dashed lines
   * - com_5
     - lin
     - 1250
     - 150
     - Back to normal speed to go around track
   * - com_6
     - fwd
     - 310
     - 100
     - Cross the zig-zag
   * - com_7
     - lin
     - 300
     - 115
     - Line to parking garage entrance
   * - com_8
     - fwd
     - 580
     - 140
     - Go through parking garage
   * - com_9
     - tip
     - 1
     - 100
     - Turn 90 degrees to exit parking garage
   * - com_10
     - fwd
     - 70
     - 100
     - Go forward to CP5
   * - com_11
     - lin
     - 400
     - 150
     - Go forward until wall is hit
   * - com_12
     - fwd
     - -70
     - -100
     - Reverse after hitting wall
   * - com_13
     - tip
     - 1
     - 100
     - Turn right

In addition, after the bump sensor was activated, we attempted to have the robot turn in a half-circle to navigate around the wall, but we were unable to get it fully implemented in the time constraints for our project.

Reliability
------------
Our code consistiently and reliably got Romi to checkpoint 4 on the game board. A consitient issue was reliability in getting the heading of Romi correct when going into the parking garage segment of the course. In the parking garage, we have Romi drive forward in a straight line without line following enabled, since there is no line to follow in this course section. If Romi is not perfectly aligned while entering this segment, it will hit the barrier of the parking garage. This is what occurs in the first video trial below. We tried several methods to fix this issue, including adding a turn-in-place command after Romi reaches checkpoint 4 in order to correct the heading. However, the heading offset that needed to be corrected coming off of the line following was not very consistient; we attemtped to remedy this by having Romi drive through this line follow segment more slowly, which did help but did not completely fix the issue. We eventually abandoned the turn-in-place command before entering the parking garage since the angle offset we were attempting to correct for was within the range of noise we got from the IMU.

When Romi successfully navigated the parking garage, our code consistiently got it to checkpoint 5, to the wall, and backing up from the wall. However, we were not able to make it to checkpoint 6, largely because it was difficult to test the navigation around the wall when we kept on encountering the above issue of Romi not navigating the parking garage consistiently.


Videos of Course Navigation
---------------------------

Navigation to Checkpoint 4 During In-Class Demo:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. youtube:: 6ZmEpD3uC0o
    :width: 560
    :height: 315

Navigation to Wall Demo:
~~~~~~~~~~~~~~~~~~~~~~~~
.. youtube:: AqD9DfiowdE
    :width: 560
    :height: 315

Video Links
~~~~~~~~~~~~
https://www.youtube.com/watch?v=6ZmEpD3uC0o
https://www.youtube.com/watch?v=AqD9DfiowdE


