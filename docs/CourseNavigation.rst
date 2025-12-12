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

We broke the course into XX segments:
1. Line follow from ssss

Etc.


Video of Course Navigation
---------------------------
