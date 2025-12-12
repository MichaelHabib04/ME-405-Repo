Mutlitasking Implementation
============================
The code for our project runs using a priority-based cooperative multitasking structure. We used the open source cotask.py to create tasks and run them in a task scheduler. Each task references a generator function in our main.pyb file that is loaded onto the MCU. In general, each task is implemented as a finite state machine, although some of our tasks align with this structure more closely than others.

Inter-task communication
-------------------------
Information is communicated between tasks using Share and Queue objects from the open source taskshare.py. A Queue is made of a series of Shares. Shares are defined as a certain data type, and information of that data type can be 

List of shares
~~~~~~~~~~~~~~


Task Diagram
-------------

List of Tasks
--------------
Include priority, frequency, and shares

Task Descriptions
------------------

FSM and short blurb for each task

commander
~~~~~~~~~~



