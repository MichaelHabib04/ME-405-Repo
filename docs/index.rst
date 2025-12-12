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

The goal of this project is to navigate a differential drive robot around an "Obstacle Course," where the robot is required to reach five checkpoints and roughly follow a line. Micropython loaded onto a microcontroller is used to control the robot. Low-level hardware programs control the motors, motor encoders, and selected sensors used for navigation. Middle level programs implement control loops and certain action commands for the robot. The function of the robot is put together into a cooperative multitasking strucutre, where each task executes different actions for controlling the robot. 

The linked GitHub Repository contains all code needed to replicate this project; the Final Term Project folder specifically contains our final versions of code. In addition, this documentation site provides an overview of the hardware used and software written for this project. We wrote all code needed for this project other than the modules used for inter-task data sharing and the task scheduler. Documentation for these modules from the ME405 Libray is linked below.

The open-source modules cotask.py and taskshare.py are used for data communication between tasks and task scheduling and prioritizing respectively.

taskshare.py info link from ME405 Library:
https://spluttflob.github.io/ME405-Support/cotask_8py.html

cotask.py infor link from ME405 Library:
https://spluttflob.github.io/ME405-Support/task__share_8py.html




.. toctree::
   :maxdepth: 12
   :caption: Contents:

   CourseNavigation
   hardware
   hardware_drivers
   action_drivers