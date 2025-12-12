.. ME 405 Final Project documentation master file, created by
   sphinx-quickstart on Wed Dec 10 20:14:16 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ME 405 Final Project documentation
================================

This is the home page for the mecha-09 ME 405 Final Project Documentation!

GitHub Repository Link: https://github.com/MichaelHabib04/ME-405-Repo/tree/main

Project Overview:
=================

The goal of this project is to navigate a differential drive robot around an "Obstacle Course," where the robot is required to reach five checkpoints and roughly follow a line. Micropython loaded onto a microcontroller is used to control the robot. Low-level hardware programs control the motors, motor encoders, and selected sensors used for navigation. Middle level programs implement control loops and certain action commands for the robot. The function of the robot is put together into a cooperative multitasking strucutre, where each task executes different actions for controlling the robot. The open-source modules cotask.py and taskshare.py are used for data communication between tasks and task scheduling and prioritizing respectively.

taskshare.py info link from ME405 Library:
https://spluttflob.github.io/ME405-Support/cotask_8py.html

cotask.py infor link from ME405 Library:
https://spluttflob.github.io/ME405-Support/task__share_8py.html

Game Board Overview
===================
.. image:: /_static/Game_Board.jpg
   :alt: Game board picture
   :width: 400px
   :align: center

The game board is a circuit that is 1x1.8 meters, with five required checkpoints that the robot must reach. The circular outline in the top left corner indicates where the robot begins the course. The game board also indicates areas where a wall is located, a structure with barriers in the lower left hand corner (the "parking garage"), and "bonus" areas where plastic cups are located. The robot is explicitly required to follow the line path until the diamond-shape before checkpoint 1, and the robot is required to interact with the wall in some manner. Challenging areas of the course include disruptions in the line (such as forks, dashes, or zig-zags), the "parking garage" area with no line to follow, and navigation around the wall back to the starting area of the course.

Navigational Approach
=====================
The course is navigated in two primary ways: Line following and position tracking. Line following is done using an IR sensor array to center the robot over the line. Position tracking is done using a state estimator to determine the robot's total distance traveled and global position on the game board. Both the line following and position tracking use a closed-loop proportional-integral controller to set a speed difference between wheels in order to alter the robot's heading angle.

The command class was created for navigation around the course, allowing the course to be broken into segments of line following and position tracking. A command object specifies the type of navigation, a setpoint speed, an end condition, and an end X and Y global coordinate. The commander task in the mutlitasking structure parses these commands and enables and disables the line follow or position tracking task for the conditions specified in the command objects.

We broke the course into XX segments:
1. Line follow from ssss

Etc.


Video of Course Navigation
==========================

(Embed YouTube video)



.. toctree::
   :maxdepth: 12
   :caption: Contents:


   hardware
   hardware_drivers
   action_drivers