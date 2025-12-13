\# ME 405 Term Project



This repository contains all code developed throughout the ME 405 course to operate a Pololu Romi differential drive robot. The project evolved through multiple lab deliverables, each adding new subsystems, controllers, and sensing capabilities. The final implementation integrates cooperative multitasking, closed-loop motor control, line following, IMU-based state estimation, and autonomous path execution.



\## Project Overview



Over the quarter, the robot gained the ability to:



\- Execute multiple concurrent tasks using cooperative multitasking  

\- Drive with closed-loop PI motor controllers  

\- Follow a line using a 7-channel IR sensor array  

\- Estimate global position using IMU and encoder–based state estimation  

\- Navigate an obstacle course autonomously using a command sequencing task  

\- Communicate with the PC over UART for debugging, graphing, and data collection  



The repository includes all intermediate development versions used during each weekly lab, as well as the final on-board and PC-side code.



\## Repository Structure



\### `Final Term Project/`



Contains the final versions of all code.



\### `Lab 0x0\*/`



Each of these folders contains the code used for that intermediate deliverable.  

This allows you to see the evolution of the project. Lab deliverables are detailed in the section below.



\### `on\_board/`



Contains all MicroPython files that run directly on the Pyboard, including:



\- `main.py` — the primary program that executes autonomous navigation  

\- Task modules (motor operations, IR sensor task, IMU task, commander task, etc.)  

\- Hardware setup code  

\- Intermediate test files used during development  



\*\*Note:\*\* Only a subset of these files need to be flashed to the Pyboard.  

The Read the Docs site (automodules section) lists every required module other than `main.py`, which must always be present.



\### `on\_pc/`



Contains Python scripts that run on the computer rather than on the robot. These scripts are used for:



\- UART communication with the UI task  

\- Step response graphing  

\- Data logging  

\- Visualization tools  



The contents of this folder evolved each week based on the required data collection or debugging tasks.



\## Lab Deliverables



The repository contains folders for each weekly lab assignment:



\- \*\*Lab 0x02\*\* — Cooperative multitasking foundation  

\- \*\*Lab 0x03\*\* — Motor control development and PI tuning  

\- \*\*Lab 0x04\*\* — Line following using the IR sensor array  

\- \*\*Lab 0x05\*\* — IMU integration and state estimation  



\## Additional Supporting Files



\- MATLAB scripts for determining state estimation matrices  

\- Step response results and motor characterization data  

\- Images and diagrams used in the documentation  



\## Documentation



Full project documentation, including hardware setup, task descriptions, state diagrams, command sequencing, and API references, is hosted on Read the Docs:



https://me-405-repo.readthedocs.io/en/latest/index.html



\## Final System Components



The final robot implementation includes:



\### Cooperative multitasking with:



\- Left and right motor operation tasks  

\- Line-following task  

\- Position controller task  

\- IMU observer/state estimator task  

\- Commander task for autonomous course navigation  

\- UART-based UI task  



\### Hardware configuration:



\- Pololu IR sensor array  

\- BNO055 IMU  

\- Dual motor drivers  

\- Quadrature encoders  

\- Bump sensors  

\- UART/Bluetooth interface  



\## Running the Robot



To run the system:



1\. Flash `main.py` and all documented modules inside `on\_board/` onto the Pyboard.  

2\. Use the `on\_pc/` scripts as needed for data collection, plotting, or UART interaction.  

3\. Power the robot and initiate pathing via the UI task.  



\## Contributors



\- Katherine Meezan  

\- Michael Habib  

\- Zachery Boyer  



ME 405 – Cal Poly Mechanical Engineering  

Instructor: Charles Refvem  

Fall 2025

&nbsp;



