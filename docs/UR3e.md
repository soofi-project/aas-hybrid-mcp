# ==> picture [206 x 35] intentionally omitted <==

Source: UR3e.pdf


---

### Page 1

Original instructions (en)
PolyScope 5
User Manual
UR3e

### Page 2

UR3e
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 3

The information contained herein is the property of Universal Robots A/S and shall not be reproduced in
whole or in part without prior written approval of Universal Robots A/S. The information herein is subject to
change without notice and should not be construed as a commitment by Universal Robots A/S. This
document is periodically reviewed and revised.
Universal Robots A/S assumes no responsibility for any errors or omissions in this document.
Copyright © 2009–2024 by Universal Robots A/S.
The Universal Robots logo is a registered trademark of Universal Robots A/S.
User Manual
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 4

UR3e
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 5

Contents
1. Liability and Intended Use
11
1.1. Limitation of Liability
11
1.2. Intended Use
11
2. Your Robot
13
2.1. Technical Specifications UR3e
17
2.2. Teach Pendant with 3-Position Enabling Device
18
2.2.1. 3PE Teach Pendant Button Functions
20
2.2.2. Using the 3PE Buttons
21
2.3. PolyScope Overview
24
2.3.1. Icons/Tabs On PolyScope
25
3. Safety
27
3.1. General
27
3.2. Safety Message Types
28
3.3. General Warnings and Cautions
29
3.4. Integration and Responsibility
31
3.5. Stop Categories
31
4. Lifting and Handling
32
4.1. Control Box and Teach Pendant
32
4.2. Robot Arm
32
5. Assembly
33
5.1. Workspace and Operating Space
34
5.2. Dimensioning the Stand
35
5.3. Mounting Description
37
5.3.1. Singularity
37
5.3.2. Fixed and Movable Installation
39
5.4. Securing the Robot Arm
40
5.5. Control Box Clearance
42
5.6. Robot Connections: Base Flange Cable
43
5.7. Robot Connections: Robot Cable
44
5.8. Mains Connections
45
6. First Boot
47
6.1. Starting your robot
47
6.2. Inserting the Serial Number
48
6.3. Initializing the Robot Arm
49
6.4. Turning the Control Box On/Off
50
User Manual
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 6

6.5. Powering Down the Robot
51
6.6. Freedrive
52
6.6.1. Freedrive Panel
54
6.7. Mounting
57
6.8. Power Down The Robot
58
7. Installation
59
7.1. Electrical Warnings and Cautions
59
7.2. Control Box Connection Ports
61
7.3. Ethernet
62
7.4. 3PE Teach Pendant Installation
63
7.4.1. Hardware Installation
63
7.4.2. New Software Installation
65
7.5. Controller I/O
67
7.5.1. I/O Interface Control
70
7.5.2. Using the I/O Tab
71
7.6. Safety I/O
73
7.6.1. I/O Signals
78
7.6.2. I/O Setup
81
7.7. Three Position Enabling Device
84
7.8. General Purpose Analog I/O
85
7.8.1. Analog Input: Communication Interface
86
7.9. General Purpose Digital I/O
87
7.9.1. Digital Output
88
7.10. Remote ON/OFF control
89
7.11. End Effector Integration
90
7.11.1. Tool I/O
91
7.11.2. Maximum Payload
92
7.11.3. Securing Tool
94
7.11.4. Set Payload
95
7.11.5. Tool I/O Installation Specifications
100
7.11.6. Tool Power Supply
101
7.11.7. Tool Digital Outputs
102
7.11.8. Tool Digital Inputs
103
7.11.9. Tool Analogue Inputs
103
7.11.10. Tool Communication I/O
104
8. First Time Use
105
8.1. Quick System Start-up
105
8.2. The First Program
106
8.2.1. Run Tab
108
8.2.2. Move Robot into Position
112
UR3e
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 7

8.2.3. Using the Program Tab
113
8.2.4. Program Tree Toolbar
116
8.2.5. Using Selected Program Nodes
117
8.2.6. Using Basic Program Nodes
118
8.2.7. Basic Program Nodes: Move
118
8.2.8. Basic Program Nodes: Waypoints
121
8.2.9. Using the Move Tab
123
8.2.10. Pose Editor
125
8.3. Safety-related Functions and Interfaces
128
8.3.1. Configurable Safety Functions
129
8.3.2. Safety Functions
130
8.3.3. Safety Parameter Set
132
8.4. Software Safety Configuration
134
8.4.1. Setting a Software Safety Password
136
8.4.2. Changing the Software Safety Configuration
137
8.4.3. Applying a New Software Safety Configuration
138
8.4.4. Safety Configuration without Teach Pendant
140
8.4.5. Software Safety Modes
141
8.4.6. Software Safety Limits
141
8.4.7. Safe Home Position
146
8.5. Software Safety Restrictions
148
8.5.1. Tool Direction Restriction
154
8.5.2. Tool Position Restriction
156
9. Cybersecurity Threat Assessment
160
9.1. General Cybersecurity
160
9.2. Cybersecurity Requirements
160
9.3. Cybersecurity Hardening Guidelines
162
9.4. Passwords
163
9.5. Password Settings
163
9.6. Administrator Password
164
9.7. Operational Password
165
10. Communication Networks
166
11. Fieldbus
167
11.1. MODBUS
168
11.2. EtherNet/IP
172
11.3. PROFINET
172
11.4. PROFIsafe
173
11.5. UR Connect
176
12. Emergency Events
178
12.1. Emergency Stop
178
User Manual
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 8

12.2. Movement Without Drive Power
179
12.3. Modes
180
12.3.1. Recovery Mode
182
12.3.2. Backdrive
182
13. Transportation
187
13.1. Teach Pendant Storage
188
14. Maintenance and Repair
189
14.1. Testing Stopping Performance
189
14.2. Robot Arm Cleaning and Inspection
190
14.3. Log Tab
195
14.4. Program and Installation Manager
198
14.5. Accessing Robot Data
200
15. Disposal and Environment
202
16. Risk Assessment
204
16.1. Pinch Hazard
207
16.2. Stopping Time and Stopping Distance
208
16.3. Commissioning
213
17. Declarations and Certificates (original EN)
214
18. Declarations and Certificates
216
19. Certifications
218
20. Certificates
220
21. Safety Functions Table
226
21.1. Table 1a
233
21.2. Table 2
234
UR3e
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 9

User Manual
10
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 10

1. Liability and Intended Use
1.1. Limitation of Liability
Description
Any information provided in this manual must not be construed as a warranty, by UR,
that the industrial robot will not cause injury or damage, even if the industrial robot
complies with all safety instructions and information for use.
1.2. Intended Use
Description
READ MANUAL
Failure to use the robot in accordance with the intended use can result
in hazardous situations.
•   Read and follow the recommendations for intended use and the
specifications provided in the User Manual.
Universal Robots robots are intended for industrial use, to handle tools/end effectors and
fixtures, or to process or transfer components or products. For details about the
conditions under which the robot should operate.
All UR robots are equipped with safety functions, which are purposely designed to enable
collaborative applications, where the robot application operates together with a human.
The safety function settings must be set to the appropriate values as determined by the
robot application risk assessment.
Collaborative applications are only intended for non-hazardous applications, where the
complete application, including tool/end effector, work piece, obstacles and other
machines, is low risk according to the risk assessment of the specific application.
UR3e
11
User Manual
1. Liability and Intended Use
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 11

WARNING
Using UR robots or UR products outside of the intended uses can result in
injuries, death and/or property damage. Do not use the UR robot or products for
any of the below unintended uses and applications:
•   Medical use, i.e. uses relating to disease, injury or disability in humans
including the following purposes:
•   Rehabilitation
•   Assessment
•   Compensation or alleviation
•   Diagnostic
•   Treatment
•   Surgical
•   Healthcare
•   Prosthetics and other aids for the physically impaired
•   Any use in proximity to patient/s
•   Handling, lifting, or transporting people
•   Any application requiring compliance with specific hygienic and/or
sanitation standards, such as proximity or direct contact with food,
beverage, pharmaceutical, and /or cosmetic products.
•   UR joint grease can be released into the air (vapor), or drip.
•   Any use, or any application, deviating from the intended use,
specifications, and certifications of UR robots or UR products.
•   Misuse is prohibited as the result could be death, personal injury, and /or
property damage
UNIVERSAL ROBOTS EXPRESSLY DISCLAIMS ANY EXPRESS OR IMPLIED
WARRANTY OF FITNESS FOR ANY PARTICULAR USE.
WARNING
Do not modify the robot. Do not modify or alter e-Series end caps. A modification
can create unforeseen hazards. All authorized disassembling and reassembling
shall be done at a UR service center, or can be done according to the newest
version of all relevant service manuals by skilled persons.
WARNING
Failure to consider the added risks due to the reach, payloads, operating torques
and speeds associated with robot application, can result in injury or death.
•   Your application risk assessment shall include the risks associated with
the application's reach, motion, payload and speed of the robot, end
effector and workpiece.
User Manual
12
UR3e
1. Liability and Intended Use
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 12

2. Your Robot
Introduction
Congratulations on the purchase of your new Universal Robots robot, which consists of
the robot arm (manipulator), Control Box and the Teach Pendant.
Originally designed to mimic the range of motion of a human arm, the robot arm is
composed of aluminium tubes, articulated by six joints, allowing for a high range of
flexibility in your automation installation.
The Universal Robots patented programming interface, PolyScope, allows you to
create, load and run your automation applications.
In the boxes
•   Robot arm
•   Control Box
•   Teach Pendant or a 3PE Teach Pendant
•   Mounting bracket for the Control Box
•   Mounting bracket for the 3PE Teach Pendant
•   Key for opening the Control Box
•   Cable for connecting the robot arm and the Control Box (multiple options available
depending on robot size)
•   Mains cable or power cable compatible with your region
•   Round sling or lifting sling (depending on robot size)
•   Tool cable adapter (depending on robot version)
•   This manual
UR3e
13
User Manual
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 13

About the
robot arm
The Joints, Base and Tool Flange are the main components of the robot arm. The controller
coordinates joint motion to move the robot arm.
Attaching an end effector (tool) to the Tool Flange at the end of the robot arm, allows the robot
to manipulate a workpiece. Some tools have a specific purpose beyond manipulating a part,
for example, QC inspection, applying adhesives and welding.
1.1:   The main components of the robot arm.
•   Base: where the robot arm is mounted.
•   Shoulder and Elbow: make larger movements.
•   Wrist 1 and Wrist 2: make finer movements.
•   Wrist 3: where the tool is attached to the Tool Flange.
The robot is partly completed machinery, as such a Declaration of Incorporation is provided. A
risk assessment is required for each robot application.
About the
manual
This manual contains safety information, guidelines for safe use, and instructions to mount
the robot arm, Control Box and Teach Pendant. You can also find instructions for how to
begin to install and how to start programming the robot.
Read and adhere to the intended uses. Perform a risk assessment. Install and use in
accordance with the electrical and mechanical specifications provided in this user manual.
Risk assessment requires an understanding of the hazards, risks and risk reduction
measures for the robot application. Robot integration can require a basic level of mechanical
and electrical training.
User Manual
14
UR3e
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 14

Content
disclaimer
Universal Robots A/S continues to improve the reliability and performance of its products,
and as such reserves the right to upgrade products, and product documentation, without
prior warning. Universal Robots A/S takes every care to ensure the content of the User
Manual/s is precise and correct, but takes no responsibility for any errors or missing
information.
This manual does not contain warranty information.
myUR
The myUR portal allows you to register all your robots, keep track of service cases and
answer general support questions.
Sign into  myur.universal-robots.com  to access the portal.
In the myUR portal, your cases are handled either by your preferred distributor, or escalated
to Universal Robots Customer Service teams.
You can also subscribe to robot monitoring and manage additional user accounts in your
company.
Support
The support site  www.universal-robots.com/support  contains other language versions of this
manual
UR+
The online showroom UR+ www.universal-robots.com/plus  provides cutting-edge products to
customize your UR robot application. You can find everything you need in one place — from
tools and accessories to software.
UR+ products connect to and work with UR robots to ensure simple set-up and an overall
smooth user experience. All UR+ products are tested by UR.
You can also access the UR+ Partner Program via our software platform  plus.universal-
robots.com  to design more user-friendly products for UR robots.
UR forums
The UR Forum  forum.universal-robots.com  allows robot enthusiasts of all skill levels to
connect to UR and each other, to ask questions and to exchange information. While the UR
Forum was created by UR+ and our admins are UR employees, the majority of the content is
created by you, the UR Forum user.
Academy
The UR Academy site  academy.universal-robots.com  offers a variety of training
opportunities.
Developer
suite
The UR Developer Suite  universal-robots.com/products/ur-developer-suite  is a collection
of all the tools needed to build an entire solution, including developing URCaps, adapting
end-effectors, and integrating hardware.
UR3e
15
User Manual
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 15

Online
manuals
Manuals, guides and handbooks can be read online. We have gathered a large number of
documents at  https://www.universal-robots.com/manuals
•   PolyScope Software Handbook with descriptions and instructions for the software
•   The Service Handbook with instructions for troubleshooting, maintenance and repair
•   The Script Directory with scripting for in depth programming
User Manual
16
UR3e
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 16

2.1. Technical Specifications UR3e
Robot type
UR3e
Maximum payload
3 kg / 6.6 lb
Reach
500 mm / 19.7 in
Degrees of freedom
6 rotating joints
Programming
PolyScope graphical user interface on 12" touchscreen
Power consumption (average)
300 W
Max average power consumption
Approx. 150 W using a typical program
Ambient temperature range
0-50 °C. At ambient temperatures above 35°C, the robot
may operate at reduced speed and performance.
Safety functions
17 sophisticated safety functions. PLd Category 3 in
accordance with: EN ISO 13849-1.
IP classification
IP54
Cleanroom classification
Robot Arm: ISO Class 5, Control Box: ISO Class 6
Noise
Robot Arm: Less than 65dB(A)
Control Box: Less than 50dB(A)
Tool I/O ports
2 digital in, 2 digital out, 2 analog in
Tool I/O power supply & voltage
12 V/24 V 600 mA
Force Torque sensor accuracy
3.5 N
Speed
All wrist joints: Max 360 °/s.
Other joints: Max 180 °/s .
Tool: Approx. 1 m/s / Approx. 39.4 in/s.
Pose repeatability
± 0.03 mm / ± 0.0011 in (1.1 mils)per ISO 9283
Joint ranges
Unlimited rotation of tool flange, ± 360 ° for all other joints
Footprint
Ø128 mm / 5.0 in
Materials
Aluminium, PC/ASA plastic
Robot weight
11.1 kg / 24.5 lb
System update frequency
500 Hz
Control Box size (W × H × D)
460 mm × 449 mm × 254 mm / 18.2 in × 17.6 in × 10 in
Control Box I/O ports
16 digital in, 16 digital out, 2 analog in, 2 analog out
Control Box I/O power supply
24 V 2 A in Control Box
Communication
MODBUS TCP & Ethernet/IP adapter, PROFINET, USB
2.0, USB 3.0
Tool Communication
RS
Control Box power source
100-240 VAC, 47-440 Hz
Short-Circuit Current Rating (SCCR)
200A
TP cable: Teach Pendant to Control Box
4.5 m / 177 in
Robot Cable: Robot Arm to Control Box
(options)
Standard (PVC) 6 m/236 in x 13.4 mm
Standard (PVC) 12 m/472.4 in x 13.4 mm
Hiflex (PUR) 6 m/236 in x 12.1 mm
Hiflex (PUR) 12 m/472.4 in x 12.1 mm
UR3e
17
User Manual
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 17

2.2. Teach Pendant with 3-Position Enabling Device
Description
Depending on the robot generation, your Teach Pendant can be with or without a 3-
Position Enabling device (3PE).
The enabling buttons are on the underside of the Teach Pendant, as illustrated below.
You can use either button, according to your preference. If the Teach Pendant is
disconnected, an external 3PE device must be connected and configured. The 3PE TP
functionality extends to the PolyScope interface, where there are additional functions in
the Header.
NOTICE
If you have bought a UR20 or a UR30 robot.
•   A Teach Pendant without the 3PE will not work with the UR20
and UR30. Only UR20 and UR30 robots have the built-in 3PE
called a 3-Position Enabling Teach Pendant (3PE TP).
•   The 3PE Teach Pendant is not included with the purchase of the
OEM Control Box, so enabling device functionality is not
provided. Using a UR20, or a UR30, requires an external
enabling device or a 3PE Teach Pendant when programming, or
teaching, within the reach of the robot application. See ISO
10218-2.
Overview of
TP
1.   Power button
2.   Emergency Stop button
3.   USB port (comes with a dust cover)
4.   3PE buttons
User Manual
18
UR3e
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 18

Freedrive
A Freedrive robot symbol is located under each 3PE button, as illustrated below.
UR3e
19
User Manual
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 19

2.2.1. 3PE Teach Pendant Button Functions
Description
NOTICE
The 3PE buttons are only active in Manual mode. In Automatic mode,
robot movement does not require 3PE button action.
The table below describes the functions of the 3PE buttons.
Position
Description
Action
1
Release
There is no pressure on
the 3PE button. It is not
pressed.
Robot movement is stopped in Manual
mode. Power is not removed from the
robot arm and the brakes remain
released.
2
Light-
press
(Grip
lightly)
There is some pressure
on the 3PE button. It is
pressed to a middle
point.
Allows your program to play when the
robot is in Manual mode.
3
Tight-
press
(Grip
tightly)
There is full pressure on
the 3PE button. It is
pressed all the way
down.
Robot movement is stopped in Manual
mode. Robot is in 3PE Stop.
1
Button release
2
Button press
User Manual
20
UR3e
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 20

2.2.2. Using the 3PE Buttons
Using the
3PE
To play a program
1.   On PolyScope, ensure the robot is set to Manual mode, or switch to Manual mode.
2.   Maintain a light-press on the 3PE button.
3.   On PolyScope, tap Play to run the program.
The program runs if the robot arm is in the first position of the program.
If the robot is not in the first position of the program, the Move Robot into Position
screen appears.
To stop a program
1.   Release the 3PE button or, on PolyScope, tap Stop.
To pause a program
1.   Release the 3PE button, or, in PolyScope, tap Pause.
To continue the program execution, keep the 3PE button light pressed and tap
Resume in PolyScope.
Freedrive with 3PE Buttons
Description
Freedrive allows the robot arm to be manually pulled into desired positions and/or
poses.
To use the
3PE button to
freedrive the
robot arm
1.   Rapidly light-press, release, light-press again and keep holding the 3PE button in
this position.
Now you can pull the robot arm into a desired position, while the light-press is
maintained.
Using Move Robot into Position
Description
Move Robot into Position allows the robot arm to move to that start position, after you
complete a program. The robot arm must be in the start position before you can run the
program.
UR3e
21
User Manual
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 21

Move into
position
To use the 3PE button to move the robot arm into position:
1.   When your program is complete, press Play.
2.   Select Play from beginning.
On PolyScope, the Move Robot into Position screen appears displaying robot arm
movement.
3.   Light-press and hold the 3PE button.
4.   Now, on PolyScope, press and hold Automove for the robot arm to move to the start
position.
The Play Program screen appears.
5.   Maintain a light-press on the 3PE button to run your program.
Release the 3PE button to stop your program.
User Manual
22
UR3e
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 22

UR3e
23
User Manual
2. Your Robot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 23

2.3. PolyScope Overview
Description
PolyScope is the Graphical User Interface (GUI) on the Teach Pendant that operates
the robot arm via a touch screen. You create, load and execute programs for the robot in
PolyScope. The PolyScope interface is divided as shown in the following illustration:
•   A: Header with icons/tabs that make interactive screens available to you.
•   B: Footer with buttons that control your loaded program/s.
•   C: Screen with fields and options to manage and monitor robot actions.
Using the
Touch
Screen
The touch sensitivity is designed to avoid false selections on PolyScope, and to prevent
unexpected motion of the robot.
The Teach Pendant touch screen is optimized for use in industrial environments. Unlike
consumer electronics, Teach Pendant touch screen sensitivity is, by design, more resistant to
environmental factors such as:
•   water droplets and/or machine coolant droplets
•   radio wave emissions
•   other conducted noise from the operating environment.
For best results, use the tip of your finger to make a selection on the screen.
In this manual, this is referred to as a "tap".
A commercially available stylus may be used to make selections on the screen if desired.
User Manual
24
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 24

2.3.1. Icons/Tabs On PolyScope
Description
The following section lists and defines the icons/tabs and buttons in the PolyScope
interface.
Header Icons /
Functions
Run is a simple means of operating the robot using pre-written programs.
Program creates and/or modifies robot programs.
Installation configures robot arm settings and external equipment e.g.
mounting and safety.
Move controls and/or regulates robot movement.
I/O monitors and sets live Input/Output signals to and from robot control box.
Log indicates robot health as well as any warning or error messages.
Program and Installation Manager selects
and displays active program and installation. The Program and Installation Manager
includes: File Path, New, Open and Save.
New... creates a new Program or Installation.
Open... opens a previously created and saved Program or Installation.
Save... saves a Program, Installation or both at the same time.
Operational
modes
Automatic indicates the operational mode of the robot is set to Automatic. Tap
it to switch to the Manual operational mode.
Manual indicates the operational mode of the robot is set to Manual. Tap it to
switch to the Automatic operational mode.
Remote
Control
The Local mode and Remote mode icons only become accessible if you enable Remote
Control.
UR3e
25
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 25

Local indicates the robot can be controlled locally. Tap it to switch to Remote control.
Remote indicates the robot can be controlled from a remote location. Tap it to switch
to Local control.
Safety Checksum displays the active safety configuration.
Hamburger Menu accesses PolyScope Help, About and Settings.
Footer Icons /
Functions
Initialize manages robot state. When RED, press it to make the robot operational.
Speed Slider shows in real time the relative speed at which the
robot arm moves, taking safety settings into account.
Simulation button toggles a program execution
between Simulation Mode and the Real Robot. When running in Simulation Mode, the
Robot Arm does not move. Therefore, the robot cannot damage itself or nearby equipment
in a collision. If you are unsure what the Robot Arm will do, use Simulation Mode to test
programs.
Play starts current loaded robot Program.
Step allows a Program to be run single-stepped.
Stop halts current loaded robot Program.
High Speed
Manual
Mode
High Speed Manual Mode is a hold-to-run function, only available in Manual mode when a
Three-Position Enabling Device is configured.
High Speed Manual Modeallows both tool speed and elbow speed to
temporarily exceed 250mm/s.
User Manual
26
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 26

3. Safety
Description
Review the content here to understand the key safety guidelines, including important
safety messages and your responsibilities when working with the robot. Note that
system design and installation are not covered here.
3.1. General
Description
Read the general safety information and the instructions and guidance pertaining to the
risk assessment and intended use provided. Give particular attention to text
accompanied by warning symbols. Subsequent sections describe and define safety-
related functions particularly relevant for collaborative applications.
Read and understand the specific engineering data relevant to mounting and installation,
in order to understand the integration of UR robots before the robot is powered on for the
first time.
It is essential to observe and follow all assembly instructions in the following sections of
this manual.
NOTICE
Universal Robots disclaims any and all liability if the robot (arm Control
Box with or without Teach Pendant) is damaged, changed or modified
in any way. Universal Robots cannot be held responsible for any
damages caused to the robot or any other equipment due to
programming errors, unauthorized access to the UR robot and its
contents, or malfunctioning of the robot.
UR3e
27
User Manual
3. Safety
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 27

3.2. Safety Message Types
Description
Safety messages are used to emphasize important information. Read all the messages
to help ensure safety and to prevent injury to personnel and product damage. The safety
message types are defined below.
WARNING
Indicates a hazardous situation that, if not avoided, can result in death
or serious injury.
WARNING: ELECTRICITY
Indicates a hazardous electrical situation that, if not avoided, can result
in death or serious injury.
WARNING: HOT SURFACE
Indicates a hazardous hot surface where injury can result from contact
and non-contact proximity.
CAUTION
Indicates a hazardous situation that, if not avoided, can result in injury.
GROUND
Indicates grounding.
PROTECTIVE GROUND
Indicates protective grounding.
NOTICE
Indicates the risk of damage to equipment and/or information to be
noted.
READ MANUAL
Indicates more detailed information that should be consulted in the
manual.
User Manual
28
UR3e
3. Safety
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 28

3.3. General Warnings and Cautions
Description
The following warnings messages can be repeated, explained or detailed in subsequent
sections.
WARNING
Failure to adhere to the general safety practices, listed below, can result in
injury or death.
•   Verify the robot arm and tool/end effector are properly and securely
bolted in place.
•   Verify the robot application has ample space to operate freely.
•   Verify the personnel are protected during the lifetime of the robot
application including transport, installation, commissioning,
programming/ teaching, operation and use, dismantling and
disposing.
•   Verify robot safety configuration parameters are set to protect
personnel, including those who can be within reach of the robot
application.
•   Avoid using the robot if it is damaged.
•   Avoid wearing loose clothing or jewelry when working with the robot.
Tie back long hair.
•   Avoid placing any fingers behind the internal cover of the Control Box.
•   Inform users of any hazardous situations and the protection that is
provided, explain any limitations of the protection and the residual
risks.
•   Inform users of the location of the emergency stop button(s) and how
to activate the emergency stop in case of an emergency or an
abnormal situation.
•   Warn people to keep outside the reach of the robot, including when
the robot application is about to start-up.
•   Be aware of robot orientation to understand the direction of movement
when using the Teach Pendant.
•   Adhere to the requirements and guidance in ISO 10218-2.
WARNING
Handling tools/end effectors with sharp edges and/or pinch points can result in
injury.
•   Make sure tools/end effectors have no sharp edges or pinch points.
•   Protective gloves and/or protective eyeglasses could be required.
UR3e
29
User Manual
3. Safety
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 29

WARNING: HOT SURFACE
Prolonged contact with the heat generated by the robot arm and the Control Box,
during operation, can lead to discomfort resulting in injury.
•   Do not handle or touch the robot while in operation or immediately after
operation.
•   Check the temperature on the log screen before handling or touching the
robot.
•   Allow the robot to cool down by powering it off and waiting one hour.
CAUTION
Failure to perform a risk assessment prior to integration and operation can
increase risk of injury.
•   Perform a risk assessment and reduce risks prior to operation.
•   If determined by the risk assessment, do not enter the range of the robot
movement or touch the robot application during operation. Install
safeguarding.
•   Read the risk assessment information.
CAUTION
Using the robot with untested external machinery, or in an untested application,
can increase the risk of injury to personnel.
•   Test all functions and the robot program separately.
•   Read the commissioning information.
NOTICE
Very strong magnetic fields can damage the robot.
•   Do not expose the robot to permanent magnetic fields.
READ MANUAL
Verify all mechanical and electrical equipment is installed according to relevant
specifications and warnings.
User Manual
30
UR3e
3. Safety
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 30

3.4. Integration and Responsibility
Description
The information in this manual does not cover designing, installing, integrating and
operating a robot application, nor does it cover all peripheral equipment that can
influence the safety of the robot application. The robot application must be designed and
installed in accordance with the safety requirements set forth in the relevant standards
and regulations of the country where the robot is installed.
The person/s integrating the UR robot are responsible for ensuring that the applicable
regulations in the country concerned are observed and that any risks in the robot
application are adequately reduced. This includes, but is not limited to:
•   Performing a risk assessment for the complete robot system
•   Interfacing other machines and additional safeguarding if required by the risk
assessment
•   Setting the correct safety settings in the software
•   Ensuring safety measures are not modified
•   Validating the robot application is designed, and installed and integrated
•   Specifying instructions for use
•   Marking the robot installation with relevant signs and contact information of the
integrator
•   Retaining all documentation; including the application risk assessment, this
manual and additional relevant documentation.
3.5. Stop Categories
Description
Depending on the circumstances, the robot can initiate three types of stop categories
defined according to IEC 60204-1. These categories are defined in the following table.
Stop
Category
Description
0
Stop the robot by immediate removal of power.
1
Stop the robot in an orderly, controlled manner. Power is removed once
the robot is stopped.
2
*Stop the robot with power available to the drives, while maintaining the
trajectory. Drive power is maintained after the robot is stopped.
*Universal Robots robots’ Category 2 stops are further described as SS1 or as SS2 type
stops according to IEC 61800-5-2.
UR3e
31
User Manual
3. Safety
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 31

4. Lifting and Handling
Description
The robot arms come in different sizes and weights, so it is important to use the
appropriate lifting and handling techniques for each model. Here you can find
information on how to safely lift and handle the robot.
4.1. Control Box and Teach Pendant
Description
The Control Box and the Teach Pendant can each be carried by one person.
While in use, all cables are to be coiled and held to prevent tripping hazards.
4.2. Robot Arm
Description
The robot arm, depending upon weight, can be carried by one or two people unless the
sling is provided. If the sling is provided, equipment for lifting and transport is required.
User Manual
32
UR3e
4. Lifting and Handling
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 32

5. Assembly
Description
Install and power on the robot arm and Control Box to start using PolyScope.
Assemble the
robot
You have to assemble the robot arm, Control Box and Teach Pendant to be able to
continue.
1.   Unpack the robot arm and the Control Box.
2.   Mount the robot arm on a sturdy, vibration-free surface.
Verify the surface can withstand at least 10 times the full torque of the base joint and
at least 5 times the weight of the robot arm.
3.   Place the Control Box on its Foot.
4.   Connect the robot cable to the robot arm and the Control Box.
5.   Plug in the mains, or main power cable, of the Control Box.
WARNING
Failure to secure the robot arm to a sturdy surface can lead to injury
caused by the robot falling.
•   Ensure the robot arm is secured to a sturdy surface
UR3e
33
User Manual
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 33

5.1. Workspace and Operating Space
Description
The workspace is the range of the fully extended robot arm, horizontally and vertically.
The operating space is the location where the robot is expected to function.
NOTICE
Disregard for the robot workspace and operating space can result in
the damage to property.
•   Consider the information below when choosing the operating
space for the robot.
NOTICE
Moving the tool close to the cylindrical volume can cause the joints to
move too fast, leading to loss of functionality and damage to property.
•   Do not move the tool close to the cylindrical volume, even when
the tool is moving slowly.
Workspace
The cylindrical volume is both directly above and directly below the robot base. The robot
extends 500 mm from the base joint.
Front
Tilted
User Manual
34
UR3e
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 34

5.2. Dimensioning the Stand
Description
The structure (stand) on which the robot arm is mounted is a crucial part of the robot
installation. The stand must be sturdy and free of any vibrations from external sources.
Each robot joint produces a torque that moves and stops the robot arm. During normal
uninterrupted operation and during stopping motion, the joint torques are transferred to the
robot stand as:
•   M z : Torque around the base z axis.
•   F z : Forces along base z axis.
•   M xy : Tilting torque in any direction of the base xy plane.
•   F xy : Force in any direction in the base xy plane.
Force and moment at base flange definition.
UR3e
35
User Manual
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 35

Dimensionin
g the Stand
The magnitude of the loads depends on robot model, program and multiple other factors.
Dimensioning of the stand shall account for the loads that the robot arm generates during
normal uninterrupted operation and during category 0, 1 and 2 stopping motion.
During stopping motion, the joints are allowed to exceed the maximum nominal operating
torque. The load during stopping motion is independent of the stop category type.
The values stated in the following tables are maximum nominal loads in worst-case
movements multiplied with a safety factor of 2.5. The actual loads will not exceed these
values.
Robot Model
Mz [Nm]
Fz[N]
M xy [Nm]
F xy  [N]
UR3e
170
490
220
390
Maximum joint torques during category 0, 1 and 2 stops.
Robot Model
Mz [Nm]
Fz[N]
M xy [Nm]
F xy  [N]
UR3e
140
370
180
320
Maximum joint torques during normal operation.
The normal operating loads can generally be reduced by lowering the acceleration limits of
the joints. Actual operating loads are dependent on the application and robot program. You
can use URSim to evaluate the expected loads in your specific application.
Safety
margin
s
You can incorporate added safety margins, factoring in the following design considerations:
•   Static stiffness: A stand that is not sufficiently stiff will deflect during robot motion, resulting
in the robot arm not hitting the intended waypoint or path. Lack of static stiffness can also
result in a poor freedrive teaching experience or protective stops.
•   Dynamic stiffness: If the eigenfrequency of the stand matches the movement frequency of
the robot arm, the entire system can resonate, creating the impression that the robot arm is
vibrating. Lack of dynamic stiffness can also result in protective stops. The stand should
have a minimum resonance frequency of 45 Hz.
•   Fatigue: The stand shall be dimensioned to match the expected operating lifetime and load
cycles of the complete system.
CAUTION
•   If the robot is mounted on an external axis, the accelerations of this axis
must not be too high. You can let the robot software compensate for the
acceleration of external axes by using the script command set_base_
acceleration()
•   High accelerations can cause the robot to make safety stops.
WARNING
•   Potential for tip-over Hazards.
•   The robot arm's operational loads can cause movable platforms, such as
tables or mobile robots, to tip over, resulting in possible accidents.
•   Prioritize safety by implementing adequate measures to prevent the
tipping of movable platforms at all times.
User Manual
36
UR3e
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 36

5.3. Mounting Description
Description
Robot arm
(Base)
Mounted with four 8.8 strength, 8.5 mm bolts and four M8 mounting holes
at the base.
Tool (Tool
Flange)
Uses four M6 thread holes for attaching a tool to the robot. The M6 bolts
shall be tightened with 8 Nm, strength class 8.8. For accurate tool
repositioning, use a pin in the Ø6 hole provided.
Control
Box
The Control Box can be hung on a wall or placed on the ground.
Teach
Pendant
The Teach Pendant is wall mounted or placed onto the Control Box.
Verify the cable does not cause tripping hazard. You can buy extra
brackets for mounting the Control Box and Teach Pendant.
CAUTION
Mounting and operating the robot in environments exceeding the recommended
IP rating can result in injury.
•   Mount the robot in an environment suited to the IP rating. The robot must
not be operated in environments that exceed those corresponding to the
IP ratings of the robot (IP54), Teach Pendant (IP54) and Control Box
(IP44)
WARNING
Unstable mounting can lead to accidents.
•   Always make sure the robot parts are properly and securely mounted and
bolted in place.
5.3.1. Singularity
UR3e
37
User Manual
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 37

Description
A singularity is a pose that restricts the motion and the ability to position the robot.
The robot arm can stop moving or have very sudden and fast movements when
approaching and leaving singularity.
WARNING
Make sure that robot motion near a singularity does not create hazards
to anyone within the range of the robot arm, end effector, and
workpiece.
•   Set safety limits for the speed and acceleration of the elbow
joint.
The following causes singularity in the robot arm:
•   Outer workspace limit
•   Inner workspace limit
•   Wrist alignment
Outer
workspace
limit
The singularity occurs because the robot cannot reach far enough or it reaches outside of
the maximum working area.
To avoid: Arrange the equipment around the robot to avoid it reaching outside of the
recommended workspace.
Inner
workspace
limit
The singularity occurs because the movements are directly above or directly below the
robot base. This causes many positions/orientations to be unreachable.
To avoid: Program the robot task in such a way that it is not necessary to work in or close to
the central cylinder. You can also consider mounting the robot base on a horizontal surface
to rotate the central cylinder from a vertical to horizontal orientation, potentially moving it
away from the critical areas of the task.
User Manual
38
UR3e
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 38

Wrist
alignment
This singularity occurs because wrist joint 2 rotates on the same plane as the shoulder,
elbow and wrist joint 1. This limits the range of movement of the robot arm, regardless of
workspace.
To avoid:Layout the robot task in such a way that it is not necessary to align the robot wrist
joints in this manner. You can also offset the direction of the tool, so that the tool can point
horizontally without the problematic wrist alignment.
5.3.2. Fixed and Movable Installation
Description
Whether the robot arm is fixed (mounted to a stand, wall or floor) or in a movable
installation (linear axis, push cart, or mobile robot base), it must be installed securely to
ensure stability through all motions.
UR3e
39
User Manual
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 39

5.4. Securing the Robot Arm
Description
110
10
5  FG8
+
+
0.02
0
X 8
8.5 min.
5 FG8
+
+
0.024
0.006
8.5 min.
45°
110
4 x
6.6
2x 5  ±1
Surface on which the robot is fitted
0.05
Dimensions and hole pattern for mounting the robot.
To power
down the
robot arm
WARNING
Unexpected start-up and/or movement can lead to injury
•   Power down the robot arm to prevent unexpected start-up during
mounting and dismounting.
1.   Press the power button on the Teach Pendant to turn off the robot.
2.   Unplug the mains cable / power cord from the wall socket.
3.   Allow 30 seconds for the robot to discharge any stored energy.
To secure
the robot
arm
1.   Place the robot arm on the surface on which it is to be mounted. The surface must be
even and clean.
2.   Tighten the four 8.8 strength, M6 bolts to a torque of 9 Nm.
(Torque values have been updated SW 5.18. Earlier printed version will show different
values)
3.   If accurate re-mounting of the robot is required, use the Ø5 mm. hole and Ø5x8 mm.
slot with corresponding ISO 2338 Ø5 h6 positioning pins in the mounting plate.
User Manual
40
UR3e
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 40

UR3e
41
User Manual
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 41

5.5. Control Box Clearance
Description
The flow of hot air in the Control Box can result in equipment malfunction.
The Control Box requires a minimum clearance of 50 mm on each side for sufficient cool
airflow. The recommended Control Box clearance is 200 mm.
WARNING
A wet Control Box can cause fatal injury.
•   Make sure the Control Box and cables do not come into contact
with liquids.
•   Place the Control Box (IP44) in an environment suited for the IP
rating.
User Manual
42
UR3e
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 42

5.6. Robot Connections: Base Flange Cable
Description
This subsection describes the connection for a robot arm configured with a Base Flange
Cable connector.
Base Flange
Cable
connector
The Base Flange Cable connector establishes the robot connection by connecting the robot
arm to the Control Box. The Robot Cable connects to the Base Flange Cable connector on
one end, and to the Control Box connector on the other end.
You can lock each connector when robot connection is established.
CAUTION
The maximum robot connection from the robot arm to the Control Box is
6 m. Improper robot connection can result in loss of power to the robot
arm.
•   Do not extend a 6 m Robot Cable.
NOTICE
Connecting the Base Flange Cable directly to any Control Box can result
in equipment or property damage.
•   Do not connect the Base Flange Cable directly to the Control Box.
UR3e
43
User Manual
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 43

5.7. Robot Connections: Robot Cable
Description
This subsection describes the connection for a robot arm configured with a fixed 6 meter
Robot Cable.
To connect
the arm and
Control box
You can turn the connector to the right to make it easier to lock after the cable is plugged in.
•   Establish the robot connection by connecting the robot arm to the Control Box with the
Robot Cable.
•   Plug and lock the cable from the robot into the connector at the bottom of the Control
Box shown below.
•   Twist the connector twice to ensure it is properly locked before turning on the robot
arm.
CAUTION
Improper robot connection can result in loss of power to the robot arm.
•   Do not disconnect the Robot Cable when the robot arm is turned on.
•   Do not extend or modify the original Robot Cable.
User Manual
44
UR3e
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 44

5.8. Mains Connections
Description
The mains cable from the Control Box has a standard IEC plug at the end. Connect a
country specific mains plug, or cable, to the IEC plug.
NOTICE
•   IEC 61000-6-4:Chapter 1 scope: “This part of IEC 61000 for
emission requirement applies to electrical and electronic
equipment intended for use within the environment of existing
at industrial (see 3.1.12) locations.”
•   IEC 61000-6-4:Chapter 3.1.12 industrial location: “Locations
characterized by a separate power network, supplied from a
high- or medium-voltage transformer, dedicated for the supply
of the installation”
Mains
connections
To power the robot, the Control Box   shall be connected to the mains via the supplied
power cord. The IEC C13 connecter on the power cord connects to the IEC C14 appliance
inlet at the bottom of the Control Box.
NOTICE
Always use a power cord with a country specific wall plug when
connecting to the Control Box. Do not use an adapter.
As a part of the electrical installation, provide the following:
•   Connection to ground
•   Main fuse
•   Residual current device
•   A lockable (in the OFF position) switch
A main switch shall be installed to power off all equipment in the robot application as an
easy means for lockout. The electrical specifications are shown in the table below.
Parameter
Min
Typ
Max
Unit
Input voltage
90
-
264
VAC
External mains fuse (90-200V)
8
-
16
A
External mains fuse (200-264V)
8
-
16
A
Input frequency
47
-
440
Hz
Stand-by power
-
-
<1.5
W
Nominal operating power
90
150
325
W
UR3e
45
User Manual
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 45

WARNING: ELECTRICITY
Failure to follow any of the below can result in serious injury or death due to
electrical hazards.
•   Ensure the robot is grounded correctly (electrical connection to ground).
Use the unused bolts associated with grounding symbols inside the
Control Box to create common grounding of all equipment in the system.
The grounding conductor shall have at least the current rating of the
highest current in the system.
•   Ensure the input power to the Control Box is protected with a Residual
Current Device (RCD) and a correct fuse.
•   Lockout all power for the complete robot installation during service.
•   Ensure other equipment shall not supply power to the robot I/O when the
robot is locked out.
•   Ensure all cables are connected correctly before the Control Box is
powered. Always use the original power cord.
User Manual
46
UR3e
5. Assembly
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 46

6. First Boot
Description
The first boot is the initial sequence of actions you can take with the robot after
assembly.
•   This initial sequence requires you to:
•   Start the robot
•   Insert the serial number
•   Intialize the robot arm
•   Power down the robot
While the robot arm is powered on you can use Freedrive to move the robot.
The robot arm requires ample space to operate freely.
CAUTION
Failure to verify the payload and installation before starting up the robot arm can
lead to injury to personnel and/or property damage.
•   Always verify the actual payload and installation are correct before
starting up the robot arm.
CAUTION
Incorrect payload and installation settings prevent the robot arm and Control Box
functioning correctly.
•   Always verify the payload and installation setting are correct.
NOTICE
Starting up the robot in lower temperatures can result in lower performance, or
stops, due to temperature dependent oil and grease viscosity.
•   Starting up the robot in low temperatures can require a warmup phase.
6.1. Starting your robot
UR3e
47
User Manual
6. First Boot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 47

To start
the robot
Start up disengages the braking system in the robot arm, allowing you to use freedrive.
1.   Tap the ON button with the green LED to start the initialization process. Then, the LED
turns yellow to indicate the power is on and in Idle.
2.   Tap the START button to release the breaks.
3.   Tap the OFF button with the red LED to power off the robot arm.
•   When the PolyScope starts, tap the ON button once to power the robot arm. Then, the
status changes to yellow to indicate the robot is on and idle.
•   When the robot arm state is Idle, tap the START button to start robot arm. At this point,
sensor data is checked against the configured mounting of the robot arm.
If a mismatch is found (with a tolerance of 30 ∘ ), the button is disabled and an error
message is displayed below it.
•   If the mounting is verified, tap Start to release all joint brakes and the robot arm is ready
for normal operation.
Robot arm start up is accompanied by sound and slight movements as joint brakes are
released.
6.2. Inserting the Serial Number
To insert the
serial
number
When you install your robot for the first time, you need to configure serial number on the
control box to match the robot arm.
This procedure is also required when you re-install the software on the control box, such as
when receiving a software update.
User Manual
48
UR3e
6. First Boot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 48

When you boot the robot for the first time, please follow these steps:
1.   Select the correct robot arm size.
2.   Select the correct control box.
3.   Add the serial number as it is written on the robot arm.
4.   End with the OK button.
6.3. Initializing the Robot Arm
To initialize
the robot
On your first start up a Cannot Proceed dialog box can appear.
Select Go to initialization screen to access the Initialize screen.
UR3e
49
User Manual
6. First Boot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 49

In the Footer, to the left, the Initialize button indicates the status of the robot arm using
colors:
•   Red Power off. The robot arm is in a stopped state.
•   Yellow Idle. The robot arm is on, but not ready for normal operation.
•   Green Normal. The robot arm is on and ready for normal operation.
6.4. Turning the Control Box On/Off
To turn the
Control Box
on/off
The Control Box mainly contains the physical electrical Input/Output that connects the robot
arm, the Teach Pendant and any peripherals. You must turn on the Control Box to be able to
power on the robot arm.
User Manual
50
UR3e
6. First Boot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 50

1.   On your Teach Pendant, press the power button to turn on the control box.
2.   Wait as text from the underlying operating system, followed by buttons, appear on the
screen.
3.   A Getting Started screen can appear, prompting you to begin programming the robot.
6.5. Powering Down the Robot
To power
down the
robot arm
WARNING
Unexpected start-up and/or movement can lead to injury
•   Power down the robot arm to prevent unexpected start-up during
mounting and dismounting.
1.   Press the power button on the Teach Pendant to turn off the robot.
2.   Unplug the mains cable / power cord from the wall socket.
3.   Allow 30 seconds for the robot to discharge any stored energy.
UR3e
51
User Manual
6. First Boot
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 51

6.6. Freedrive
Description
Freedrive allows the robot arm to be manually pulled into desired positions and/or poses.
The joints move with little resistance because the brakes are released. While the robot
arm is being moved manually, it is in Freedrive.
Resistance increases as the robot arm in Freedrive approaches a predefined limit or
plane. This makes pulling the robot into position feel heavy.
WARNING
Injury to personnel can occur due to unexpected motion.
•   Verify the configured payload is the payload being used.
•   Verify the correct payload is securely attached to the tool flange.
Enabling
Freedrive
You can enable Freedrive in the following ways:
•   Use the 3PE Teach Pendant.
•   Use the Freedrive on robot.
•   Use I/O Actions.
NOTICE
Enabling Freedrive while you are moving the robot arm, can cause it to
drift leading to faults.
•   Do not enable Freedrive while you are pushing or touching the
robot.
3PE Teach
Pendant
To use the 3PE TP button to freedrive the robot arm:
1.   Rapidly light-press, release, light-press again and keep holding the 3PE button in this
position.
Now you can pull the robot arm into a desired position, while the light-press is maintained.
Freedrive on
robot
To use Freedrive on robot to freedrive the robot arm:
1.   Press-and-hold the button of switch configured for Freedrive on robot.
2.   When the Freedrive panel appears in PolyScope, select the desired movement type
for the robot arm’s joints. Or use the list of axes to customize the movement type.
3.   You can define the type of feature if required, by selecting an option from the Feature
dropdown list.
The robot arm can stop moving if it approaches a singularity scenario. Tap All axes
are free in the Freedrive panel to resume movement.
4.   Move the robot arm as desired.
User Manual
52
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 52

Backdrive
During initialization of the robot arm, minor vibrations may be observed when the robot
brakes are released. In some situations, such as when the robot is close to collision, these
vibrations are undesirable. Use Backdrive to force specific joints to a desired position
without releasing all brakes in the robot arm.
UR3e
53
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 53

6.6.1. Freedrive Panel
Description
When the robot arm is in Freedrive, a panel appears on PolyScope, as illustrated below.
User Manual
54
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 54

LED
Freedrive
panel
The LED on the status bar of the Freedrive panel indicates:
•   When one or more joints are approaching their joint limits.
•   When the robot arm’s positioning is approaching singularity. Resistance increases
as the robot approaches singularity, making it feel heavy to position.
Icons
You can lock one or more of the axes allowing the TCP to move in a particular direction, as
defined in the table below.
All axes are free
Movement is allowed through all axes.
Plane
Movement is only allowed through the X-axis and
Y-axis.
Translation
Movement is allowed through all axes, without
rotation.
Rotation
Movement is allowed through all axes, in a
spherical motion, around the TCP.
CAUTION
Moving the robot arm in some axes when a tool is attached, can present a
pinch point.
•   Use caution when moving the robot arm in any axis.
UR3e
55
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 55

User Manual
56
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 56

6.7. Mounting
Description
Specifying the mounting of the Robot arm serves two purposes:
1.   Making the Robot arm appear correctly on screen.
2.   Telling the controller about the direction of gravity.
An advanced dynamics model gives the Robot arm smooth and precise motions, as well
as allows the Robot arm to hold itself in Freedrive Mode. For this reason, it is important
to mount the Robot arm correctly.
WARNING
Failure to mount the Robot’s arm correctly may result in frequent robot
stops, and/or the Robot arm will move when pressing the Freedrive
button.
If the Robot arm is mounted on a flat table or floor, no change is needed on this screen.
However, if the Robot arm is ceiling mounted, wall mounted, or mounted at an angle,
this needs to be adjusted using the buttons.
The buttons on the right side of the screen are for setting the angle of the Robot arm’s
mounting. The top three right side buttons set the angle to ceiling (180 ∘ ), wall (90 ∘ ), floor
(0 ∘ ). The Tilt buttons set an arbitrary angle.
UR3e
57
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 57

The buttons on the lower part of the screen are used to rotate the mounting of the Robot arm
to match the actual mounting.
WARNING
Use the correct installation settings. Save and load the installation files with
the program.
6.8. Power Down The Robot
To power
down the
robot arm
WARNING
Unexpected start-up and/or movement can lead to injury
•   Power down the robot arm to prevent unexpected start-up during
mounting and dismounting.
1.   Press the power button on the Teach Pendant to turn off the robot.
2.   Unplug the mains cable / power cord from the wall socket.
3.   Allow 30 seconds for the robot to discharge any stored energy.
User Manual
58
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 58

7. Installation
Description
Installing the robot can require the configuration and use of input and output signals
(I/Os). These different types of I/Os and their uses are described in the following
sections.
7.1. Electrical Warnings and Cautions
Warnings
Observe the following warnings for all the interface groups, including when you design and
install an application.
WARNING
Failure to follow any of the below can result in serious injury or death, as the
safety functions could be overridden.
•   Never connect safety signals to a PLC that is not a safety PLC with the
correct safety level. It is important to keep safety interface signals
separated from the normal I/O interface signals.
•   All safety-related signals shall be constructed redundantly (two
independent channels).
•   Keep the two independent channels separate so a single fault cannot lead
to loss of the safety function.
WARNING: ELECTRICITY
Failure to follow any of the below can result in serious injury or death due to
electrical hazards.
•   Make sure all equipment not rated for water exposure remain dry. If water
is allowed to enter the product, lockout-tagout all power and then contact
your local Universal Robots service provider for assistance.
•   Only use the original cables supplied with the robot only. Do not use the
robot for applications where the cables are subject to flexing.
•   Use caution when installing interface cables to the robot I/O. The metal
plate in the bottom is intended for interface cables and connectors.
Remove the plate before drilling holes. Make sure that all shavings are
removed before reinstalling the plate. Remember to use correct gland
sizes.
UR3e
59
User Manual
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 59

CAUTION
Disturbing signals with levels higher than those defined in the specific IEC
standards can cause unexpected behaviors from the robot. Be aware of the
following:
•   The robot has been tested according to international IEC standards for
ElectroMagnetic Compatibility (EMC). Very high signal levels or
excessive exposure can damage the robot permanently. EMC problems
are found to happen usually in welding processes and are normally
prompted by error messages in the log. Universal Robots cannot be held
responsible for any damages caused by EMC problems.
•   I/O cables going from the Control Box to other machinery and factory
equipment may not be longer than 30m, unless additional tests are
performed.
GROUND
Negative connections are referred to as Ground (GND) and are connected to the
casing of the robot and the Control Box. All mentioned GND connections are
only for powering and signalling. For PE (Protective Earth) use the M6-size
screw connections marked with earth symbols inside the Control Box. The
grounding conductor shall have at least the current rating of the highest current
in the system.
READ MANUAL
Some I/Os inside the Control Box can be configured for either normal or safety-
related I/O. Read and understand the complete Electrical Interface chapter.
User Manual
60
UR3e
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 60

7.2. Control Box Connection Ports
Description
The underside of the I/O interface groups is equipped with external connection ports, as
illustrated below. There are capped openings at the base of the Control Box cabinet to
run external connector cables to access the ports.
External
connection
ports
The Mini Displayport supports monitors using Displayport. This requires an active Mini
Display to DVI or HDMI converter. Passive converters do not work with DVI/HDMI ports.
The Fuse must be a UL marked, Mini Blade type with maximum current rating: 10A and
minimum voltage rating: 32V
NOTICE
Connecting or disconnecting a Teach Pendant while the Control Box is
powered on can cause damage.
•   Do not connect a Teach Pendant while the Control Box is on.
•   Power off the Control Box before you connect a Teach Pendant.
Do not connect or disconnect the Teach Pendant while Control Box is
powered on. This can cause damage to Control Box.
NOTICE
Failure to plug in the active adapter before powering on the Control Box
can hinder the display output.
•   Plug in the active adapter before powering on the Control Box.
•   In some cases the external monitor must be powered on before
the Control Box.
•   Use an active adapter that supports revision 1.2 as not all adapters
function out-of-the-box.
UR3e
61
User Manual
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 61

7.3. Ethernet
Description
The Ethernet interface can be used for:
•   MODBUS, EtherNet/IP and PROFINET.
•   Remote access and control.
To connect the Ethernet cable by passing it through the hole at the base of the Control Box, and
plugging it into the Ethernet port on the underside of the bracket.
Replace the cap at the base of the Control Box with an appropriate cable gland to connect the cable
to the Ethernet port.
The electrical specifications are shown in the table below.
Parameter
Min
Typ
Max
Unit
Communication speed
10
-
1000
Mb/s
User Manual
62
UR3e
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 62

7.4. 3PE Teach Pendant Installation
7.4.1. Hardware Installation
To remove a
Teach Pendant
NOTICE
Replacing the Teach Pendant can result in the system reporting a fault
on start-up.
•   Always select the correct configuration for the type of Teach
Pendant.
To remove the standard Teach Pendant:
1.   Power down the control box and disconnect the main power cable from the
power source.
2.   Remove and discard the two cable ties used for mounting the Teach Pendant
cables.
3.   Press in the clips on both sides of the Teach Pendant plug as illustrated, and pull
down to disconnect from the Teach Pendant port.
4.   Fully open/loosen the plastic grommet at the bottom of the control box and
remove the Teach Pendant plug and cable.
5.   Gently remove the Teach Pendant cable and Teach Pendant.
1
Clips
2
Plastic grommet
UR3e
63
User Manual
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 63

1
Cable ties
To install a 3PE
Teach Pendant
1.   Place the Teach Pendant plug and cable in through the bottom of the control box
and fully close/tighten the plastic grommet.
2.   Push the Teach Pendant plug into the Teach Pendant port to connect.
3.   Use two new cable ties to mount the Teach Pendant cables.
4.   Connect the main power cable to the power source and power on the control box.
There is always a length of cable with the Teach Pendant that can present a tripping
hazard if it is not stored properly.
•   Always store the Teach Pendant and the cable properly to avoid tripping
hazards.
User Manual
64
UR3e
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 64

7.4.2. New Software Installation
To configure
the
3PE TP
software
1.   On PolyScope, in the Header, tap Installation and select Safety.
2.   Tap Hardware and unlock the options on the Select available hardware screen.
A password is required to unlock this screen.
3.   In the Teach Pendant drop-down list, select 3PE Enabled.
4.   Tap Apply to restart the system. PolyScope continues to run.
5.   Tap Confirm Safety Configuration to complete the 3PE Teach Pendant software
installation.
6.   As the robot restarts and initializes, light-press the 3PE button and tap Start on
PolyScope.
UR3e
65
User Manual
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 65

User Manual
66
UR3e
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 66

7.5. Controller I/O
Description
You can use the I/O inside the Control Box for a wide range of equipment including
pneumatic relays, PLCs and emergency stop buttons.
The illustration below shows the layout of electrical interface groups inside the Control
Box.
24V
EI1
24V
SI0
24V
SI1
24V
EI0
Safety
ON
OFF
12V
Remote
24V
0V
PWR
GND
Power
24V
CI1
24V
CI2
24V
CI3
24V
CI0
Conﬁgurable Inputs
24V
CI5
24V
CI6
24V
CI7
24V
CI4
0V
CO1
0V
CO2
0V
CO3
0V
CO0
Conﬁgurable Outputs
0V
CO5
0V
CO6
0V
CO7
0V
CO4
24V
DI1
24V
DI2
24V
DI3
24V
DI0
Digital Inputs
24V
DI5
24V
DI6
24V
DI7
24V
DI4
0V
DO1
0V
DO2
0V
DO3
0V
DO0
Digital Outputs
0V
DO5
0V
DO6
0V
DO7
0V
DO4
AG
AI1
AG
AO0
AG
AO1
AG
AI0
Analog
Analog Outputs
Analog Inputs
Safeguard Stop
Emergency Stop
GND
0V
24V
DI8
DI9
DI10
DI11
You can use the horizontal Digital Inputs block (DI8-DI11), illustrated below, for
quadrature encoding Conveyor Tracking.
0V
24V
DI8
DI9
DI10
DI11
The meaning of the color schemes listed below must be observed and maintained.
Yellow with red text
Dedicated safety signals
Yellow with black text
Configurable for safety
Gray with black text
General purpose digital I/O
Green with black text
General purpose analog I/O
In the GUI, you can set up configurable I/O as either safety-related I/O or general
purpose I/O.
UR3e
67
User Manual
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 67

Common
specifications
for all digital I/O
This section defines electrical specifications for the following 24V digital I/O of the
Control Box.
•   Safety I/O.
•   Configurable I/O.
•   General purpose I/O.
NOTICE
The word configurable is used for I/O configured as either safety-
related I/O or normal I/O. These are the yellow terminals with black text.
Install the robot according to the electrical specifications which are the same for all three
inputs.
It is possible to power the digital I/O from an internal 24V power supply or from an
external power source by configuring the terminal block called Power. This block
consists of four terminals. The upper two (PWR and GND) are 24V and ground from the
internal 24V supply. The lower two terminals (24V and 0V) in the block are the 24V input
to supply the I/O. The default configuration uses the internal power supply.
Power
supply
If more current is needed, connect an external power supply as shown below.
24V
0V
PWR
GND
Power
24V
0V
PWR
GND
Power
In this example the default configuration using
the internal power supply
In this example the default configuration with
an external power supply for more current.
The electrical specifications for both the internal and external power supply are shown below.
Terminals
Parameter
Min
Typ
Max
Unit
Internal 24V power supply
[PWR   -   GND]
Voltage
23
24
25
V
[PWR   -   GND]
Current
0
-
2*
A
External 24V input requirements
[24V   -   0V]
Voltage
20
24
29
V
[24V   -   0V]
Current
0
-
6
A
*3.5A for 500ms or 33% duty cycle.
User Manual
68
UR3e
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 68

Digital
I/Os
The digital I/O are constructed in compliance with IEC 61131-2. The electrical specifications are
shown below.
Terminals
Parameter
Min
Typ
Max
Unit
Digital Outputs
[COx   /   DOx]
Current*
0
-
1
A
[COx   /   DOx]
Voltage drop
0
-
0.5
V
[COx   /   DOx]
Leakage current
0
-
0.1
mA
[COx   /   DOx]
Function
-
PNP
-
Type
[COx   /   DOx]
IEC 61131-2
-
1A
-
Type
Digital Inputs
[EIx/SIx/CIx/DIx]
Voltage
-3
-
30
V
[EIx/SIx/CIx/DIx]
OFF region
-3
-
5
V
[EIx/SIx/CIx/DIx]
ON region
11
-
30
V
[EIx/SIx/CIx/DIx]
Current (11-30V)
2
-
15
mA
[EIx/SIx/CIx/DIx]
Function
-
PNP +
-
Type
[EIx/SIx/CIx/DIx]
IEC 61131-2
-
3
-
Type
*For resistive loads or inductive loads of maximum 1H.
UR3e
69
User Manual
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 69

7.5.1. I/O Interface Control
Description
The I/O Interface Control allows you to switch between user control and URcap control.
I/O Interface
Control
1.   Tap the Installation tab and under General, tap Tool I/O
2.   Under I/O Interface Control, select User to access the Tool Analog Inputs and/or
Digital Output Mode settings. Selecting a URCap removes access to the Tool Analog
Inputs and the Digital Output Mode settings.
NOTICE
If a URCap controls an end-effector, such as a gripper, then the URCap
requires control of the Tool IO Interface. Select the URCap in the list, to
allow it to control the Tool IO Interface.
User Manual
70
UR3e
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 70

7.5.2. Using the I/O Tab
Description
Use the I/O Tab screen to monitor and set the live I/O signals from/to the Control Box.
The screen displays the current state of the I/O, including during program execution. The
program stops if anything is changed during execution. At program stop, all output
signals retain their states. The screen updates at 10Hz, so a very fast signal might not
display properly.
Configurable I/Os can be reserved for special safety settings defined in the safety I/O
configuration section of the installation (see I/O); those which are reserved will have the
name of the safety function in place of the default or user defined name.
Configurable outputs that are reserved for safety settings are not togglable and will be
displayed as LED’s only.
Voltage
When the Tool Output is controlled by the user, you can configure Voltage. Selecting a
URCap removes access to Voltage.
Analog
Domain
Settings
The analog I/O’s can be set to either current [4-20mA] or voltage [0-10V] output. These
settings are persistent over restarts of the robot controller and saved in the installation.
Control over the tool I/Os could be assigned to a URCap in Tool I/O of the Installation tab.
Selecting a URCap removes user’s control over tool’s analog I/O.
UR3e
71
User Manual
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 71

Tool
Communication
Interface
When the Tool Communication Interface TCI is enabled, the tool analog input
becomes unavailable. On the I/O screen, the Tool Input field appears as shown.
Dual Pin power
When Dual Pin Power is enabled, the tool digital outputs must be named as follows:
•   tool_out[0] (Power)
•   tool_out[1] (GND)
User Manual
72
UR3e
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 72

7.6. Safety I/O
Safety I/O
This section describes dedicated safety input (Yellow terminal with red text) and configurable
I/O (Yellow terminals with black text) when configured as safety I/O.
Safety devices and equipment must be installed according to the safety instructions and the
risk assessment in chapter Safety.
All safety I/O are paired (redundant), so a single fault does not cause loss of the safety
function. However, the safety I/O must be kept as two separate branches.
The permanent safety input types are:
•   Robot Emergency Stop   for emergency stop equipment only
•   Safeguard Stop   for protective devices
•   3PE Stop   for protective devices
Table
The functional difference is shown below.
Emergency
Stop
Safeguard Stop
3PE Stop
Robot stops moving
Yes
Yes
Yes
Program execution
Pauses
Pauses
Pauses
Drive power
Off
On
On
Reset
Manual
Automatic or
manual
Automatic or
manual
Frequency of use
Infrequent
Every cycle to
infrequent
Every cycle to
infrequent
Requires re-initialization
Brake release
only
No
No
Stop Category (IEC 60204-1)
1
2
2
Performance level of monitoring
function (ISO 13849-1)
PLd
PLd
PLd
Safety
caution
Use the configurable I/O to set up additional safety I/O functionality, e.g. Emergency Stop
Output. Use the PolyScope interface to define a set of configurable I/O for safety functions.
CAUTION
Failure to verify and test the safety functions regularly can lead to
hazardous situations.
•   Safety functions shall be verified before putting the robot into
operation.
•   Safety functions shall be tested regularly.
UR3e
73
User Manual
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 73

OSSD
signals
All configured and permanent safety inputs are filtered to allow the use of OSSD safety
equipment with pulse lengths under 3ms. The safety input is sampled every millisecond and
the state of the input is determined by the most frequently seen input signal over the last 7
milliseconds.
OSSD
Safety
Signals
You can configure the Control Box to output OSSD pulses when a safety output is
inactive/high. OSSD pulses detect the ability of the Control Box to make safety outputs
active/low. When OSSD pulses are enabled for an output, a 1ms low pulse is generated on
the safety output once every 32ms. The safety system detects when an output is connected
to a supply and shuts down the robot.
The illustration below shows: the time between pulses on a channel (32ms), the pulse length
(1ms) and the time from a pulse on one channel to a pulse on the other channel (18ms)
To enable OSSD for Safety Output
1.   In the Header, tap Installation and select Safety.
2.   Under Safety, select I/O.
3.   On the I/O screen, under Output Signal, select the desired OSSD checkbox. You must
assign the output signal to enable the OSSD checkboxes.
Default safety
configuration
The robot is delivered with a default configuration, which enables operation without any
additional safety equipment.
24V
EI1
24V
SI0
24V
SI1
24V
EI0
Safety
Safeguard Stop
Emergency Stop
Connecting
emergency
stop buttons
Most applications require one or more extra emergency stop buttons. The illustration
below shows how one or more emergency stop buttons can be connected.
24V
EI1
24V
SI0
24V
SI1
24V
EI0
Safety
Safeguard Stop
Emergency Stop
24V
EI1
24V
SI0
24V
SI1
24V
EI0
Safety
Safeguard Stop
Emergency Stop
User Manual
74
UR3e
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 74

Sharing the
Emergency
Stop with other
machines
You can set up a shared emergency stop function between the robot and other machines
by configuring the following I/O functions via the GUI. The Robot Emergency Stop Input
cannot be used for sharing purposes. If more than two UR robots or other machines need
to be connected, a safety PLC must be used to control the emergency stop signals.
•   Configurable input pair: External Emergency Stop.
•   Configurable output pair: System Stop.
The illustration below shows how two UR robots share their emergency stop functions. In
this example the configured I/Os used are CI0-CI1 and CO0-CO1.
24V
CI1
24V
CI2
24V
CI3
24V
CI0
Configurable Inputs
24V
CI5
24V
CI6
24V
CI7
24V
CI4
0V
CO1
0V
CO2
0V
CO3
0V
CO0
Configurable Outputs
0V
CO5
0V
CO6
0V
CO7
0V
CO4
24V
CI1
24V
CI2
24V
CI3
24V
CI0
Configurable Inputs
24V
CI5
24V
CI6
24V
CI7
24V
CI4
0V
CO1
0V
CO2
0V
CO3
0V
CO0
Configurable Outputs
0V
CO5
0V
CO6
0V
CO7
0V
CO4
A
B
Safeguard
stop with
automatic
resume
This configuration is only intended for applications where the operator cannot go through
the door and close it behind him. The configurable I/O is used to setup a reset button
outside the door to reactivate robot motion. The robot resumes movement automatically
when the signal is re-established.
WARNING
Do not use this configuration if signal can be re-established from the
inside of the safety perimeter.
24V
EI1
24V
SI0
24V
SI1
24V
EI0
Safety
Safeguard Stop
Emergency Stop
24V
EI1
24V
SI0
24V
SI1
24V
EI0
Safety
Safeguard Stop
Emergency Stop
24V
0V
24V
0V
In this example a door switch is a basic
safeguard device where the robot is
stopped when the door is opened.
In this example a safety mat is a safety device
where automatic resume is appropriate. This
example is also valid for a safety laser scanner.
UR3e
75
User Manual
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 75

Safeguard
Stop with
reset button
If the safeguard interface is used to interact with a light curtain, a reset outside the safety
perimeter is required. The reset button must be a two channel type. In this example the I/O
configured for reset is CI0-CI1.
24V
EI1
24V
SI0
24V
SI1
24V
EI0
Safety
Safeguard7Stop
Emergency7Stop
24V
0V
24V
0V
24V
CI1
24V
CI2
24V
CI3
24V
CI0
Configurable7Inputs
24V
CI5
24V
CI6
24V
CI7
24V
CI4
User Manual
76
UR3e
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 76

UR3e
77
User Manual
7. Installation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 77

7.6.1. I/O Signals
Description
The I/O are divided between inputs and outputs and are paired up so that each function
provides a Category 3 and PLd I/O.
Input
Signals
The inputs are described in the tables below:
Emergency
Stop Button
Performs a Stop Category 1 (IEC 60204-1) informing other machines
using the System Stop output if that outputis defined. A stop is initiated
in anything connected to the output.
Robot
Emergency
Stop
Performs a Stop Category 1 (IEC 60204-1) via Control Box input,
informing other machines using the System Emergency Stop Output if
that outputis defined.
External
Emergency
Stop
Performs a Stop Category 1 (IEC 60204-1) on robot only.
Reduced
All safety limits can be applied while the robot is using a Normal
configuration, or a Reduced configuration.
When configured, a low signal sent to the inputs causes the safety
system to transition to the reduced configuration. The robot arm
decelerates to satisfy the reduced parameters.
The safety system guarantees the robot is within reduced limits less
than 0.5s after the input is triggered. If the robot arm continues to
violate any of the reduced limits, a Stop Category 0 is triggered. Trigger
planes can also cause a transition to the reduced configuration. The
safety system transitions to the normal configuration in the same way.
User Manual
78
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 78

Input
Signals
The inputs are described in the tables below:
Operational
Mode
When an external mode selection is used it switches between
Automatic Mode and Manual Mode. The robot is in Automatic mode
when input is low and Manual mode when the input is high.
Safeguard
Reset
Returns from the Safeguard Stop state, when a rising edge on the
Safeguard Reset input occurs. When a Safeguard Stop occurs, this
input ensures that the Safeguard Stop state continues until a reset is
triggered.
Safeguard
A stop triggered by a safeguard input. Performs a Stop Category 2
(IEC 60204-1) in all modes, when triggered by a Safeguard.
Automatic
Mode
Safeguard
Stop
Performs a Stop Category 2 (IEC 60204-1) in Automatic mode ONLY.
Automatic Mode Safeguard Stop can only be selected when a Three-
Position Enabling Device is configured and installed.
Automatic
Mode
Safeguard
Reset
Returns from the Automatic Mode Safeguard Stop state when a rising
edge on the Automatic Mode Safeguard Reset input occurs.
3-Position
Enabling
Device
In Manual Mode, an external 3-Position Enabling Device must be
pressed and held in the center-on position to move the robot. If you are
using a built-in 3-Position Enabling Device, the button must be pressed
and held in the mid position to move the robot.
Freedrive on
robot
You can configure the Freedrive input to enable and use Freedrive
without pressing the Freedrive button on a standard TP, or without
having to press-and-hold any of the buttons on the 3PE TP in the light-
press position.
WARNING
When the default Safeguard Reset is disabled, an automatic reset happens
when the safeguard no longer triggers a stop.
This can happen if a person passes though the field of the safeguard.
If a person is not detected by the safeguard and the person is exposed to
hazards, automatic reset is forbidden by standards.
•   Use the external reset to ensure resetting only when a person is not
exposed to hazards.
WARNING
When Automatic Mode Safeguard stop is enabled, a safeguard Stop is not
triggered in Manual Mode.
UR3e
79
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 79

Output
Signals
All safety outputs go low in the event of a safety system violation or fault. This means the
System Stop output initiates a stop even when an E-stop is not triggered.
You can use the following Safety functions output signals. All signals return to low when the
state which triggered the high signal has ended:
1 System
Stop
Signal is Low when the safety system has been triggered into a stopped
state including by the Robot Emergency Stop input or the Emergency
Stop Button. To avoid deadlocks, if the Emergency Stopped state is
triggered by the System Stop input, low signal will not be given.
Robot
Moving
Signal is Low if the robot is moving, otherwise high.
Robot Not
Stopping
Signal is High when the robot is stopped or in the process of stopping
due to an emergency stop or safeguard stop. Otherwise it will be logic
low.
Reduced
Signal is Low when reduced parameters are active or if the safety input
is configured with a reduced input and the signal is currently low.
Otherwise the signal is high.
Not
Reduced
This is the inverse of Reduced, defined above.
Safe Home
Signal is High if the Robot Arm is stopped and is located in the
configured Safe Home Position. Otherwise, the signal is Low. This is
often used when UR robots are integrated with mobile robots.
NOTICE
Any external machinery receiving its Emergency Stop state from the robot
through the System Stop output must comply with ISO 13850. This is
particularly necessary in setups where the Robot Emergency Stop input is
connected to an external Emergency Stop device. In such cases, the System
Stop output becomes high when the external Emergency Stop device is
released. This implies that the emergency stop state at the external machinery
will be reset with no manual action needed from the robot’s operator. Hence,
to comply with safety standards, the external machinery must require manual
action in order to resume.
1 System Stop was previously known as "System Emergency Stop" for Universal Robots robots. PolyScope
can display "System Emergency Stop".
User Manual
80
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 80

7.6.2. I/O Setup
Description
Use the I/O Setup screen to define I/O signals and configure actions with the I/O tab
control. The types of I/O signals are listed under Input and Output.
You can use a fieldbus, for example, Profinet and EtherNet/IP, to access the general
purpose registers.
If you enable the Tool Communication Interface (TCI), the tool analog input becomes
unavailable.
NOTICE
When starting programs from an I/O or fieldbus input, the robot can
begin movement from the position it has, there will not be any manual
movement to the first waypoint via PolyScope required.
I/O Signal
Type
To limit the number of signals listed under Input and Output, use the View drop-down menu
to change the displayed content based on signal type.
Assigning
User-defined
Names
You can name the Input and Output signals to easily identify the ones being used.
1.   Select the desired signal.
2.   Tap the text field to type a name for the signal.
3.   To reset the name to default, tap Clear.
You must provide a user-defined name for a general purpose register to make it available in
the program (i.e., for a Wait command or the conditional expression of an If command).
The Wait and If commands are described in ( Wait ) and ( If ), respectively. You can find
named general purpose registers in the Input or Output selector on the Expression Editor
screen.
UR3e
81
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 81

I/O Actions
and I/O Tab
Control
You can use Physical and Fieldbus digital I/Os to trigger actions or react to the status of a
program.
I/O Tab
Control
Use I/O Tab Control to specify whether an output is controlled on the I/O tab (by either
programmers, or both operators and programmers), or if it is controlled by the robot
programs.
Available
Input
Actions
Command
Action
Start
Starts or resumes the current program on a rising edge (only enabled
in Remote Control)
Stop
Stops the current program on a rising edge
Pause
Pauses the current program on a rising edge
Freedrive
When the input is high, the robot goes into freedrive (similar to the
freedrive button).
The input is ignored if other conditions disallow freedrive.
WARNING
If the robot is stopped while using the Start input action, the robot slowly
moves to the first waypoint of the program before executing that program. If
the robot is paused while using the Start input action, the robot slowly moves
to the position from where it was paused before resuming that program.
User Manual
82
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 82

Available
Output
Actions
Action
Output
state
Program state
Low when not running
Low
Stopped or
paused
High when not running
High
Stopped or
paused
High when running, low when stopped
Low
High
Running,
Stopped or
paused
Low on unscheduled stop
Low
Program
terminated
unscheduled
Low on unscheduled stop, otherwise High
Low
High
Program
terminated
unscheduled
Running,
stopped or
paused
Continuous Pulse
Alternates
between
high and
low
Running
(pause or stop
the program to
maintain the
pulse state)
Program
Termination
Cause
An unscheduled program termination can occur for any of the reasons listed below:
•   Robot stop
•   Fault
•   Violation
•   Runtime exception
UR3e
83
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 83

7.7. Three Position Enabling Device
Description
The robot arm is equipped with an enabling device in the form of the 3PE Teach
Pendant.
The Control Box supports the following enabling device configurations:
•   3PE Teach Pendant
•   External Three-Position Enabling device
•   External Three-Position device and 3PE Teach Pendant
The illustration below shows how to connect a Three-Position Enabling device.
24V
CI1
24V
CI2
24V
CI3
24V
CI0
24V
CI5
24V
CI6
24V
CI7
24V
CI4
Configurable Inputs
3-Position Switch
Note: The two input channels for the Three-Position Enabling Device input have a
disagreement tolerance of 1 second.
NOTICE
The UR robot safety system does not support multiple external Three-
Position Enabling Devices.
Operational
Mode Switch
Using a Three-Position Enabling device requires the use of an Operational Mode switch.
The illustration below shows an Operational Mode switch.
24V
CI1
24V
CI2
24V
CI3
24V
CI0
24V
CI5
24V
CI6
24V
CI7
24V
CI4
Configurable Inputs
Operational mode Switch
User Manual
84
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 84

7.8. General Purpose Analog I/O
Description
The analog I/O interface is the green terminal. It is used to set or measure voltage (0-
10V) or current (4-20mA) to and from other equipment.
The following directions is recommended to achieve the highest accuracy.
•   Use the AG terminal closest to the I/O. The pair share a common mode filter.
•   Use the same GND (0V) for equipment and Control Box. The analog I/O is not
galvanically isolated from the Control Box.
•   Use a shielded cable or twisted pairs. Connect the shield to the GND terminal at
the terminal called Power.
•   Use equipment that works in current mode. Current signals are less sensitive to
interferences.
Electrical
Specifications
In the GUI you can select input modes. The electrical specifications are shown below.
Terminals
Parameter
Min
Typ
Max
Unit
Analog Input in current mode
[AIx   -   AG]
Current
4
-
20
mA
[AIx   -   AG]
Resistance
-
20
-
ohm
[AIx   -   AG]
Resolution
-
12
-
bit
Analog Input in voltage mode
[AIx   -   AG]
Voltage
0
-
10
V
[AIx   -   AG]
Resistance
-
10
-
Kohm
[AIx   -   AG]
Resolution
-
12
-
bit
Analog Output in current mode
[AOx   -   AG]
Current
4
-
20
mA
[AOx   -   AG]
Voltage
0
-
24
V
[AOx   -   AG]
Resolution
-
12
-
bit
Analog Output in voltage mode
[AOx   -   AG]
Voltage
0
-
10
V
[AOx   -   AG]
Current
-20
-
20
mA
[AOx   -   AG]
Resistance
-
1
-
ohm
[AOx   -   AG]
Resolution
-
12
-
bit
UR3e
85
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 85

Analog
Output and
Analog
Input
AG
AI1
AG
AO0
AG
AO1
AG
AI0
Analog
Analog Outputs
Analog Inputs
24V
0V
PWR
GND
Power
AG
AI1
AG
AO0
AG
AO1
AG
AI0
Analog
Analog Outputs
Analog Inputs
24V
0V
PWR
GND
Power
This example illustrates controlling a
conveyor belt with an analog speed control
input.
This example illustrates connecting an
analog sensor.
7.8.1. Analog Input: Communication Interface
Description
The Tool Communication Interface (TCI) enables the robot to communicate with an
attached tool via the robot tool analog input. This removes the need for external cabling.
Once the Tool Communication Interface is enabled, all tool analog inputs are
unavailable
Tool
Communication
Interface
1.   Tap the Installation tab and under General tap Tool I/O.
2.   Select Communication Interface to edit TCI settings.
Once the TCI is enabled, the tool analog input is unavailable for the I/O Setup of
the Installation and does not appear in the input list. Tool analog input is also
unavailable for programs as Wait For options and expressions.
3.   In the drop-down menus under Communication Interface, select required values.
Any changes in values are immediately sent to the tool. If any installation values
differ from what the tool is using, a warning appears.
User Manual
86
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 86

7.9. General Purpose Digital I/O
Description
The Startup screen contains settings for automatically loading and starting a default
program, and for auto-initializing the Robot arm during power up.
General
purpose
digital I/O
This section describes the general purpose 24V I/O (Gray terminals) and the configurable
I/O (Yellow terminals with black text) when not configured as safety I/O.
The general purpose I/O can be used to drive equipment like pneumatic relays directly or for
communication with other PLC systems. All Digital Outputs can be disabled automatically
when program execution is stopped.
In this mode, the output is always low when a program is not running. Examples are shown in
the following subsections.
These examples use regular Digital Outputs but any configurable outputs could also have be
used if they are not configured to perform a safety function.
0V
DO1
0V
DO2
0V
DO3
0V
DO0
Digital Outputs
0V
DO5
0V
DO6
0V
DO7
0V
DO4
LOAD
24V
DI1
24V
DI2
24V
DI3
24V
DI0
Digital Inputs
24V
DI5
24V
DI6
24V
DI7
24V
DI4
In this example a load is controlled from a Digital
Outputs when connected.
In this example a simple button is
connected to a Digital Input.
Communication
with other
machines or
PLCs
You can use the digital I/O to communicate with other equipment if a common GND
(0V) is established and if the machine uses PNP technology, see below.
24V
DI1
24V
DI2
24V
DI3
24V
DI0
Digital Inputs
24V
DI5
24V
DI6
24V
DI7
24V
DI4
0V
DO1
0V
DO2
0V
DO3
0V
DO0
Digital Outputs
0V
DO5
0V
DO6
0V
DO7
0V
DO4
24V
DI1
24V
DI2
24V
DI3
24V
DI0
Digital Inputs
24V
DI5
24V
DI6
24V
DI7
24V
DI4
0V
DO1
0V
DO2
0V
DO3
0V
DO0
Digital Outputs
0V
DO5
0V
DO6
0V
DO7
0V
DO4
A   B
UR3e
87
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 87

7.9.1. Digital Output
Description
The tool communication interface allows two digital outputs to be independently
configured. In PolyScope, each pin has a drop-down menu that allows the output mode
to be set. The following options are available:
•   Sinking: This allows the pin to be configured in an NPN or Sinking configuration.
When the output is off, the pin allows a current to flow to the ground. This can be
used in conjunction with the PWR pin to create a full circuit.
•   Sourcing: This allows the pin to be configured in a PNP or Sourcing configuration.
When the output is on, the pin provides a positive voltage source (configurable in
the IO Tab). This can be used in conjunction with the GND pin to create a full
circuit.
•   Push / Pull: This allows the pin to be configured in a Push / Pull configuration.
When the output is on, the pin provides a positive voltage source (configurable in
IO Tab). This can be used in conjunction with the GND pin to create a full circuit
When the output is off, the pin allows a current to flow to the ground.
After selecting a new output configuration, the changes take effect. The currently loaded
installation is modified to reflect the new configuration. After verifying the tool outputs are
working as intended, make sure to save the installation to prevent losing changes.
Dual Pin
Power
Dual Pin Power is used as a source of power for the tool. Enabling Dual Pin Power disables
default tool digital outputs.
User Manual
88
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 88

7.10. Remote ON/OFF control
Description
Use remote ON/OFF control to turn the Control Box on and off without using the Teach
Pendant. It is typically used:
•   When the Teach Pendant is inaccessible.
•   When a PLC system must have full control.
•   When several robots must be turned on or off at the same time.
Remote
Control
The remote ON/OFF control provides a auxiliary 12V supply, kept active when the Control Box
is turned off. The ON input is intended only for short time activation and works in the same way
as the POWER button. The OFF input can be held down as desired. Use a software feature to
load and start programs automatically (see part  Part II PolyScope Manual ).
The electrical specifications are shown below.
Terminals
Parameter
Min
Typ
Max
Unit
[12V   -   GND]
Voltage
10
12
13
V
[12V   -   GND]
Current
-
-
100
mA
[ON   /   OFF]
Inactive voltage
0
-
0.5
V
[ON   /   OFF]
Active voltage
5
-
12
V
[ON   /   OFF]
Input current
-
1
-
mA
[ON]
Activation time
200
-
600
ms
ON
OFF
12V
Remote
GND
ON
OFF
12V
Remote
GND
This example illustrates connecting a remote
ON button.
This example illustrates connecting a remote
OFF button.
CAUTION
Maintaining a press and hold on the power button switches the Control Box OFF
without saving.
•   Do not press and hold the ON input or the POWER button without saving.
•   Use the OFF input for remote off control to allow the Control Box to save
open files and shut down correctly.
UR3e
89
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 89

7.11. End Effector Integration
Description
The end effector can also be referred to as the tool and the workpiece in this manual.
NOTICE
UR provides documentation for the end effector to be integrated with
the robot arm.
•   Refer to the documentation specific to the end
effector/tool/workpiece for mounting and connection.
User Manual
90
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 90

7.11.1. Tool I/O
Tool
Connector
The tool connector illustrated below provides power and control signals for the grippers
and sensors used on a specific robot tool. The tool connector has eight holes and is
located next to the tool flange on Wrist 3.
The eight wires inside the connector have different functions, as listed in the table:
Pin #
Signal
Description
1
AI3 / RS485-
Analog in 3 or RS485-
2
AI2 / RS485+
Analog in 2 or RS485+
3
TO0/PWR
Digital Outputs 0 or 0V/12V/24V
4
TO1/GND
Digital Outputs 1 or Ground
5
POWER
0V/12V/24V
6
TI0
Digital Inputs 0
7
TI1
Digital Inputs 1
8
GND
Ground
NOTICE
The Tool Connector must be manually tightened up to a maximum of
0.4 Nm.
Tool I/O
Accessories
The UR20 tool I/O can require an accessory element to facilitate connection with tools.
Depending on the tool, you can use the following tool I/O accessories: Tool Flange
Adapter (see  Tool Flange Accessories ) and/or Tool Cable Adapter.
UR3e
91
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 91

Tool Cable
Adapter
The Tool Cable Adapter is the electronic accessory that allows compatibility between the tool
I/O and e-Series tools.
1
Connects to the tool/end effector.
2
Connects to the robot.
WARNING
Connecting the Tool Cable Adapter to a robot that is powered on can lead to
injury.
•   Connect the adapter to the tool/end effector before connecting the
adapter to the robot.
•   Do not power on the robot if the Tool Cable Adapter is not connected
to the tool/end effector.
The eight wires inside the Tool Cable Adapter have different functions, as listed in the table
below:
Pin #
Signal
Description
1
AI2 / RS485+
Analog in 2 or RS485+
2
AI3 / RS485-
Analog in 3 or RS485-
3
TI1
Digital Inputs 1
4
TI0
Digital Inputs 0
5
POWER
0V/12V/24V
6
TO1/GND
Digital Outputs 1 or Ground
7
TO0/PWR
Digital Outputs 0 or 0V/12V/24V
8
GND
Ground
GROUND
The tool flange is connected to GND (Ground).
7.11.2. Maximum Payload
User Manual
92
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 92

Description
The rated robot arm payload depends on the center of gravity (CoG) offset of the
payload, as shown below. The CoG offset is defined as the distance from the center of
the tool flange to the center of gravity of the attached payload.
The robot arm can accommodate a long center of gravity offset, if the payload is placed
below the tool flange. For example when computing the payload mass in a pick and
place application, consider both the gripper and the workpiece.
The robot's capacity to accelerate can be reduced if the payload CoG exceeds the
robot's reach and payload. You can verify the reach and payload of your robot in the
Technical Specifications.
Payload [kg]
0
100
200
300
400
1
2
3
4
Center of gravity offset [mm]
The relationship between the rated payload and the center of gravity offset.
Payload
inertia
You can configure high inertia payloads, if the payload is set correctly.
The controller software automatically adjusts accelerations when the following parameters
are correclty configured:
•   Payload mass
•   Center of gravity
•   Inertia
You can use the URSim to evaluate the accelerations and cycle times of the robot motions
with a specific payload.
UR3e
93
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 93

7.11.3. Securing Tool
Description
The tool or workpiece is mounted to the tool output flange (ISO) at the tip of the robot.
Dimensions and hole pattern of the tool flange. All measurements are in millimeters.
Tool flange
The tool output flange (ISO 9409-1) is where the tool is mounted at the tip of the robot. It is
recommended to use a radially slotted hole for the positioning pin to avoid over-constraining,
while keeping precise position.
CAUTION
Very long M8 bolts can press against the bottom of the tool flange and short
circuit the robot.
•   Do not use bolts that extend beyond 10 mm to mount the tool.
WARNING
Failure to tighten bolts properly cause injury due to loss of the adapter flange
and/or end effector.
•   Ensure the tool is properly and securely bolted in place.
•   Ensure the tool is constructed such that it cannot create a hazardous
situation by dropping a part unexpectedly.
User Manual
94
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 94

7.11.4. Set Payload
Description
The Set Payload   command allows you to configure the payload for the robot. Payload is
the combined weight of everything attached to the robot tool flange.
When to use:
•   When adjusting the payload weight to prevent the robot from triggering a robot
stop. A correctly configured payload weight ensures optimal robot movement.
Setting the payload correctly ensures optimal motion performance and avoids
robot stops.
•   When setting up the payload for use in a pick and place program, using a gripper.
Set Payload
Use the Set
Payload
command
1.   In your robot program, select the place or node where you wish to add a Set
command.
2.   Under Basic, tap Set Payload.
3.   Use the drop-down, under Select Payload.
a.   Select one of the payloads already configured.
b.   Or, use the drop-down to configure a new payload by selecting Custom
Payload and completing the mass and CoG fields.
Tip
You can also use the Set Now button to set the values on the node as the active payload.
Use tip
Remember to always update your payload when making any changes to the
configuration of the robot program.
Example: Set
Payload
In a pick and place program, you would create a default payload in the installation. Then
you add a Set Payload when picking up an object. You would update the payload after
the gripper closes, but before starting to move.
Additionally, you would use the Set Payload after the object has been released.
UR3e
95
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 95

Payload
Transition Time
This is the time it takes the robot to adjust for a given payload. At the bottom of the
screen, you can set the transition time between different payloads.
You can add a payload transition time in seconds.
Setting a transition time larger than zero, prevents the robot from doing a small "jump",
when the payload changes. The program continues while the adjustment is taking place.
Using the Payload Transition Time is recommended when
picking up or releasing heavy objects or using a vacuum gripper.
User Manual
96
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 96

Payload
Description
You must set the Payload, the CoG and the inertia for the robot to perform optimally.
You can define multiple Payloads, and switch between them in your program. This is
useful in Pick and Place applications, for example, where the robot picks up and
releases an object.
Adding,
Renaming,
Modfying and
Removing
Payloads
You can start configuring a new Payload with the following actions:
•   Tap the
to define a new Payload with a unique name. The new payload is
available in the drop-down menu.
•   Tap the
to rename a Payload.
•   Tap the
to remove a selected Payload. You cannot remove the last Payload.
Active
Payload
The checkmark in the drop-down indicates which payload is active
. The
active Payload can be changed using the
.
Default
Payload
The default Payload is set as the active Payload before the program starts.
•   Select the desired Payload and tap Set as default to set a Payload as the default.
The green icon in the drop-down menu indicates the default configured Payload
.
Setting the
Center of
Gravity
Tap the fields  CX ,  CY  and  CZ  to set the center of gravity. The settings apply to the selected
Payload.
UR3e
97
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 97

Payload
Estimation
This feature allows the robot to help set the correct Payload and Center of Gravity (CoG).
Using the
Payload
Estimation
Wizard
1.   In the Installation Tab, under General, select Payload.
2.   On the Payload screen, tap Measure.
3.   In the Payload Estimation Wizard tap Next.
4.   Follow the steps in the Payload Estimation Wizard to set the four positions.
Setting the four positions requires moving the robot arm into four different positions.
The load of the payload is measured at each position.
5.   Once all measurements are complete, you can verify the result and tap Finish.
NOTICE
Follow the these guidelines for best Payload Estimation results:
•   Ensure the TCP positions are as different as possible from each
other
•   Perform the measurements within a short timespan
•   Avoid pulling on the tool and/or attached payload before and
during estimation
•   Robot mounting and angle must be correctly defined in the
installation
User Manual
98
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 98

Setting
Inertia
Values
You can select Use custom Inertia Matrix to set inertia values.
Tap the fields:  IXX ,  IYY ,  IZZ ,  IXY ,  IXZ  and  IYZ  to set the inertia for the selected Payload.
The inertia is specified in a coordinate system with the origin at the Center of Gravity (CoG) of
the payload and the axes aligned with the tool flange axes.
The default inertia is calculated as the inertia of a sphere with the user specified mass, and a
mass density of 1g/cm 3
UR3e
99
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 99

7.11.5. Tool I/O Installation Specifications
Description
The electrical specifications are shown below. Access Tool I/O in the Installation Tab to
set the internal power supply to 0V, 12V or 24V.
Parameter
Min
Typ
Max
Unit
Supply voltage in 24V mode
23.5
24
24.8
V
Supply voltage in 12V mode
11.5
12
12.5
V
Supply current (single pin)*
-
600
2000**
mA
Supply current (dual pin)*
-
600
2000**
mA
Supply capacitive load
-
-
8000***
uF
* It is highly recommended to use a protective diode for inductive loads.
** Peak for max 1 second, duty cycle max: 10%. Average current over 10 seconds must
not exceed typical current.
*** When tool power is enabled, a 400 ms soft start time begins allowing a capacitive
load of 8000 uF to be connected to the tool power supply at start-up. Hot-plugging the
capacitive load is not allowed.
User Manual
100
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 100

7.11.6. Tool Power Supply
Description
Access Tool I/O in the Installation Tab
Dual Pin
Power
Supply
In Dual Pin Power mode, the output current can be increased as listed in Tool I/O.
1.   In the Header, tap Installation.
2.   In the list on the left, tap General.
3.   Tap Tool IO and select Dual Pin Power.
4.   Connect the wires Power (gray) to TO0 (blue) and Ground (red) to TO1 (pink).
NOTICE
Once the robot makes an Emergency Stop, the voltage is set to 0V for both
Power Pins (power is off).
UR3e
101
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 101

7.11.7. Tool Digital Outputs
Description
Digital Outputs support three different modes:
Mode
Active
Inactive
Sinking (NPN)
Low
Open
Sourcing (PNP)
High
Open
Push / Pull
High
Low
Access Tool I/O in the Installation Tab to configure the output mode of each pin. The
electrical specifications are shown below:
Parameter
Min
Typ
Max
Unit
Voltage when open
-0.5
-
26
V
Voltage when sinking 1A
-
0.08
0.09
V
Current when sourcing/sinking
0
600
1000
mA
Current through GND
0
1000
3000*
mA
NOTICE
Once the robot makes an Emergency Stop, the Digital Outputs (DO0 and DO1)
are deactivated (High Z).
CAUTION
The Digital Outputs in the tool are not current-limited. Overriding the specified
data can cause permanent damage.
Using Tool
Digital
Outputs
This example illustrates turning on a load using the internal 12V or 24V power supply. The
output voltage at the I/O tab must be define. There is voltage between the POWER
connection and the shield/ground, even when the load is turned off.
TO0
POWER
It is recommended to use a protective diode for inductive loads, as shown below.
TO0
POWER
User Manual
102
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 102

7.11.8. Tool Digital Inputs
Description
The Startup screen contains settings for automatically loading and starting a default
program, and for auto-initializing the Robot arm during power up.
Table
The Digital Inputs are implemented as PNP with weak pull-down resistors. This means that a
floating input always reads as low. The electrical specifications are shown below.
Parameter
Min
Type
Max
Unit
Input voltage
-0.5
-
26
V
Logical low voltage
-
-
2.0
V
Logical high voltage
5.5
-
-
V
Input resistance
-
47k
-
Ω
Using the
Tool Digital
Inputs
This example illustrates connecting a simple button.
TI0
POWER
7.11.9. Tool Analogue Inputs
Description
Tool Analogue Input are non-differential and can be set to either voltage (0-10V) or
current (4-20mA) on the I/O tab. The electrical specifications are shown below.
Parameter
Min
Type
Max
Unit
Input voltage in voltage mode
-0.5
-
26
V
Input resistance @ range 0V to 10V
-
10.7
-
kΩ
Resolution
-
12
-
bit
Input voltage in current mode
-0.5
-
5.0
V
Input current in current mode
-2.5
-
25
mA
Input resistance @ range 4mA to 20mA
-
182
188
Ω
Resolution
-
12
-
bit
Two examples of using Analog Input are shown in the following subsections.
UR3e
103
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 103

Caution
CAUTION
Analog Inputs are not protected against over voltage in current mode.
Exceeding the limit in the electrical specification can cause permanent
damage to the input.
Using Tool
Analog Inputs,
Non-
differential
This example shows an analog sensor connection with a non-differential output. The
sensor output can be either current or voltage, as long as the input mode of that Analog
Input is set to the same on the I/O tab.
Note: You can check that a sensor with voltage output can drive the internal resistance of
the tool, or the measurement might be invalid.
GND
POWER
AI8
AI2
Using Tool
Analog Inputs,
differential
This example shows an analog sensor connection with a differential output. Connecting the
negative output part to GND (0V), works in the same way as a non-differential sensor.
POWER
AI8
GND
AI2
7.11.10. Tool Communication I/O
Description
•   Signal requests The RS485 signals use internal fail-safe biasing. If the attached
device does not support this fail-safe, signal biasing must either be done in the
attached tool, or added externally by adding pull-up resistors to RS485+ and pull-
down to RS485-.
•   Latency The latency of messages sent via the tool connector ranges from 2ms to
4ms, from the time the message is written on the PC to the start of the message
on the RS485. A buffer stores data sent to the tool connector until the line goes
idle. Once 1000 bytes of data have been received, the message is written on the
device.
Baud Rates
9.6k, 19.2k, 38.4k, 57.6k, 115.2k, 1M, 2M, 5M
Stop Bits
1, 2
Parity
None, Odd, Even
User Manual
104
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 104

8. First Time Use
Description
This section describes how you get started using the robot. Among other things, it covers
easy start-up, an overview of the Polyscope user interface and how to set up your first
program. Additionally, it covers free drive mode and basic operation.
8.1. Quick System Start-up
Quick System
Start
MANDATORY ACTION
Before using the PolyScope, verify the robot arm and Control Box are
correctly installed.
This is how you quickly start up the robot.
1.   On the Teach Pendant, press the emergency stop button.
2.   On the Teach Pendant, press the power button and allow the system to start,
displaying text on the PolyScope.
3.   A popup appears on the touch screen indicating that the system is ready and that
the robot must be initialized.
4.   In the popup dialog, tap Go to Initialize Screen to access the Initialize screen.
5.   Unlock the emergency stop button to change robot state from Emergency Stopped
to Power off.
6.   Step outside the reach (workspace) of the robot.
7.   On the Initialize Robot screen, tap the ON button and allow robot state to change to
Idle.
8.   In the Payload field, in Active Payload, verify the payload mass. You can also
verify the mounting position is correct, in the Robot field.
9.   Tap the Start button, for the robot to release its brake system. The robot vibrates
and makes clicking sounds indicating it is ready to be programmed.
NOTICE
Learn to program your Universal Robots robot on  www.universal-
robots.com/academy/
UR3e
105
User Manual
8. First Time Use
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 105

8.2. The First Program
Description
A program is a list of commands telling the robot what to do. For most tasks,
programming is done entirely using the PolyScope software. PolyScope allows you to
teach the robot arm how to move using a series of waypoints to set up a path for the
robot arm to follow.
Use the Move tab to move the Robot Arm to a desired position, or teach the position by
pulling the Robot Arm into place while holding down the Freedrive button at the top of the
Teach Pendant.
You can create a program can to send I/O signals to other machines at certain points in
the robot’s path, and perform commands like if…then and loop, based on variables and
I/O signals.
User Manual
106
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 106

To create a
simple
program
1.   On PolyScope, in the Header File Path, tap New... and select Program.
2.   Under Basic, tap Waypoint to add a waypoint to the program tree. A default MoveJ is
also added to the program tree.
3.   Select the new waypoint and in the Command tab, tap Waypoint.
4.   On the Move Tool screen, move the robot arm by pressing the move arrows.
You can also move the robot arm by holding down the Freedrive button and pulling the
Robot Arm into desired positions.
5.   Once the robot arm is in position, press OK and the new waypoint displays as
Waypoint_1.
6.   Follow steps 2 to 5 to create Waypoint_2.
7.   Select Waypoint_2 and press the Move Up arrow until it is above Waypoint_1 to
change the order of the movements.
8.   Stand clear, hold on to the emergency stop button and in the PolyScope Footer, press
Play button for the Robot Arm to move between Waypoint_1 and Waypoint_2.
Congratulations! You have now produced your first robot program that moves the
Robot Arm between the two given waypoints.
NOTICE
1.   Do not drive the robot into itself or anything else as this may cause
damage to the robot.
2.   This is only a quick start guide to show how easy it is to use a UR
robot. It assumes a harmless environment and a very careful user.
Do not increase the speed or acceleration above the default values.
Always conduct a risk assessment before placing the robot into
operation.
WARNING
Keep your head and torso outside the reach (workspace) of the robot. Do
not place fingers where they can be caught.
UR3e
107
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 107

8.2.1. Run Tab
Description
The Run tab allows you to do simple operations and monitor the state of your robot. You
can load, play, pause and stop a program, as well as monitor variables. The Run Tab is
most useful when the program is created and the robot is ready for operation.
Program
The Program pane displays the name and status of the current program.
To load a new
program
1.   In the Program pane, tap Load Program.
2.   Select your desired program from the list.
3.   Tap Open to load the new program.
The variables, if present, are displayed when you play the program.
Variables
The Variables pane displays the list of variables used by programs to store and update
values during runtime.
•   Program variables belong to programs.
•   Installation variables belong to installations that can be shared among different
programs. The same installation can be used with multiple programs.
All program variables and installation variables in your program are displayed in the
Variables pane as a list showing the Name, Value and Description of the variable.
User Manual
108
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 108

Variable
descriptions
You can add information to your variables by adding variable descriptions in the
Description column. You can use the variable descriptions to convey the purpose of the
variable and/or the meaning of its value to operators using the Run tab screen and/or
other programmers.
Variable descriptions (if used) can be up to 120 characters, displayed in the Description
column of the variables list on the Run tab screen and the Variables tab screen.
Favorite
variables
You can display selected variables by using the Show only favorite variables option.
To show favorite variables
1.   Under Variables, check the Show only favorite variables box.
2.   Check Show only favorite variables again to show all variables.
You cannot designate favorite variables in the Run Tab, you can only display them.
Designating favorite variables depends on the variable type.
To designate
favorite
program
variables
1.   In the Header, tap Program.
The variables are listed under Variable Setup.
2.   Select the desired variables.
3.   Check the Favorite variable box.
4.   Tap Run to return to your variable display.
To designate
favorite
installation
variables
1.   In the Header, tap Installation.
2.   Under General, select Variables.
The variables are listed under Installation Variables.
3.   Select the desired variables.
4.   Check the Favorite variable box.
5.   Tap Run to return to your variable display.
Collapse/expand
the Description
column
A variable description spans multiple lines to fit the width of the Description column if
necessary. You can also collapse and expand the Description column by using the
buttons shown below.
To collapse/expand the Description column
1.   Tap
to collapse the Description column.
2.   Tap
to expand the Description column.
here
UR3e
109
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 109

Collapsed
Description
column
Expanded
Description
column
User Manual
110
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 110

Control
The Control pane allows you to control the running program. You can play and stop, or pause
and resume a program, using the buttons listed in the table below:
•   The Play button, Pause button and the Resume Button are combined.
•   The Play button changes to Pause when the program is running.
•   The Pause button changes to Resume.
Button
Function
Play
To play a program
1.   Under Control, tap Play to start running a
program from the beginning.
Resume
To resume a paused program
1.   Tap Resume to continue running the
paused program.
Stop
To stop a program
1.   Tap Stop to stop the running program
You cannot resume a stopped program.
You can tap Play to restart the program.
Pause
To pause a program
1.   Tap Pause to pause a program at a specific
point.
You can resume a paused program.
UR3e
111
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 111

8.2.2. Move Robot into Position
Description
Access the Move Robot into Position screen when the Robot Arm must move to a
particular start position before running a program, or when the Robot Arm is moving to a
waypoint while modifying a program.
In cases where the Move Robot into Position screen cannnot move the Robot Arm to
the program start position, it moves to the first waypoint in the program tree.
The Robot Arm can move to an incorrect pose if:
•   The TCP, feature pose or waypoint pose of the first movement is altered during
program execution before the first move is executed.
•   The first waypoint is inside an If or Switch program tree node.
Accessing the
Move Robot
into Position
Screen
1.   Tap the Run tab in the header.
2.   In the Footer, tap Play to access the Move Robot into Position screen.
3.   Follow the on-screen instructions to interact with the animation and the real robot.
Move robot to
Hold down Move robot to: to move the Robot Arm to a start position. The animated Robot
Arm displayed on-screen shows the desired movement about to be performed.
NOTICE
Collision can damage the robot or other equipment. Compare the
animation with the position of the real Robot Arm to ensure the Robot Arm
can safely perform the movement without colliding with any obstacles.
Manual
Tap Manual to access the Move screen where the Robot Arm can be moved by using the
Move Tool arrows and/or configuring Tool Position and Joint Position coordinates.
User Manual
112
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 112

8.2.3. Using the Program Tab
Description
The Program tab is the where you create and edit robot programs. There are two main
areas:
•   The left side contains the program nodes you can add to your robot program.
You can use the Basic, Advanced and Template dropdowns to the very left.
•   The right side contains the configuration of the program nodes you can add to
your program.
You can use Command, Graphics and Variables options.
UR3e
113
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 113

Program Tree
The program tree is built as you add program nodes to your program.
You can use the Command tab to configure the functionality of the added program nodes.
Adding
program
nodes
•   You cannot run an empty program tree or a program containing incorrectly
configured program nodes.
•   Incorrectly configured programs nodes are higlighted in yellow.
•   Correctly configured program nodes are highlighted in white.
User Manual
114
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 114

Program
Execution
Indication
You can follow the the flow of a long robot program by looking at the active program node.
When the program is running, the program node currently being executed is indicated by a
small icon next to that node.
The path of execution is highlighted with blue arrow
.
Tapping the
icon at the corner of the program allows it to track the command being
executed
Search
Button
You can also search for a specific command/program node. This is useful when you have a
long program with many different program nodes.
UR3e
115
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 115

8.2.4. Program Tree Toolbar
Description
You can work with the program nodes that have been added to the program tree by
using the icons in the bottom of the program tree.
Icons in
the
Program
Tree
toolbar
Use the toolbar at the base of the Program Tree to modify the Program Tree.
Undo & Redo
&
undo and redo changes to commands.
Move Up &
Move Down
&
changes the position of a node.
Cut
cuts a node and allows it to be used for other
actions (e.g., paste it on other place on the
Program Tree).
Copy
copies a node and allows it to be used for other
actions (e.g., paste it on other place on the
Program Tree).
Paste
pastes a node that was previously cut or copied.
Delete
removes a node from the Program Tree.
Suppress
suppresses specific nodes on the Program Tree.
Search Button
search in the Program Tree. Tap the
icon
to exit search.
User Manual
116
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 116

8.2.5. Using Selected Program Nodes
Description
You can start your robot program from any program node in the program tree. This is
useful when you are testing your program.
When the robot is in Manual Mode you can allow a program to start from a selected node
or you can start the entire program from the beginning.
Play From
Selection
The Play button in the Footer provides options for how to start the program.
In the image below, the Play button is selected and Play from Selection is displayed.
•   You can start a program only from a node in the robot Program tree. The Play from
Selection stops if a program cannot be run from a selected node.
The program also stops and displays an error message if an unassigned variable in
encountered while playing a program from selected node.
•   You can use Play from Selection in a subprogram. The program execution halts
when the subprogram ends.
•   You cannot use Play from Selection with a thread because threads always start from
the beginning.
To play a
program from
a selected
node
1.   In the Program tree, select a node.
2.   In the Footer, tap Play.
3.   Select Play from Selection to run a program from a node in the program tree.
Example
You can start a stopped program again from a specific node.
UR3e
117
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 117

8.2.6. Using Basic Program Nodes
Description
Basic program nodes are used to create simple robot applications. Some basic program
nodes are also used to organize your robot program and create comments in your robot
program. This can be quite useful, if it is large robot program.
8.2.7. Basic Program Nodes: Move
Description
The Move command allows the robot to move from point A to point B.
How the robot moves is important to the task the robot is performing.
When you add a Move to your program tree, the Move pane appears to the right of the
screen.
The Movecommand controls the robot's motion via waypoints.
Waypoints are automatically added when you add Move commands to a program.
You can also use Moves to set acceleration and speed for the robot arm's movement
between waypoints.
The robot moves using four Move commands:
•   MoveJ
•   MoveL
•   MoveP
•   MoveCircle
User Manual
118
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 118

MoveJ
The MoveJ command creates a movement from point A to point B that is optimal for the
robot.
The movement may not be a direct line between A and B, but optimal for the start position of
the joints and the end position of the joints.
Add a MoveJ
command
1.   In your robot program, select the place where you wish to add a Move.
2.   Under Basic, tap Move to add a waypoint to the robot program together with a Move
node.
3.   Select the move node.
4.   Select the MoveJ in the drop-down menu.
Detail
MoveJ makes movements that are calculated in the robot arm joint space. Joints are
controlled to finish their movements at the same time. This movement type results in a
curved path for the tool to follow. The shared parameters that apply to this movement type
are the maximum joint speed and joint acceleration, specified in deg/s and deg/s 2 ,
respectively. If it is desired to have the robot arm move fast between waypoints,
disregarding the path of the tool between those waypoints, this movement type is the
preferable choice.
MoveL
The MoveL command creates a movement that is a direct line from point A and point B.
Add a MoveL
command
1.   In your Robot Program, select the place where you wish to add a Move.
2.   Under Basic, tap Move to add a waypoint to the robot program together with a Move
node.
3.   Select the move node.
4.   Select the MoveL from the drop-down menu.
Detail
MoveL moves the Tool Center Point (TCP) linearly between waypoints. This means that
each joint performs a more complicated motion to keep the tool on a straight line path. The
shared parameters that can be set for this movement type are the desired tool speed and
tool acceleration specified in mm/s and mm/s 2 , respectively, and also a feature.
MoveP
The MoveP command creates a movement with a constant speed between the waypoints.
Blend between waypoints is enabled to ensure constant speed.
Add a MoveP
command
1.   In your Robot Program, select the place where you wish to add a Move.
2.   Under Basic, tap Move to add a waypoint to the robot program together with the
Move node.
3.   Select the move node.
4.   Select the MoveP from the drop-down menu.
UR3e
119
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 119

Detail
MoveP moves the tool linearly with constant speed with circular blends, and is intended for
some process operations, like gluing or dispensing. The size of the blend radius is by
default a shared value between all the waypoints. A smaller value will make the path turn
sharper whereas a higher value will make the path smoother. While the robot arm is moving
through the waypoints with constant speed, the robot control box cannot wait for either an
I/O operation or an operator action. Doing so might stop the robot arm’s motion, or cause a
robot stop.
MoveCircle
The MoveCircle command creates a circular movement, by creating a half circle.
You can only add CircleMove via a MoveP command.
Add a
MoveCircle
command
1.   In your Robot Program, select the place where you wish to add a Move.
2.   Under Basic, tap Move.
A waypoint is added to the robot program together with the Move node.
3.   Select the move node.
4.   Select the MoveP from the drop-down menu.
5.   Tap Add circle move
6.   Select the orientation mode.
Detail
The robot starts the circular movement from its current position, or start point, and moves
through a ViaPoint specified on the circular arc, to an EndPoint that completes the circular
movement.
A mode is used to calculate tool orientation, through the circular arc.
The mode can be:
•   Fixed: only the start point is used to define the tool orientation.
•   Unconstrained: the start point transforms to the EndPoint to define tool orientation.
User Manual
120
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 120

8.2.8. Basic Program Nodes: Waypoints
Description
Waypoints are one of the most central parts of a robot program, telling the robot arm
where to go one movement at a time.
Add
Waypoints
A waypoint accompanies a Move, so adding a Move is required for the first waypoint.
Add a
waypoint to a
robot program
1.   In your Robot Program, select the place where you wish to add a Move.
2.   Under Basic, tap Move.
A waypoint is added to the robot program together with the Move node.
UR3e
121
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 121

Add additional
waypoints to a
Move or
Waypoint
1.   In your Robot Program, select a Move node or Waypoint node.
2.   Under Basic, tap Waypoint.
The additional waypoint is added in the Move node. This waypoint is part of the
Move command.
The additional waypoint is added under the waypoint that you selected in the robot
program.
Detail
Using a waypoint means applying the taught relationship between the feature and the TCP
from the Move command. The relationship between the feature and the TCP, applied to the
current selected feature, achieves the desired TCP location. The robot calculates how to
position the arm to allow the current active TCP to reach the desired TCP position.
User Manual
122
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 122

8.2.9. Using the Move Tab
Description
Use the Move Tab screen to move (jog) the robot arm directly, either by
translating/rotating the robot tool, or by moving robot joints individually.
To use the
Move Tool
arrows
Hold down any of the Move Tool arrows to move the robot arm in the corresponding direction.
•   The Translate arrows (upper) move the tool flange in the direction indicated.
•   The Rotate arrows (lower) change the orientation of the tool in the indicated direction.
The rotation point is the Tool Center Point (TCP), i.e.the point at the end of the robot
arm that gives a characteristic point on the tool. The TCP is shown as a small blue ball.
Robot
If the current position of the TCP approaches a safety plane, a trigger plane, or the orientation
of robot tool is near the tool orientation boundary limit , a 3D representation of the proximate
boundary limit is shown. The visualization of boundary limits is disabled during program
execution.
Safety planes display in yellow and black with an arrow indicating which side of the plane, the
robot TCP is allowed to be positioned.
Trigger planes display in blue and green with an arrow indicating the side of the plane, where
the Normal mode limits are active.
The tool orientation boundary limit is visualized with a spherical cone together with a vector
indicating the current orientation of the robot tool. The inside of the cone represents the
allowed area for the tool orientation (vector).
When the robot TCP is no longer in proximity of the limit, the 3D representation disappears. If
the TCP is in violation or very close to violating a boundary limit, the visualization of the limit
turns red.
UR3e
123
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 123

Feature
Under Feature, you can define how to control the robot arm relative to View, Base or Tool
features. For the best feel for controlling the robot arm you can select the View feature, then
use Rotate arrows to change the viewing angle of the 3D image to match your view of the
real robot arm.
Active TCP
In the Robot field, under Active TCP, the name of the current active Tool Center Point (TCP)
is displayed.
Home
The Home button accesses the Move Robot into Position screen, where you can hold down
the Auto button to move robot into position previously defined under Installation. The Home
button’s default setting returns the Robo Arm to an upright position .
Freedrive
The on-screen Freedrive button allows the Robot Arm to be pulled into desired
positions/poses.
Align
The Align button allows the Z axis of the active TCP to align to a selected feature.
Tool Position
The text boxes display the full coordinate values of the TCP relative to the selected feature.
You can configure several named TCPs. You can also tap Edit pose to access the Pose
Editor screen.
Joint
Position
The Joint Position field allows you to directly control individual joints. Each joint moves
along a default joint limit range from   −360 ∘ to   + 360 ∘ , defined by a horizontal bar. Once the
limit is reached you cannot move a joint any further. You can configure joints with a position
range different from the default, this new range is indicated with red zone inside the
horizontal bar.
User Manual
124
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 124

Using
Freedrive in
the Move tab
The Freedrive button shall only be used in applications if allowed by the risk assessment.
WARNING
Failure to correctly configure the mounting setting can result in unwanted
robot arm movement when you use the Freedrive button.
•   Payload settings and robot mounting settings shall be set correctly
before using Freedrive.
•   All personnel shall remain outside the reach of the robot arm, when
Freedrive is in use.
WARNING
Failure to correctly configure the installation settings, can increase the risk
of the robot arm falling during Freedrive, due to payload errors.
•   Verify the installation settings are correct (e.g. Robot mounting
angle, payload mass and payload center of gravity offset) . Save
and load the installation files along with the program.
•   Save and load the installation files along with the program.
8.2.10. Pose Editor
Description
Once you access the Pose Editor screen, you can precisely configure a target joint
positions, or a target pose (position and orientation) for the TCP. Note: This screen is
offline and does not control the Robot Arm directly.
UR3e
125
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 125

Robot
The 3D image shows the current Robot Arm position. The shadow shows the Robot Arm
target position controlled by the specified values on the screen. Press the magnifying glass
icons to zoom in/out or drag a finger across it to change the view.
If the specified target position of the robot TCP is close to a safety or trigger plane, or the
orientation of robot tool is near the tool orientation boundary limit, a 3D representation of the
proximate boundary limit is shown. Safety planes are visualized in yellow and black with a
small arrow representing the plane normal, which indicates the side of the plane on which the
robot TCP is allowed to be positioned. Trigger planes are displayed in blue and green and a
small arrow pointing to the side of the plane, where the Normal mode limits are active. The
tool orientation boundary limit is visualized with a spherical cone together with a vector
indicating the current orientation of the robot tool. The inside of the cone represents the
allowed area for the tool orientation (vector). When the target robot TCP is no longer in
proximity of the limit, the 3D representation disappears. If the target TCP is in violation or very
close to violating a boundary limit, the visualization of the limit turns red.
Feature and
Tool
Position
The active TCP and coordinate values of the selected feature are displayed. The X, Y, Z
coordinates specify tool position. The RX, RY, RZ coordinates specify orientation. For
further information about configuring several named TCPs.
Use the drop down menu above the RX, RY and RZ boxes to choose the orientation
representation type:
•   Rotation Vector  [rad]  The orientation is given as a rotation vector. The length of the
axis is the angle to be rotated in radians, and the vector itself gives the axis about
which to rotate. This is the default setting.
•   Rotation Vector  [ ∘ ]  The orientation is given as a rotation vector, where the length of
the vector is the angle to be rotated in degrees.
•   RPY  [rad] Roll, pitch and yaw (RPY) angles, where the angles are in radians. The
RPY-rotation matrix (X, Y’, Z” rotation) is given by:
R rpy (γ, β, α) = R Z (α)  ⋅ R Y (β)  ⋅ R X (γ)
•   RPY  [ ∘ ] Roll, pitch and yaw (RPY) angles, where angles are in degrees.
You can tap the values to edit the coordinates. You can also tap the + or - buttons to the right
of a box to add/subtract an amount to/from the current value. Or you can hold down a button
to directly increase/decrease the value.
Joint
Positions
Individual joint positions are specified directly. Each joint position can have Joint Limit range
from   −360 ∘ to   + 360 ∘ . You can configure Joint Positions as follows:
•   Tap the joint position to edit the values.
•   Tap the + or - buttons to the right of a box to add or subtract an amount to/from the
current value.
•   Hold down a button to directly increase/decrease the value.
OK Button
If you activate this screen from the Move screen, tap the OK button to return to the Move
screen. The Robot Arm moves to the specified target. If the last specified value was a tool
coordinate, the Robot Arm moves to the target position using movement type MoveL; or it
uses movement type MoveJ if a joint position was specified last.
User Manual
126
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 126

Cancel
Button
The Cancel button exits the screen discarding all changes.
UR3e
127
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 127

8.3. Safety-related Functions and Interfaces
Description
Universal Robots robots are equipped with a range of built-in safety functions as well as
safety I/O, digital and analog control signals to or from the electrical interface, to connect
to other machines and additional protective devices. Each safety function and I/O is
constructed according to EN ISO13849-1 with Performance Level d (PLd) using a
category 3 architecture.
WARNING
The use of safety configuration parameters different from those
determined as necessary for risk reduction, can result in hazards that
are not reasonably eliminated, or risks that are not sufficiently reduced.
•   Ensure tools and grippers are connected correctly to avoid
hazards due to interruption of power.
WARNING: ELECTRICITY
Programmer and/or wiring errors can cause the voltage to change from
12V to 24V leading to fire damage to equipment.
•   Verify the use of 12V and proceed with caution.
NOTICE
•   The use and configuration of safety functions and interfaces must follow
the risk assessment procedures for each robot application.
•   The stopping time should be taken into account as part of the application
risk assessment
•   If the robot detects a fault or violation in the safety system (e.g. if one of
the wires in the Emergency Stop circuit is cut or a safety limit is
exceeded), then a Stop Category 0 is initiated.
NOTICE
The end effector is not protected by the UR safety system. The functioning of the
end effector and/or connection cable is not monitored
User Manual
128
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 128

8.3.1. Configurable Safety Functions
Description
Universal Robots robot safety functions, as listed in the table below, are in the robot but
are meant to control the robot system i.e. the robot with its attached tool/end effector.
The robot safety functions are used to reduce robot system risks determined by the risk
assessment. Positions and speeds are relative to the base of the robot.
Safety
Function
Description
Joint Position
Limit
Sets upper and lower limits for the allowed joint positions.
Joint Speed
Limit
Sets an upper limit for joint speed.
Safety
Planes
Defines planes, in space, that limit robot position. Safety planes limit
either the tool/end effector alone or both the tool/end effector and the
elbow.
Tool
Orientation
Defines allowable orientation limits for the tool.
Speed Limit
Limits maximum robot speed. The speed is limited at the elbow, at the
tool/end effector flange, and at the center of the user-defined tool/end
effector positions.
Force Limit
Limits maximum force exerted by the robot tool/end effector and elbow
in clamping situations. The force is limited at the tool/end effector,
elbow flange and center of the user-defined tool/end effector positions.
Momentum
Limit
Limits maximum momentum of the robot.
Power Limit
Limits mechanical work performed by the robot.
Stopping
Time Limit
Limits maximum time the robot uses for stopping after a robot stop is
initiated. 1
Stopping
Distance
Limit
Limits maximum distance travelled by the robot after a robot stop is
initiated.
Safety
Function
When performing the application risk assessment, it is necessary to take into account the
motion of the robot after a stop has been initiated. In order to ease this process, the safety
functions Stopping Time Limit and Stopping Distance Limit can be used.
These safety functions dynamically reduces the speed of the robot motion such that it can
always be stopped within the limits. The joint position limits, the safety planes and the
tool/end effector orientation limits take the expected stopping distance travel into account
i.e. the robot motion will slow down before the limit is reached.
The functional safety can be summarized as:
1 Robot stop was previously known as "Protective stop".
UR3e
129
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 129

Safety Function
Accuracy
Performance Level
Category
Emergency Stop
–
d
3
Safeguard Stop
–
d
3
Joint Position Limit
5 °
d
3
Joint Speed Limit
1.15 °/s
d
3
Safety Planes
40 mm
d
3
Tool Orientation
3 °
d
3
Speed Limit
50 mm/s
d
3
Force Limit
25 N
d
3
Momentum Limit
3 kg m/s
d
3
Power Limit
10 W
d
3
Stopping Time Limit
50 ms
d
3
Stopping Distance Limit
40 mm
d
3
Safe Home
1.7 °
d
3
Warnings
CAUTION
Failure to configure the maximum speed limit can result in hazardous
situations.
•   If the robot is used in manual hand-guiding applications with linear
movements, the speed limit must be set to maximum 250 mm/s for
the tool/end effector and elbow unless a risk assessment shows
that higher speeds are acceptable. This will prevent fast
movements of the robot elbow near singularities.
NOTICE
There are two exceptions to the force limiting function that are important
when designing an application.
As the robot stretches out, the knee-joint effect can give high forces in the
radial direction (away from the base) at low speeds. Similarly, the short
leverage arm, when the tool/end effector is close to the base and moving
around the base, can cause high forces at low speeds.
8.3.2. Safety Functions
User Manual
130
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 130

Description
The safety system acts by monitoring if any of the safety limits are exceeded or if an
Emergency Stop or a Safeguard Stop is initiated.
The reactions of the safety system are:
Trigger
Reaction
Emergency Stop
Stop Category 1
Safeguard Stop
Stop Category 2
3PE Stop (if a 3-Position Enabling device is connected)
Stop Category 2
Limit Violation
Stop Category 0
Fault Detection
Stop Category 0
NOTICE
If the safety system detects any fault or violation, all safety outputs re-
set to low.
UR3e
131
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 131

8.3.3. Safety Parameter Set
Description
The safety system has the following set of configurable safety parameters:
•   Normal
•   Reduced
Normal and
Reduced
You can set up the safety limits for each set of safety parameters, creating distinct
configurations for normal, or higher settings, and reduced. The reduced configuration is
active when the tool/end effector is positioned on the reduced side of a Trigger Reduced
Plane, or when the reduced configuration is externally triggered by a safety input.
Using a plane to trigger the Reduced configuration: When the robot arm moves from the
side of the trigger plane configured with reduced safety parameters, to the side that is
configured with normal safety parameters, there is a 20 mm area around the trigger plane
where both normal and reduced limits are allowed. This area around the trigger plane
prevents nuisance safety stops when the robot is exactly at the limit.
Using an input to trigger the Reduced configuration: When a safety input starts, or stops,
the reduced configuration, up to 500 ms can elapse before the new limit values become
active. This can happen in either of the following circumstances:
•   Switching from the reduced configuration to normal
•   Switching from the normal configuration to reduced
The robot arm adapts to the new safety limits within the 500 ms.
User Manual
132
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 132

Recovery
When a safety limit is exceeded, the safety system must be restarted. For example, if a joint
position limit is outside a safety limit, at start-up, Recovery is activated.
You cannot run programs for the robot when recovery is activated, but the robot arm can be
manually moved back within limits using Freedrive, or by using the Move tab in PolyScope.
The safety limits for Recovery are:
Safety Function
Limit
Joint Speed Limit
30 °/s
Speed Limit
250 mm/s
Force Limit
100 N
Momentum Limit
10 kg m/s
Power Limit
80 W
The safety system issues a Stop Category 0 if a violation of these limits appears.
WARNING
Failure to use caution when moving the robot arm in recovery mode can
lead to hazardous situations.
•   Use caution when moving the robot arm back within the limits, as
limits for the joint positions, the safety planes, and the tool/end
effector orientation are all disabled in recovery mode.
UR3e
133
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 133

8.4. Software Safety Configuration
Description
This section covers how to access the robot safety settings. It is made up of items that
help you set up the robot Safety Configuration.
WARNING
Before you configure your robot safety settings, your integrator must
conduct a risk assessment to guarantee the safety of personnel and
equipment around the robot. A risk assessment is an evaluation of all
work procedures throughout the robot lifetime, conducted in order to
apply correct safety configuration settings. You must set the following
in accordance with the risk assessment.
1.   The integrator must prevent unauthorized persons from
changing the safety configuration e.g. installing password
protection.
2.   Use and configuration of the safety-related functions and
interfaces for a specific robot application.
3.   Safety configuration settings for set-up and teaching before the
robot arm is powered on for the first time.
4.   All safety configuration settings accessible on this screen and
sub-tabs.
5.   The integrator must ensure that all changes to the safety
configuration settings comply with the risk assessment.
User Manual
134
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 134

Accessing
Software
Safety
Settings
Safety Settings are password protected and can only be configured once a password is set
and subsequently used.
To access the software safety settings
1.   In your PolyScope header, tap the Installation icon.
2.   In the Side Menu on the left of the screen, tap Safety.
3.   Observe that the Robot Limits screen displays, but settings are inaccessible.
4.   If a Safety password was previously set, enter the password and press Unlock to
make settings accessible. Note: Once Safety settings are unlocked, all settings are
now active.
5.   Press Lock tab or navigate away from the Safety menu to lock all Safety item
settings again.
UR3e
135
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 135

8.4.1. Setting a Software Safety Password
Description
You must set a password to Unlock all safety settings that make up your Safety
Configuration. If no safety password is applied, you are prompted to set it up.
To set a
Software
Safety
password
You can tap the Lock tab to lock all Safety settings again or simply navigate to a screen
outside of the Safety menu.
1.   In your PolyScope header right corner, press the Hamburger menu and select
Settings.
2.   On the left of the screen, in the blue menu, press Password and select Safety.
3.   In New password, type a password.
4.   Now, in Confirm new password, type the same password and press Apply.
5.   In the bottom left of the blue menu, press Exit to return to previous screen.
User Manual
136
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 136

8.4.2. Changing the Software Safety Configuration
Description
Changes to the Safety Configuration settings must comply with the risk assessment
conducted by the integrator.
Recommended
procedure for the
integrator:
To change the safety configuration
1.   Verify that changes comply with the risk assessment conducted by the integrator.
2.   Adjust safety settings to the appropriate level defined by the risk assessment
conducted by the integrator.
3.   Verify that the settings are applied.
4.   Place following text in the operators’ manuals:
Before working near the robot, make sure that the safety configuration is as expected.
This can be verified e.g. by inspecting the Safety Checksum in the top right corner of
PolyScope for any changes.
UR3e
137
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 137

8.4.3. Applying a New Software Safety Configuration
Description
The robot is powered off while you make changes to the configuration.
Your changes only take effect after you tap the Apply button.
The robot cannot be powered on again until you select Apply and Restart to visually
inspect your robot Safety Configuration which, for safety reasons, is displayed in SI Units
in a popup.
You can select Revert Changes to return to the previous configuration. When your
visual inspection is complete you can select Confirm Safety Configuration and the
changes are automatically saved as part of the current robot installation.
Safety Checksum
Description
The Safety Checksum icon displays your applied robot safety configuration.
It could be four or eight digits.
A four-digit Checksum should be read from top to bottom and left to right, while an eight-
digit Checksum is read left to right, top row first. Different text and/or colors indicate
changes to the applied safety configuration.
The Safety Checksum changes if you change the Safety Functions settings, because
the Safety Checksum is only generated by the safety settings.
You must apply your changes to the Safety Configuration for the Safety Checksum to
reflect your changes.
User Manual
138
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 138

UR3e
139
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 139

8.4.4. Safety Configuration without Teach Pendant
Description
You can use the robot without attaching the Teach Pendant. Removing the Teach
Pendant requires defining another Emergency Stop source. You must specify if the
Teach Pendant is attached to avoid triggering a safety violation.
CAUTION
If the Teach Pendant is detached or disconnected from the robot, the
Emergency Stop button is no longer active. You must remove the
Teach Pendant from the vicinity of the robot.
To safely
remove the
Teach
Pendant
The robot can be used without PolyScope as the programming interface.
To configure the robot without a Teach Pendant
1.   In the Header tap Installation.
2.   In the Side Menu on left tap Safety and select Hardware.
3.   Input Safety password and Unlock the screen.
4.   Deselect Teach Pendant to use robot without PolyScope interface.
5.   Press Save and restart to implement changes.
User Manual
140
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 140

8.4.5. Software Safety Modes
Description
Under normal conditions, i.e. when no robot stop is in effect, the safety system operates
in a Safety Mode associated with a set of safety limits   1 :
•   Normal mode is the safety mode that is active by default
•   Reduced mode is active when the robot Tool Center Point (TCP) is positioned
beyond a Trigger Reduced mode plane, or when triggered using a configurable
input.
•   Recovery mode activates when a safety limit from the active limit set is violated,
the robot arm performs a Stop Category 0. If an active safety limit, such as a joint
position limit or a safety boundary, is violated already when the robot arm is
powered on, it starts up in Recovery mode. This makes it possible to move the
robot arm back within the safety limits. While in Recovery mode, the movement of
the robot arm is restricted by a fixed limit that you cannot customize.
WARNING
Limits for joint position, tool position and tool orientation are disabled
in Recovery mode, so take caution when moving the robot arm back
within the limits.
The menu of the Safety Configuration screen enables the user to define separate sets of
safety limits for Normal and Reduced mode. For the tool and joints, Reduced mode limits
for speed and momentum are required to be more restrictive than their Normal mode
counterparts.
To Switch
Modes: PolyScope
1.   In the Header, select the profile icon.
•   Automatic indicates the operational mode of the robot is set to
Automatic.
•   Manual indicates the operational mode of the robot is set to Manual.
Using the
Dashboard
Server
1.   Connect to the Dashboard server.
2.   Use the Set Operational Mode commands.
•   Set Operational Mode Automatic
•   Set Operational Mode Manual
•   Clear Operational Mode
8.4.6. Software Safety Limits
1 Robot stop was previously known as "Protective Stop" for Universal Robots robots.
UR3e
141
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 141

Description
In the Safety Configuration the safety system limits are specified. The Safety System
receives the values from the input fields and detects any violation if any these values are
exceeded. The robot controller attempts to prevent any violations by making a robot stop
or by reducing the speed.
Robot Limits
Description
Robot Limits restrict general robot movements. The Robot Limits screen has two
configuration options: Factory Presets and Custom.
Factory
Presets
Factory Presets is where you can use the slider to select a predefined safety setting . The
values in the table are updated to reflect the preset values ranging from Most Restricted to
Least Restricted
NOTICE
Slider values are only suggestions and do not substitute a proper risk
assessment.
User Manual
142
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 142

Custom
Custom is where you can set Limits on how the robot functions and monitor the associated
Tolerance.
Power
Limits maximum mechanical work produced by the robot in the
environment. This limit considers the payload a part of the robot and
not of the environment.
Momentum
Limits maximum robot momentum.
Stopping
Time
Limits maximum time it takes the robot to stop e.g. when an
emergency stop is activated.
Stopping
Distance
Limits maximum distance the robot tool or elbow can travel while
stopping.
NOTICE
Restricting stopping time and distance affect overall
robot speed. For example, if stopping time is set to
300 ms, the maximum robot speed is limited
allowing the robot to stop within 300 ms.
Tool Speed
Limits maximum robot tool speed.
Tool Force
Limits maximum force that the robot tool exerts on the environment to
prevent clamping situations.
Elbow Speed
Limits maximum robot elbow speed.
Elbow Force
Limits maximum force that the elbow exerts on the environment to
prevent clamping situations.
UR3e
143
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 143

The tool speed and force are limited at the tool flange and the center of the two user-defined tool
positions.
NOTICE
You can switch back to Factory Presets for all robot limits to reset to their
default settings.
Joint Limits
Description
Joint limits allow you to restrict individual robot joint movements in joint space i.e. joint
rotational position and joint rotational speed. Joint limiting can also be called software
based axis limiting. The joint limit options are: Maximum speed and Position range.
User Manual
144
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 144

Wrist 3
position
range
When using cables attached to the robot, you must first disable the Unrestricted Range for
Wrist 3 checkbox to avoid cable tension and robot stops.
1.   Maximum speed is where you define the maximum angular velocity for each joint.
2.   Position range is where you define the position range for each joint. Again, the input
fields for Reduced mode are disabled if there is no safety plane or configurable input
set to trigger it. This limit enables safety-rated soft axis limiting of the robot.
UR3e
145
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 145

8.4.7. Safe Home Position
Description
Safe Home is a return position defined by using the user-defined Home Position.
Safe Home I/Os are active when the Robot Arm is in the Safe Home Position and a Safe
Home I/O is defined.
The Robot Arm is in the Safe Home Position if the joint positions are at the specified joint
angles or a multiple of 360 degrees thereof.
The Safe Home Safety Output is active when the robot is standing still at the Safe Home
Position.
Syncing
from Home
To sync from Home
1.   In the Header, tap Installation.
2.   In the Side Menu on the left of the screen, tap Safety and select Safe Home.
3.   Under Safe Home, tap Sync from Home.
4.   Tap Apply and in the dialog box that appears, select Apply and restart.
Safe Home
Output
The Safe Home Position must be defined before the Safe Home Output.
Defining
Safe Home
Output
To define Safe Home Output
1.   In the Header, tap Installation.
2.   In the Side Menu on the left of the screen, under Safety, select I/O.
3.   On the I/O screen in the Output Signal, under Function Assignment, in drop-down
menu, select Safe Home.
4.   Tap Apply and in the dialog box that appears, select Apply and restart.
User Manual
146
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 146

Editing Safe
Home
To edit Safe Home
Editing Home does not automatically modify a previously defined Safe Home position. While
these values are out of sync, Home program node is undefined.
1.   In the Header, tap Installation.
2.   In the Side Menu on the left of the screen, under General, select Home.
3.   Tap Edit Position and set the new robot arm position and tap OK.
4.   In the Side Menu, under Safety, select Safe Home. You need a Safety password to
Unlock the Safety Settings.
5.   Under Safe Home, tap Sync from Home
UR3e
147
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 147

8.5.   Software Safety Restrictions
Description
NOTICE
Configuring planes is entirely based on features. We recommend you
create and name all features before editing the safety configuration, as
the robot is powered off once the Safety Tab has been unlocked and
moving the robot will be impossible.
Safety planes restrict robot workspace. You can define up to eight safety planes,
restricting the robot tool and elbow. You can also restrict elbow movement for each
safety plane and disable by deselecting the checkbox. Before configuring safety planes,
you must define a feature in the robot installation. The feature can then be copied into the
safety plane screen and configured.
WARNING
Defining safety planes only limits the defined Tool spheres and elbow,
not the overall limit for the robot arm. This means that specifying a
safety plane, does not guarantee that other parts of the robot arm will
obey this restriction.
Saf
ety
Pla
nes
Mod
es
You can configure each plane with restrictive Modes using the icons listed below.
Disabled
The safety plane is never active in this state.
Normal
When the safety system is in Normal mode, a normal plane is
active and it acts as a strict limit on the position.
Reduced
When the safety system is in Reduced mode, a reduced mode
plane is active and it acts as a strict limit on the position.
Normal & Reduced
When the safety system is either in Normal or Reduced mode,
a normal and reduced mode plane is active and acts as a strict
limit on the position.
Trigger Reduced
Mode
The safety plane causes the safety system to switch to
Reduced mode if the robot Tool or Elbow is positioned beyond
it.
Show
Pressing this icon hides or shows the safety plane in the
graphics pane.
Delete
Deletes the created safety plane. There is no undo/redo
action. If a plane is deleted in error, it must be remade.
Rename
Pressing this icon allows you to rename the plane.
User Manual
148
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 148

Configuring
safety planes
1.   In your PolyScope header, tap Installation.
2.   In the Side Menu on the left of the screen, tap Safety and select Planes.
3.   On the top right of the screen, in the Planes field, tap Add plane.
4.   On the bottom right of the screen, in the Properties field, set up Name, Copy
Feature and Restrictions.
Copy
Feature
In Copy Feature, only Undefined and Base are available. You can reset a configured safety
plane by selecting Undefined
If the copied feature is modified in the Features screen, a warning icon appears to the right of
the Copy Feature text. This indicates that the feature is out of sync i.e. the information in the
properties card is not updated to reflect the modifications that may have been made to the
Feature.
UR3e
149
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 149

Col
or
Cod
es
Gray
Plane is configured but disabled (A)
Yellow & Black
Normal Plane (B)
Blue & Green
Trigger Plane (C)
Black Arrow
The side of the plane the tool and/or elbow is allowed to be on (For
Normal Planes)
Green Arrow
The side of the plane the tool and/or elbow is allowed to be on (For
Trigger Planes)
Gray Arrow
The side of the plane the tool and/or elbow is allowed to be on (For
Disabled Planes)
User Manual
150
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 150

Elbow
Restriction
You can enable Restrict Elbow to prevent robot elbow joint from passing through any of
your defined planes. Disable Restrict Elbow for elbow to pass through planes.
The diameter of the ball that restricts the elbow is different for each size of robot.
UR3e
0.1 m
UR5e
0.13 m
UR10e / UR16e
0.15 m
UR20 / UR30
0.19 m
The information about the specific radius can be found in the urcontrol.conf file on the robot
under the section [Elbow].
Tool Flange
Restriction
Restricting the tool flange prevents the tool flange and the attached tool from crossing a
safety plane. When you restrict the tool flange, the unrestricted area is the area inside of
the safety plane, where the tool flange can operate normally.
The tool flange cannot cross the restricted area, outside of the safety plane.
Removing the restriction allows the tool flange to go beyond the safety plane, to the
restricted area, while the attached tool remains inside of the safety plane.
You can remove the tool flange restriction when working with a large tool off-set. This will
allow extra distance for the tool to move.
Restricting the tool flange requires the creation of a plane feature. The plane feature is
used to set up a safety plane later in the safety settings.
UR3e
151
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 151

Adding a
plane feature
example
Displacement offsets the plane in either the positive or negative direction along the plane
normal (Z-axis of the plane feature).
Deselect the checkbox for the Elbow and the Tool Flange so they do not trigger the safety
plane. The Elbow can remain checked as needed by your application.
The unrestricted tool flange can cross a safety plane, even when no tool is defined.
If no tool is added, a warning on the Tool Position button prompts you to correctly define the
tool.
When working with an unrestricted tool flange and a defined tool, it is ensured that the
dangerous part of the tool can't go above and/or beyond certain area. The unrestricted tool
flange can be used for any application where safety planes are needed, like Welding or
Assembly.
User Manual
152
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 152

Tool flange
restriction
example
In this example, an X-Y-plane is created with an offset of 300mm along the positive Z-axis
with reference to the base feature.
The Z-axis of the plane can be thought of as “pointing” towards the restricted area.
If the safety plane is needed on e.g., the surface of a table, rotate the plane 3.142 rad or
180° around either the X- or Y-axis so the restricted area is under the table.
(TIP: Change the display of rotation from “Rotation Vector [rad]” to “RPY [°]”)
If needed it is possible to offset the plane in either positive or negative Z-direction later in
the safety settings.
When satisfied with the position of the plane, tap OK.
UR3e
153
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 153

8.5.1. Tool Direction Restriction
Description
The Tool Direction screen can be used to restrict the angle in which the tool is pointing.
The limit is defined by a cone that has a fixed orientation with respect to the robot arm
Base. As the robot arm moves around, tool direction is restricted so it remains within the
defined cone. The default direction of the tool coincides with the Z-axis of the tool output
flange. It can be customized by specifying tilt and pan angles.
Before configuring the limit, you must define a point or plane in the robot installation. The
feature can then be copied and its Z axis used as the center of the cone defining the limit.
NOTICE
Configuration of the tool direction is based on features. We recommend
you create desired feature(s) before editing the safety configuration, as
once the Safety Tab has been unlocked, the robot arm powers off
making it impossible to define new features.
User Manual
154
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 154

Limit
Prope
rties
The Tool Direction limit has three configurable properties:
1.   Cone center: You can select a point or plane feature from the drop-down menu, to define
the center of the cone. The Z axis of the selected feature is used as the direction around
which the cone is centred.
2.   Cone angle: You can define how many degrees the robot is allowed to deviate from center.
Disabled Tool direction limit
Never active
Normal Tool direction limit
Active only when safety system is in Normal mode
Reduced Tool direction limit
Active only when the safety system is in Reduced mode
Normal & Reduced Tool
direction limit
Active when the safety system is in Normal mode as
well as when it is in Reduced mode.
You can reset the values to default or undo the Tool Direction configuration by setting the copy
feature back to "Undefined".
Tool
Prope
rties
By default, the tool points in the same direction as the Z axis of the tool output flange. This can be
modified by specifying two angles:
•   Tilt angle: How much to tilt the Z axis of the output flange towards the X axis of the output
flange
•   Pan angle: How much to rotate the tilted Z axis around the original output flange Z axis.
Alternatively, the Z axis of an existing TCP can be copied by selecting that TCP from the drop-down
menu.
UR3e
155
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 155

8.5.2. Tool Position Restriction
Description
The Tool Position screen enables more controlled restriction of tools and/or accessories
placed on the end of the robot arm.
•   Robot is where you can visualize your modifications.
•   Tool is where you can define and configure a tool up to two tools.
•   Tool_1 is the default tool defined with values x=0.0, y= 0.0, z=0.0 and radius=0.0.
These values represent the robot tool flange.
Under Copy TCP, you can also select Tool Flange and cause the tool values to go back
to 0.
A default sphere is defined at the tool flange.
User Manual
156
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 156

User
defined
tools
For the user defined tools, the user can change:
•   Radius to change the radius of the tool sphere. The radius is considered when using
safety planes. When a point in the sphere passes a reduced mode trigger plane, the
robot switches to Reduced mode. The safety system prevents any point on the sphere
from passing a safety plane.
•   Position to change the position of the tool with respect to the tool flange of the robot.
The position is considered for the safety functions for tool speed, tool force, stopping
distance and safety planes.
You can use an existing Tool Center Point as a base for defining new tool positions. A copy of
the existing TCP, predefined in General menu, in TCP screen, can be accessed in Tool
Position menu, in Copy TCP drop-down list.
When you edit or adjust the values in the Edit Position input fields, the name of the TCP
visible in the drop down menu changes to custom, indicating that there is a difference
between the copied TCP and the actual limit input. The original TCP is still available in the
drop down list and can be selected again to change the values back to the original position.
The selection in the copy TCP drop down menu does not affect the tool name.
Once you apply your Tool Position screen changes, if you try to modify the copied TCP in the
TCP configuration screen, a warning icon appears to the right of the Copy TCP text. This
indicates that the TCP is out of sync i.e. the information in the properties field is not updated
to reflect modifications that may have been made to the TCP. The TCP can be synced by
pressing the sync icon.
The TCP does not have to be synced in order to define and use a tool successfully.
You can rename the tool by pressing the pencil tab next to the displayed tool name. You can
also determine the Radius with an allowed range of 0-300 mm. The limit appears in the
graphics pane as either a point or a sphere depending on radius size.
UR3e
157
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 157

Tool Position
Warning
You must set a Tool Position within the safety settings, for the safety plane to trigger
correctly when the tool TCP approaches the safety plane.
The warning remains on the Tool Position if:
•   You fail to add a new tool under Tool Flange.
To configure the tool position
1.   In the Header tap Installation.
2.   On the left side of the screen, under Safety, tap Tool Position.
3.   On the right side of the screen, select Add Tool.
•   The newly added tool has a default name: Tool_x.
4.   Tap the edit button to rename Tool_x to something more identifiable.
5.   Edit the Radius and Position to match that of the tool you are currently using, or use
the Copy TCP drop-down and choose a TCP from the General>TCP settings if such
is defined.
User Manual
158
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 158

Tool Position
Warning
example
In this example, a Radius of 0.8mm is set and the TCP position to XYZ [20, 0, 400] in
millimeters respectively. Optionally you can choose to ”Copy TCP” by using the drop-down
menu if one has already been set in the ->General/TCP settings. Once the Apply is tapped
in the bottom right corner of the screen, you are DONE.
The warning on the Tool Position button indicates a tool is not added under Tool Flange.
Tool Position button without the warning indicates a tool (other than the Tool Flange) is
added.
UR3e
159
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 159

9. Cybersecurity Threat Assessment
Description
This section provides information to help you strengthen the robot against potential
cybersecurity threats. It outlines requirements for addressing cybersecurity threats and
provides security hardening guidelines.
9.1. General Cybersecurity
Description
Connecting a Universal Robots robot to a network can introduce cybersecurity risks.
These risks can be mitigated by using qualified personnel and implementing specific
measures for protecting the robot's cybersecurity.
Implementing cybersecurity measures requires conducting a cybersecurity threat
assessment.
The purpose is to:
•   Identify threats
•   Define trust zones and conduits
•   Specify the requirements of each component in the application
WARNING
Failure to conduct a cybersecurity risk assessment can place the robot
at risk.
•   The integrator or competent, qualified personnel shall conduct a
cybersecurity risk assessment.
NOTICE
Only competent, qualified personnel shall be responsible for
determining the need for specific cybersecurity measures and for
providing the required cybersecurity measures.
9.2. Cybersecurity Requirements
Description
Configuring your network and securing your robot requires you to implement the threat
measures for cybersecurity.
Follow all the requirements before you start configure your network, then verify the robot
setup is secure.
User Manual
160
UR3e
9. Cybersecurity Threat Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 160

Cybersecurity
•   Operating personnel must have a thorough understanding of general
cybersecurity principles and advanced technologies as used in the UR robot.
•   Physical security measures must be implemented to allow only authorized
personnel physical access to the robot.
•   There must be adequate control of all access points. For example: locks on
doors, badge systems, physical access control in general.
WARNING
Connecting the robot to a network that is not properly secured, can
introduce security and safety risks.
•   Only connect your robot to a trusted and properly secured
network.
Network
configuration
requirements
•   Only trusted devices are to be connected to the local network.
•   There must be no inbound connections from adjacent networks to the robot.
•   Outgoing connections from the robot are to be restricted to allow the smallest
relevant set of specific ports, protocols and addresses.
•   Only URCaps and magic scripts from trusted partners can be used, and only
after verifying their authenticity and integrity
Robot setup
security
requirements
•   Change the default password to a new, strong password.
•   Disable the "Magic Files" when not actively used (PolyScope 5).
•   Disable SSH access when not needed. Prefer key-based authentication over
password-based authentication
•   Set the robot firewall to the most restrictive usable settings and disable all
unused interfaces and services, close ports and restrict IP addresses
UR3e
161
User Manual
9. Cybersecurity Threat Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 161

9.3. Cybersecurity Hardening Guidelines
Description
Although PolyScope includes many features for keeping the network connection secure,
you can harden security by observing to following guidelines:
•   Before connecting your robot to any network, always change the default password
to a strong password.
NOTICE
You cannot retrieve or reset a forgotten or lost password.
•   Store all passwords securely.
•   Use the built-in settings to restrict the network access to the robot as much as
possible.
•   Some communication interfaces have no method of authenticating and encrypting
communication. This is a security risk. Consider appropriate mitigating measures,
based on your cybersecurity threat assessment.
•   SSH tunneling (Local port forwarding) must be used to access robot interfaces
from other devices if the connection crosses the trust zone boundary.
•   Remove sensitive data from the robot before it is decommissioned. Pay particular
attention to the URCaps and data in the program folder.
•   To ensure secure removal of highly sensitive data, securely wipe or destroy
the SD card.
User Manual
162
UR3e
9. Cybersecurity Threat Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 162

9.4. Passwords
Description
You can create and manage different types of password in PolyScope. An initial
password must be set to access the full safety settings. The following password types
are described below:
•   Administrator
•   Operational
9.5. Password Settings
To set a
Password
You must set a password to Unlock all safety settings that make up your Safety
Configuration. If no safety password is applied, you are prompted to set it up.
1.   In your PolyScope header right corner, press the Hamburger menu and select
Settings.
2.   On the left of the screen, in the blue menu, press Password and select Safety.
3.   In New password, type a password.
4.   Now, in Confirm new password, type the same password and press Apply.
5.   In the bottom left of the blue menu, press Exit to return to previous screen.
You can press the Lock tab to lock all Safety settings again or simply navigate to a screen
outside of the Safety menu.
UR3e
163
User Manual
9. Cybersecurity Threat Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 163

9.6. Administrator Password
Description
Use the Administrator (Admin) Password to change the security configuration of the
system, including network access.
The Admin password is equal to the password used for the root user account on the
Linux system running on the robot, which may be needed in some network use cases
such as SSH or SFTP.
WARNING
You cannot recover a lost Admin password.
•   Take the appropriate steps to ensure your admin password is
not lost.
To set the
Admin
Password
1.   In the Header, tap the Hamburger menu icon and select Settings.
2.   Under Password, tap Admin.
3.   Under Current password, put in the default password: easybot.
4.   Under New password, create a new password.
Creating a strong, secret password obtains the best security for your system.
5.   Under Confirm new password, repeat your new password.
6.   Tap Apply to confirm your password change.
Safety
The Safety password prevents unauthorized modification of the Safety settings.
User Manual
164
UR3e
9. Cybersecurity Threat Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 164

9.7. Operational Password
Description
The Operational Mode Password, or mode password, creates two different user roles on
PolyScope:
•   Manual
•   Automatic
When the mode password is set, programs and installations can only be created and
edited in Manual mode. Automatic mode only allows the operator to load pre-made
programs . Once a password has been set, a new Mode icon appears in the Header.
Switching operational modes, from Manual to Automatic and from Automatic to Manual,
causes PolyScope to prompt for the new password.
To set the
Mode
Password
1.   In the Header, tap the Hamburger menu icon and select Settings.
2.   Under Password, tap Mode.
3.   Under New password, create a new password.
Creating a strong, secret password obtains the best security for your system.
4.   Under Confirm new password, repeat your new password.
5.   Tap Apply to confirm your password change.
UR3e
165
User Manual
9. Cybersecurity Threat Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 165

10. Communication Networks
User Manual
166
UR3e
10. Communication Networks
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 166

11. Fieldbus
Description
You can use the Fieldbus options to define and configure the family of industrial
computer network protocols used for real-time distributed control accepted by
PolyScope:
•   MODBUS
•   Ethernet/IP
•   PROFINET
•   PROFIsafe
UR3e
167
User Manual
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 167

11.1. MODBUS
Description
Here, the MODBUS client (master) signals can be set up. Connections to MODBUS
servers (or slaves) on specified IP addresses can be created with input/output signals
(registers or digital). Each signal has a unique name so it can be used in programs.
Refresh
Push this button to refresh all MODBUS connections. Refreshing disconnects all modbus
units, and connects them back again. All statistics are cleared.
Add unit
Push this button to add a new MODBUS unit.
Delete unit
Push this button to delete the MODBUS unit and all signals on that unit.
Set unit IP
Here the IP address of the MODBUS unit is shown. Press the button to change it.
Sequential
mode
Available only when Show Advanced Options selected. Selecting this checkbox forces the
modbus client to wait for a response before sending the next request. This mode is
required by some fieldbus units. Turning this option on may help when there are multiple
signals, and increasing request frequency results in signal disconnects.
The actual signal frequency may be lower than requested when multiple signals are
defined in sequential mode. Actual signal frequency can be observed in signal statistics.
The signal indicator turns yellow if the actual signal frequency is less than half of the value
selected from the Frequency drop-down list.
Add signal
Push this button to add a signal to the corresponding MODBUS unit.
Delete
signal
Push this button to delete a MODBUS signal from the corresponding MODBUS unit.
User Manual
168
UR3e
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 168

Set
sig
nal
type
Use this drop down menu to choose the signal type.
Available types are:
Digital input
A digital input (coil) is a one-bit quantity which is read from the
MODBUS unit on the coil specified in the address field of the signal.
Function code 0x02 (Read Discrete Inputs) is used.
Digital output
A digital output (coil) is a one-bit quantity which can be set to either
high or low. Before the value of this output has been set by the user,
the value is read from the remote MODBUS unit. This means that
function code 0x01 (Read Coils) is used. When the output has been
set by a robot program or by pressing the set signal value button,
the function code 0x05 (Write Single Coil) is used onwards.
Register input
A register input is a 16-bit quantity read from the address specified
in the address field. The function code 0x04 (Read Input Registers)
is used.
Register output
A register output is a 16-bit quantity which can be set by the user.
Before the value of the register has been set, the value of it is read
from the remote MODBUS unit. This means that function code 0x03
(Read Holding Registers) is used. When the output has been set by
a robot program or by specifying a signal value in the set signal
value field, function code 0x06 (Write Single Register) is used to set
the value on the remote MODBUS unit.
Set signal
address
This field shows the address on the remote MODBUS server. Use the on-screen keypad to
choose a different address. Valid addresses depends on the manufacturer and configuration
of the remote MODBUS unit.
Set signal
name
Using the on-screen keyboard, the user can give the signal a name. This name is used when
the signal is used in programs.
Signal
value
Here, the current value of the signal is shown. For register signals, the value is expressed as
an unsigned integer. For output signals, the desired signal value can be set using the button.
Again, for a register output, the value to write to the unit must be supplied as an unsigned
integer.
UR3e
169
User Manual
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 169

Signal
connec
tivity
status
This icon shows whether the signal can be properly read/written (green), or if the unit responds
unexpected or is not reachable (gray). If a MODBUS exception response is received, the response
code is displayed. The MODBUS-TCP Exception responses are:
E1
ILLEGAL FUNCTION (0x01) The function code received in the
query is not an allowable action for the server (or slave).
E2
ILLEGAL DATA ADDRESS (0x02) The function code received in
the query is not an allowable action for the server (or slave), check
that the entered signal address corresponds to the setup of the
remote MODBUS server.
E3
ILLEGAL DATA VALUE (0x03) A value contained in the query data
field is not an allowable value for server (or slave), check that the
entered signal value is valid for the specified address on the remote
MODBUS server.
E4
SLAVE DEVICE FAILURE (0x04) An unrecoverable error occurred
while the server (or slave) was attempting to perform the requested
action.
E5
ACKNOWLEDGE (0x05) Specialized use in conjunction with
programming commands sent to the remote MODBUS unit.
E6
SLAVE DEVICE BUSY (0x06) Specialized use in conjunction with
programming commands sent to the remote MODBUS unit, the
slave (server) is not able to respond now.
Show
Advanced
Options
This check box shows/hides the advanced options for each signal.
User Manual
170
UR3e
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 170

Advan
ced
Optio
ns
Update Frequency
This menu can be used to change the update frequency of the
signal. This means the frequency with which requests are sent to
the remote MODBUS unit for either reading or writing the signal
value. When the frequency is set to 0, then modbus requests are
initiated on demand using a modbus_get_signal_status,
modbus_set_output_register, and modbus_set_output_signal
script functions.
Slave Address
This text field can be used to set a specific slave address for the
requests corresponding to a specific signal. The value must be in
the range 0-255 both included, and the default is 255. If you
change this value, it is recommended to consult the manual of
the remote MODBUS device to verify its functionality when
changing slave address.
Reconnect count
Number of times TCP connection was closed, and connected
again.
Connection status
TCP connection status.
Response time [ms]
Time between modbus request sent, and response received -
this is updated only when communication is active.
Modbus packet errors
Number of received packets that contained errors (i.e. invalid
length, missing data, TCP socket error).
Timeouts
Number of modbus requests that didn’t get response.
Requests failed
Number of packets that could not be sent due to invalid socket
status.
Actual freq.
The average frequency of client (master) signal status updates.
This value is recalculated each time the signal receives a
response from the server (or slave).
All counters count up to 65535, and then wrap back to 0.
UR3e
171
User Manual
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 171

11.2. EtherNet/IP
Description
EtherNet/IP is a network protocol that enables the connection of the robot to an industrial
EtherNet/IP Scanner Device.
If the connection is enabled, you can select the action that occurs when a program loses
EtherNet/IP Scanner Device connection.
Those actions are:
None
PolyScope ignores the loss of EtherNet/IP connection and the
program continues to run.
Pause
PolyScope pauses the current program. The program resumes from
where it stopped.
Stop
PolyScope stops the current program.
11.3. PROFINET
Description
The PROFINET network protocol enables or disables the connection of the robot to an
industrial PROFINET IO-Controller.
If the connection is enabled, you can select the action that occurs when a program loses
PROFINET IO-Controller connection.
Those actions are:
None
PolyScope ignores the loss of PROFINET connection and the
program continues to run.
Pause
PolyScope pauses the current program. The program resumes from
where it stopped.
Stop
PolyScope stops the current program.
If the PROFINET engineering tool (e.g. TIA portal) emits a DCP Flash signal to the robot's
PROFINET or PROFIsafe device, a popup in PolyScope is displayed.
User Manual
172
UR3e
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 172

11.4. PROFIsafe
Description
The PROFIsafe network protocol (implemented as version 2.6.1) allows the robot to
communicate with a safety PLC according to ISO 13849, Cat 3 PLd requirements. The
robot transmits safety state information to a safety PLC, then receives information to
trigger safety related functions, such as: emergency stop or enter reduced mode.
The PROFIsafe interface provides a safe, network-based alternative to connecting wires
to the safety IO pins of the robot control box.
PROFIsafe is only available on robots that have an enabling license, which you can
obtain by contacting your local sales representative, once obtained, the license can be
downloaded on  myUR .
Please refer to  Robot Registration and URCap License files  for information regarding
robot registration and license activation.
Adva
nced
Optio
ns
A control message received from the safety PLC contains the information in the table below.
Signal
Description
E-Stop by system
Asserts the system e-stop.
Safeguard stop
Asserts the safeguard stop.
Reset safeguard stop
Resets safeguard stop state (on low-to-high transition in
automatic mode) if the safeguard stop input is cleared
beforehand.
Safeguard stop auto
Asserts safeguard stop if the robot is operating in Automatic
mode.
Safeguard stop auto shall only be used when a 3-Position
Enabling (3PE) Device is configured. If no 3PE Device is
configured, the safeguard stop auto acts as a normal
safeguard stop input.
Reset safeguard stop
auto
Resets safeguard stop auto state (on low-to-high transition
when in automatic mode) if safeguard stop auto inputs are
cleared beforehand.
Reduced mode
Activates the Reduced mode safety limits.
Operational mode
Activates either manual or automatic operational mode. If the
safety configuration "Operational mode selection via
PROFIsafe" is disabled, this field shall be omitted from the
PROFIsafe control message.
UR3e
173
User Manual
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 173

Advan
ced
Optio
ns
A status message sent to the safety PLC contains the information in the table below.
Signal
Description
Stop, cat. 0
Robot is performing, or it has completed, a safety stop of category
0; A hard stop by immediate removal of power to the arm and the
motors.
Stop, cat. 1
Robot is performing, or it has completed, a safety stop of category
1; A controlled stop after which the motors are left in a power off
state with brakes engaged.
Stop, cat. 2
Robot is performing, or it has completed, a safety stop of category
2; A controlled stop after which the motors are left in a power on
state.
Violation
Robot is stopped because the safety system failed to comply with
the safety limits currently defined.
Fault
Robot is stopped because of an unexpected exceptional error in
the safety system.
E-stop by system
Robot is stopped because of one of the following conditions:
•   a safety PLC connected via PROFIsafe has asserted
system level e-stop.
•   an IMMI module connected to the control box has asserted
a system level e-stop.
•   a unit connected to the system e-stop configurable safety
input of the control box has asserted system level e-stop.
E-stop by robot
The robot is stopped because of one of the following conditions:
•   The e-stop button of the teach pendant is pressed.
•   An e-stop button connected to the robot e-stop non-
configurable safety input of the control box is pressed.
Safeguard stop
The robot is stopped due to one of the following conditions:
•   A safety PLC connected via PROFIsafe has asserted the
safeguard stop.
•   A unit connected to the safeguard stop non-configurable
input of the control box has asserted the safeguard stop.
•   A unit connected to the safeguard stop configurable safety
input of the control box has asserted the safeguard stop.
The signal follows the safeguard reset semantics. A configured
safeguard stop reset functionality shall be used to reset this
signal.
PROFIsafe implies use of the safeguard reset functionality.
User Manual
174
UR3e
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 174

Advan
ced
Optio
ns
Signal
Description
Safeguard stop auto
The robot is stopped because it is operating in Automatic mode
and because of one of the following conditions:
•   A safety PLC connected via PROFIsafe has asserted
safeguard stop auto.
•   A unit connected to a safeguard stop auto configurable
safety input of the control box has asserted safeguard
stop auto.
The signal follows the safeguard reset semantics. A configured
safeguard stop reset functionality shall be used to reset this
signal
PROFIsafe implies use of the safeguard reset functionality
3PE stop
Robot is stopped because it is operating in Manual mode and
because of one of the following conditions:
•   You are using a 3PE TP and none of the buttons are in the
middle position.
•   A 3-position enabling device connected to a configurable
safety input of the control box has asserted the 3PE stop.
Operational mode
Indication of the current operational mode of the robot.
This mode can be: Disabled (0), Automatic (1), or Manual (2).
Reduced mode
Reduced mode safety limits are currently active.
Active limit set
The active set of safety limits.
This can be: Normal (0), Reduced (1), or Recovery (2).
Robot moving
Robot is moving. If any joint moves at a velocity of 0.02 rad/s or
higher the robot is considered in motion.
Safe home position
Robot is at rest (robot not moving), and in the position defined as
the Safe Home Position.
UR3e
175
User Manual
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 175

Configuring
PROFIsafe
Configuring PROFIsafe relates to programming the safety PLC, but requires minimal robot
setup.
1.   Connect the robot to a trusted network that accesses a safety compliant PLC.
2.   On PolyScope, in the Header, tap Installation.
3.   Tap Safety, select PROFIsafe and configure as needed.
Enabling
PROFIsafe
1.   Enter the robot safety password and tap Unlock.
2.   Use the switch button to enable PROFIsafe.
3.   Enter a source address and destination address into the corresponding boxes.
These addresses are arbitrary numbers used by the robot and the safety PLC to
identify each other.
4.   You can switch the Control Operational Mode to the ON position if you want
PROFIsafe to control the robot operational mode.
Only one source can control the operational mode of the robot. Therefore other
sources of mode selection are disabled when operational mode selection via
PROFIsafe is enabled.
The robot is now setup to communicate with a safety PLC.
You cannot release the robot's brakes if the PLC is not responding or if it is misconfigured.
11.5. UR Connect
User Manual
176
UR3e
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 176

Description
The URCap UR Connect comes pre-installed with 5.19 PolyScope 5 software.
To ensure correct operation, there are some additional prerequisites that must be
installed.
Please refer to the URCap documentation for additional information.
UR Connect Installation and User Guide
Go here for more information about the product:  https://www.universal-
robots.com/optimization-services/ur-connect/
Install UR
Connect
To install the UR Connect, please follow the steps below:
1.   Go to the Installation tab.
2.   Hit the tab URCaps in the left side of the screen.
3.   Hit Install to start installation the prerequisites.
4.   Follow the steps on the screen.
Activate UR
Connect
The UR Connect URCap needs to be paired with myUR to send data to MyUR.
Please refer to the MyUR documentation on the UR Connect for further information.
UR Connect
URCap
Update
You can find the URCaps on the Installation Tab.
1.   Go to the Installation tab.
2.   Hit the tab URCaps in the left side of the screen.
3.   Hit the button Check for Updates in the bottom right corner.
4.   You can now download, dismiss or delay the update.
a.   If you delay or dismiss, the update will only refresh when there is a new
version.
5.   Follow the update steps.
6.   Restart PolyScope when the update is complete.
NOTICE
You can still update UR Connect even if it is NOT installed.
UR3e
177
User Manual
11. Fieldbus
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 177

12. Emergency Events
Description
Follow the instructions here to handle emergency situations, such as activating the
emergency stop using the red push-button. This section also describes how to manually
move the system without power.
12.1. Emergency Stop
Description
The Emergency Stop or E-stop is the red push-button located on the Teach Pendant.
Press the emergency stop push-button to stop all robot motion. Activating the
emergency stop push-button causes a stop category one (IEC 60204-1).
Emergency stops are not safeguards (ISO 12100).
Emergency stops are complementary protective measures that do not prevent injury.
The risk assessment of the robot application determines if additional emergency stop
push-buttons are required. The emergency stop function and the actuating device must
comply with ISO 13850.
After an emergency stop is actuated, the push-button latches in that setting. As such,
each time an emergency stop is activated, it must be manually reset at the push-button
that initiated the stop.
Before resetting the emergency stop push-button, you must visually identify and assess
the reason the E-stop was first activated. Visual assessment of all the equipment in the
application is required. Once the problem is solved, reset the emergency stop push-
button.
To reset the emergency stop push-button
1.   Hold the push-button and twist clockwise until the latching disengages.
You should feel when the latching is disengaged, indicating the push-button is
reset.
2.   Verify the situation and whether to reset the emergency stop.
3.   After resetting the emergency stop, restore power to the robot and resume
operation.
User Manual
178
UR3e
12. Emergency Events
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 178

12.2. Movement Without Drive Power
Description
In the unlikely event of an emergency, when powering the robot is either impossible or
unwanted, you can use forced back-driving to move the robot arm.
To perform forced back-driving you must push, or pull, the robot arm hard to move the
joint. Each joint brake has a friction clutch that enables movement during high forced
torque.
Performing forced back-driving requires high force and cannot be performed by one
person alone. In clamping situations, two or more people are required to do the forced
back-driving. In some situations, two or more people are required to disassemble the
robot arm.
WARNING
Risks due to an unsupported robot arm breaking or falling can cause
injury or death.
•   Support the robot arm before removing power.
NOTICE
Moving the robot arm manually is intended for emergency and service
purposes only. Unnecessary moving of the robot arm can lead to
property damage.
•   Do not move the joint more than 160 degrees, to ensure the
robot can find its original physical position.
•   Do not move any joint more than necessary.
UR3e
179
User Manual
12. Emergency Events
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 179

12.3. Modes
Description
You access and activate different modes using Teach Pendant or the Dashboard Server.
If an external mode selector is integrated, it control the modes - not PolyScope or the
Dashboard Server.
Automatic Mode Once activated, the robot can only execute a program of pre-defined
tasks. You cannot modify or save programs and installations.
Manual Mode Once activated, you can program the robot. You can modify and save
programs and installations.
The speeds used in Manual Mode must be limited to prevent injury. When the robot is
operating in Manual Mode, a person could be positioned within reach of the robot. The
speed must be limited to the value that is appropriate for the application risk assessment.
WARNING
Injury can occur if the speed used, while the robot is operating in
Manual Mode, is too high.
High Speed Manual Mode can be used. It allows both tool speed and elbow speed to
temporarily exceed 250 mm/s, while a hold-to-run is used.
Hold-to-run is performed by continuous contact with the Speed Slider.
The robot performs a Safeguard Stop in Manual mode, if a Three-Position Enabling
Device is configured, and either released (not pressed) or it is fully compressed.
Switching between Automatic mode to Manual mode requires the Three-Position
Enabling Device to be fully released and pressed again to allow the robot to move.
When using High Speed Manual Mode, use safety joint limits or safety planes to restrict
the robot’s moving space.
Mode
switching
Operational mode
Manual
Automatic
Freedrive
x
*
Move robot with arrows on Move Tab
x
*
Edit & save program & installation
x
Execute Programs
Reduced
speed**
*
Start program from selected node
x
*Only when no Three-Position Enabling Device is configured.
** If a Three-Position Enabling Device is configured, the robot operates at Manual
Reduced Speed unless High Speed Manual Mode is activated.
User Manual
180
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 180

WARNING
•   Any suspended safeguards must be returned to full functionality before
selecting Automatic Mode.
•   Wherever possible, Manual Mode shall only be used with all persons
located outside the safeguarded space.
•   If an external mode selector is used, it must be placed outside the
safeguarded space.
•   No-one is to enter, or be within, the safeguarded space in Automatic
Mode, unless safeguarding is used or the collaborative application is
validated for power and force limiting (PFL).
Three-
Position
Enabling
Device
When a Three-Position Enabling Device is used and the robot is in Manual Mode,
movement requires pressing the Three-Position Enabling Device to the center-on
position. The Three-Position Enabling Device has no effect in Automatic Mode.
NOTICE
•   Some UR robot sizes might not be equipped with a Three-
Position Enabling Device. If the risk assessment requires the
enabling device, a 3PE Teach Pendant must be used.
A 3PE Teach Pendant (3PE TP) is recommended for programming. If another person can
be within the safeguarded space when in Manual Mode, an additional device can be
integrated and configured for the additional person's use.
UR3e
181
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 181

12.3.1. Recovery Mode
Description
When a safety limit is exceeded, Recovery Mode is automatically activated, allowing the
robot arm to be moved. Recovery Mode is a type of   Manual Mode .
You cannot run robot programs when Recovery Mode is active.
During Recovery Mode, the robot arm is moved to be within joint limits, using either
Freedrive or the Move tab in PolyScope.
Safety limits
of Recovery
Mode
Safety Function
Limit
Joint Speed Limit
30 °/s
Speed Limit
250 mm/s
Force Limit
100 N
Momentum Limit
10 kg m/s
Power Limit
80 W
The safety system issues a Stop Category 0 if a violation of these limits appears.
WARNING
Failure to use caution when moving the robot arm in recovery mode can
lead to hazardous situations.
•   Use caution when moving the robot arm back within the limits, as
limits for the joint positions, the safety planes, and the tool/end
effector orientation are all disabled in recovery.
12.3.2. Backdrive
Description
Backdrive is a Manual Mode used to force specific joints to a desired position without
releasing all brakes in the robot arm.
This is sometimes necessary if the robot arm is close to collision and the vibrations that
accompany a full restart are not desired.
The robot joints feel heavy to move, while Backdrive is in use.
You can use any of the following sequences to enable Backdrive:
•   3PE Teach Pendant
•   3PE device/switch
•   Freedrive on robot
User Manual
182
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 182

3PE Teach
Pendant
To use the 3PE TP button to backdrive the robot arm.
1.   On the Initialize screen, tap ON to start the power up sequence.
2.   When the robot state is Teach Pendant 3PE Stop, light-press, then light-press-
and-hold, the 3PE TP button.
The robot state changes to Backdrive.
3.   Now you can apply significant pressure to release the brake in a desired joint to
move the robot arm.
As long as light-press is maintained on the 3PE button, Backdrive is enabled,
allowing the arm to move.
3PE
device/switch
To use a 3PE device/switch to backdrive the robot arm.
1.   On the Initialize screen, tap ON to start the power up sequence.
2.   When the robot state is Teach Pendant 3PE Stop, light-press, then light-press-
and-hold, the 3PE TP button.
The robot state changes to System 3PE Stop.
3.   Press and hold the 3PE device/switch.
The robot state changes to Backdrive.
4.   Now you can apply significant pressure to release the brake in a desired joint to
move the robot arm.
As long as the hold is maintained on both the 3PE device/switch and the 3PE TP
button, Backdrive is enabled, allowing the arm to move.
Freedrive on
robot
To use Freedrive on robot to backdrive the robot arm.
1.   On the Initialize screen, tap ON to start the power up sequence.
2.   When the robot state is Teach Pendant 3PE Stop, press and hold the Freedrive
on robot.
The robot state changes to Backdrive.
3.   Now you can apply significant pressure to release the brake in a desired joint to
move the robot arm.
As long as the hold is maintained on the Freedrive on robot, Backdrive is enabled,
allowing the arm to move.
UR3e
183
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 183

Backdrive Inspection
Description
If the robot is close to colliding with something, you can use Backdrive to move the robot
arm to a safe position before initializing.
3PE Teach Pendant
User Manual
184
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 184

Enable
Backdrive
1.   Press ON to enable power. Status changes to Robot Active
2.   Press and hold Freedrive. Status changes to Backdrive
3.   Move robot as in Freedrive mode. Joint brakes are released where needed once
the Freedrive button is activated.
NOTICE
In Backdrive Mode the robot is “heavy” to move around.
MANDATORY ACTION
You must test Backdrive mode on all joints.
Safety
settings
Verify the robot safety settings comply with the robot installation risk assessment.
Additional
safety inputs
and outputs
are still
functioning
Check which safety inputs and outputs are active and that they can be triggered via
PolyScope or external devices.
UR3e
185
User Manual
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 185

User Manual
186
UR3e
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 186

13. Transportation
Description
Only transport the robot in its original packaging. Save the packaging material in a dry
place if you want to move the robot later.
When moving the robot from its packaging to the installation space, hold both tubes of
the robot arm at the same time. Hold the robot in place until all mounting bolts are
securely tightened at the base of the robot.
Lift the Control Box by its handle.
WARNING
Incorrect lifting techniques, or using improper lifting equipment, can lead to
injury.
•   Avoid overloading your back or other body parts when lifting the
equipment.
•   Use proper lifting equipment.
•   All regional and national lifting guidelines shall be followed.
•   Make sure to mount the robot according to the instructions in Mechanical
Interface.
NOTICE
If the robot is attached to 3rd-party application / installation during transport,
please refer to the following:
•   Transporting the robot without its original packaging will void all warranties
from Universal Robots A/S.
•   If the robot is transported attached to a 3rd-party application / installation,
follow the recommendations for transporting the robot without the original
transport packaging.
Disclaimer
Universal Robots cannot be held responsible for any damage caused by transportation of
the equipment.
You can see the recommendations for transportation without packaging at:  universal-
robots.com/manuals
UR3e
187
User Manual
13. Transportation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 187

Description
Universal Robots always recommends transporting the robot in its original packaging.
These recommendations are written to reduce unwanted vibrations in joints and brake
systems and reduce joint rotation.
If the robot is transported without its original packaging, then please refer to the following
guidelines:
•   Fold the robot as much as possible – do not transport the robot in the singularity
position.
•   Move the center of gravity in the robot as close to the base as possible.
•   Secure each tube to a solid surface on two different points on the tube.
•   Secure any attached end effector rigidly in 3 axes.
Transport
Fold the robot as much as possible.
Do not transport extended.
(singularity position)
Secure the tubes to a solid surface.
Secure attached end effector in 3 axes.
13.1. Teach Pendant Storage
Description
The operator needs to have a clear understanding about what the e-Stop on the Teach
Pendant affects when pressed. For example there can be confusion with a multi-robot
installation. It should be made clear if the e-Stop on the Teach Pendant stops the whole
installation or only its connected robot.
If there could be confusion, store the Teach Pendant such that the e-Stop button is not
visible or usable.
User Manual
188
UR3e
13. Transportation
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 188

14. Maintenance and Repair
Description
Any maintenance work, inspection and calibration shall be conducted in compliance with
all safety instructions in this manual and according to local requirements.
Repair work shall be done by Universal Robots. Client designated, trained individuals
can do repair work, provided they follow the Service Manual.
Safety for
Maintenance
After maintenance and repair work, checks must be done to ensure the required safety
level. Checks must adhere to valid national or regional work safety regulations. The
correct functioning of all safety functions shall also be tested.
The purpose of maintenance and repair work is to ensure that the system is kept
operational or, in the event of a fault, to return the system to an operational state. Repair
work includes troubleshooting in addition to the actual repair itself.
When working on the robot arm or control box, you must observe the procedures and
warnings below.
WARNING
Failure to adhere to any of the safety practices, listed below, can result in injury.
•   Unplug the main power cable from the bottom of the Control Box to ensure
that it is completely unpowered. Power off any other source of energy
connected to the robot arm or Control Box. Take necessary precautions to
prevent other persons from powering on the system during the repair
period.
•   Check the earth connection before re-powering the system.
•   Observe ESD regulations when parts of the robot arm or Control Box are
disassembled.
•   Prevent water and dust from entering the robot arm or Control Box.
WARNING: ELECTRICITY
Disassembling the Control Box power supply too quickly after switching off, can
result in injury due to electrical hazards.
•   Avoid disassembling the power supply inside the Control Box, as high
voltages (up to 600 V) can be present inside these power supplies for
several hours after the Control Box has been switched off.
14.1. Testing Stopping Performance
UR3e
189
User Manual
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 189

Description
Test periodically to determine if stopping performance is degraded. Increased stopping
times can require safeguarding to be modified, possibly with changes to the installation.
If stop time and/or stop distance safety functions are used and are the basis of the risk
reduction strategy, no monitoring or testing of stopping performance is required. The
robot does continuous monitoring.
14.2. Robot Arm Cleaning and Inspection
Description
As part of regular maintenance the robot arm can be cleaned, in accordance with the
recommendations in this manual and local requirements.
Cleaning
Methods
To address the dust, dirt, or oil on the robot arm and/or Teach Pendant, simply use a cloth
alongside one of the cleaning agents provided below.
Surface Preparation: Before applying the below solutions, surfaces may need to be
prepared by removing any loose dirt or debris.
Cleaning agents:
•   Water
•   70% Isopropyl alcohol
•   10% Ethanol alcohol
•   10% Naphtha (Use to remove grease.)
Application: The solution is typically applied to the surface that needs cleaning using a
spray bottle, brush, sponge, or cloth. It can be applied directly or diluted further depending
on the level of contamination and the type of surface being cleaned.
Agitation: For stubborn stains or heavily soiled areas, the solution may be agitated using
a brush, scrubber, or other mechanical means to help loosen the contaminants.
Dwell Time: If necessary, the solution is allowed to dwell on the surface for a up to 5
minutes to penetrate and dissolve the contaminants effectively.
Rinsing: After the dwell time, the surface is typically rinsed thoroughly with water to
remove the dissolved contaminants and any remaining cleaning agent residue. It's
essential to ensure thorough rinsing to prevent any residue from causing damage or
posing a safety hazard.
Drying: Finally, the cleaned surface may be left to air dry or dried using towels.
WARNING
DO NOT USE BLEACH in any diluted cleaning solution.
User Manual
190
UR3e
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 190

WARNING
Grease is an irritant and can cause an allergic reaction. Contact, inhalation or
ingestion can cause illness or injury. To prevent illness or injury, adhere to
the following:
•   PREPARATION:
•   Ensure that the area is well ventilated.
•   Have no food or beverages around the robot and cleaning
agents.
•   Ensure that an eye wash station is nearby.
•   Gather the required PPE (gloves, eye protection)
•   WEAR :
•   Protective gloves: Oil resistant gloves (Nitrile) impermeable
and resistant to product.
•   Eye protection is recommended to prevent accidental contact
of grease with eyes.
•   DO NOT INGEST.
•   In the event of
•   contact with skin, wash with water and a mild cleaning agent
•   a skin reaction, get medical attention
•   contact with the eyes, use an eyewash station, get medical
attention.
•   inhalation of vapors or ingestion of grease, get medical
attention
•   After grease work
•   clean contaminated work surfaces.
•   dispose responsibly of any used rags or paper used for
cleaning.
•   Contact with children and animals is prohibited.
UR3e
191
User Manual
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 191

Robot Arm
Inspection
Plan
The table below is a checklist of the type of inspections recommended by Universal Robots.
Perform inspections regularly as advised in the table. Any referenced parts found to be in an
unacceptable state must be rectified or replaced.
Inspection action type
Timeframe
Monthly
Biannually
Annually
1
Check flat rings
V
✘
2
Check robot cable
V
✘
3
Check robot cable connection
V
✘
4
Check Robot Arm mounting bolts
*
F
✘
5
Check Tool mounting bolts *
F
✘
6
Round Sling
F
✘
User Manual
192
UR3e
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 192

Robot Arm
Inspection
Plan
NOTICE
Using compressed air to clean the robot arm can damage the robot arm
components.
•   Never use compressed air to clean the robot arm.
UR3e
193
User Manual
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 193

Robot Arm
Inspection
Plan
1.   Move the Robot Arm to ZERO position, if possible.
2.   Turn off and disconnect the power cable from Control Box.
3.   Inspect the cable between Control Box and Robot Arm for any damage.
4.   Check the base mounting bolts are properly tightened.
5.   Check the tool flange bolts are properly tightened.
6.   Inspect the flat rings for wear and damage.
•   Replace the flat rings if they are worn out or damaged.
NOTICE
If any damage is observed on a robot within the warranty period, contact
the distributor where the robot was purchased.
Inspection
1.   Unmount any tool/s or attachment/s or set the TCP/Payload/CoG according to tool
specifications.
2.   To move the robot arm in Freedrive:
•   On a 3PE Teach Pendant, rapidly light-press, release, light-press again and
keep holding the 3PE button in this position.
Power button
3PE button
3.   Pull/Push the robot to a horizontally elongated position and release.
4.   Verify the robot arm can maintain the position without support and without activating
Freedrive.
User Manual
194
UR3e
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 194

14.3. Log Tab
Description
The Log tab displays information about the robot arm and Control Box.
Readings
and Joint
Load
The Readings pane displays Control Box information. The Joint Load pane displays
information for each robot arm joint.
Each joint displays:
•   Temperature
•   Load
•   Status
•   Voltage
Date Log
The first column displays log entries, categorized by the severity. The second column shows a
paperclip if there is an Error Report associated with the log entry. The next two columns
display the messages’ time of arrival and the source of the message. The last column shows a
short description of the message itself.
Some log messages are designed to provide more information that is displayed on the right
side, after selecting the log entry.
UR3e
195
User Manual
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 195

Message
Severity
You can filter messages by selecting the toggle buttons that correspond to the severity of the
log entry or by whether an attachment is present. The following table describes message
severity.
Provides general information, such as status of a program, changes of
the controller and controller version.
Issues that may have occurred but the system was able to recover.
A violation occurs if the safety limit is exceeded. This causes the robot
to perform a safety rated stop.
A fault occurs if there is an unrecoverable error in the system. This
causes the robot to perform a safety rated stop.
When you select a log entry, additional information appears on the right side of the screen.
Selecting the attachments filter either displays entry attachments exclusively or, displays all
entries.
Saving Error
Reports
A detailed status report is available when a paper clip icon appears on the log line.
NOTICE
The oldest report is deleted when a new one is generated. Only the five
most recent reports are stored.
1.   Select a log line and tap the Save Report button to save the report to a USB drive.
You can save the report while a program is running.
You can track and export the following list of errors:
•   Emergency stop
•   Fault
•   Internal PolyScope exceptions
•
1 Robot Stop
•   Unhandled exception in URCap
•   Violation
The exported report contains: a user program, a history log, an installation and a list of
running services.
1 Robot stop was previously known as "Protective Stop" for Universal Robots robots.
User Manual
196
UR3e
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 196

Technical
Support File
The report file contains information that is helpful to diagnose and reproduce issues. The file
contains records of previous robot failures, as well as current robot configurations,
programs and installations. The report file can be saved to external USB drive. On the Log
screen, tap Support file and follow the on-screen instructions to access the function.
NOTICE
The export process can take up to 10 minutes depending on USB drive
speed and the size of files collected from robot file system. The report is
saved as a regular zip file, that is not password protected, and can be
edited before sending to technical support.
UR3e
197
User Manual
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 197

14.4. Program and Installation Manager
Description
The Program and Installation Manager refers to three icons that allow you to create, load
and configure Programs and Installations:
•   New...   Allows you to create a new Program and/or Installation.
•   Open... Allows you to load a Program and/or Installation.
•   Save... Offers saving options for a Program and/or Installation.
The File Path displays your current loaded Program name and the type of Installation.
File Path changes when you create or load a new Program or Installation.
You can have several installation files for a robot. Programs created load and use the
active installation automatically.
To load
a
progra
m
1.   In the Program and Installation Manager, tap Open... and select Program.
2.   On the Load Program screen, select an existing program and tap Open.
3.   In the File Path, verify that the desired program name is displayed.
User Manual
198
UR3e
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 198

To load
an
installat
ion
1.   In the Program and Installation Manager, tap Open... and select Installation.
2.   On the Load Robot Installation screen, select an existing installation and tap Open.
3.   In the Safety Configuration box, select Apply and restart to prompt robot reboot.
4.   Select Set Installation to set installation for the current Program.
5.   In the File Path, verify that the desired installation name is displayed.
To create a
new program
1.   In the Program and Installation Manager, tap New... and select Program.
2.   On the Program screen, configure your new program as desired.
3.   In the Program and Installation Manager, tap Save... and select Save All or Save
Program As...
4.   On the Save Program As screen, assign a file name and tap Save.
5.   In the File Path, verify that the new program name is displayed.
To create a
new
installation
Save your installation for use after powering down the robot.
1.   In the Program and Installation Manager, tap New... and select Installation.
2.   Tap Confirm Safety Configuration.
3.   On the Installation screen, configure your new installation as desired.
4.   In the Program and Installation Manager, tap Save... and select Save Installation
As...
5.   On the Save Robot Installation screen, assign a file name and tap Save.
6.   Select Set Installation to set installation for the current Program.
7.   In File Path, verify that the new installation name is displayed.
UR3e
199
User Manual
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 199

To use the
save
options
Save...Depending on the program/installation you load-create, you can:
•   Save All to save the current Program and Installation immediately, without the system
prompting to save to a different location or different name. If no changes are made to
the Program or Installation, the Save All... button appears deactivated.
•   Save Program As... to change the new Program name and location. The current
Installation is also saved, with the existing name and location.
•   Save Installation As... to change the new Installation name and location. The current
Program is saved, with the existing name and location.
14.5. Accessing Robot Data
Description
Use the About option to access and display different types of data about the robot.
You can display the following types of robot data:
•   General
•   Version
•   Legal
User Manual
200
UR3e
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 200

To display
data about
the robot
1.   In the Header, tap the Hamburger menu.
2.   Select About.
3.   Tap General to access the robot's software version, network settings and serial
number.
For the other data types you can:
•   Tap Version to display more detailed data about the robot's software version.
•   Tap Legal to display data about the robot's software license/s.
4.   Tap Close to return to your screen.
UR3e
201
User Manual
14. Maintenance and Repair
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 201

15. Disposal and Environment
Description
Universal Robots robots must be disposed of in accordance with the applicable national
laws, regulations and standards. this responsibility rests with the owner of the robot.
UR robots are produced in compliance with restricted use of hazardous substances to
protect the environment; as defined by the European RoHS directive 2011/65/EU. If
robots (robot arm, Control Box, Teach Pendant) are returned to Universal Robots
Denmark, then the disposal is arranged by Universal Robots A/S.
The disposal fee for UR robots sold on the Danish market is prepaid to DPA-system by
Universal Robots A/S. Importers in countries covered by the European WEEE Directive
2012/19/EU must make their own registration to the national WEEE register of their
country. The fee is typically less than 1€/robot.
You can find a list of national registers here:  https://www.ewrn.org/national-registers .
Search for Global Compliance here:  https://www.universal-robots.com/download .
User Manual
202
UR3e
15. Disposal and Environment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 202

Substances in
the UR robot
Robot arm
•   Tubes, Base Flange, Tool mounting bracket: Anodized aluminum
•   Joint housings: Powder coated aluminum
•   Black band sealing rings: AEM rubber
•   additional slip ring under black band: moulded black plastic
•   Endcaps/ lids: PC/ASA Plastic
•   Minor mechanical components e.g. screws, nuts, spacers (steel, brass, and
plastic)
•   Wire bundles with copper wires and minor mechanical components e.g.
screws, nuts, spacers (steel, brass, and plastic)
Robot arm joints (internal)
•   Gears: Steel and grease (detailed in the Service Manual)
•   Motors: Iron core with copper wires
•   Wire bundles with copper wires, PCB's, various electronic components and
minor mechanical components
•   Joint seals and O-rings contain a small amount of PFAS which is a
compound within PTFE (commonly known as Teflon TM ).
•   Grease: synthetic + mineral oil with a thickener of either lithium complex
soap or Urea. Contains molybdenum.
•   Depending on model and date of production, the color of the grease
could be yellow, magenta, dark pink, red, green.
•   The Service Manual details the handling precautions and Grease
Safety Data Sheets
Control box
•   Cabinet (enclosure): Powder coated steel
•   Standard Control Box
•   Aluminum sheet metal housing (internal to the cabinet). This is also the
housing of the OEM controller.
•   Standard Control Box and OEM controller.
•   Wire bundles with copper wires, PCB's, various electronic components,
plastic connectors, and minor mechanical components e.g. screws, nuts,
spacers (steel, brass, and plastic)
•   A lithium battery is mounted to a PCB. See the Service Manual for how to
remove.
UR3e
203
User Manual
15. Disposal and Environment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 203

16. Risk Assessment
Description
The risk assessment is a requirement that shall be performed for the application. The
application risk assessment is the responsibility of the integrator. The user can also be
the integrator.
The robot is partly completed machinery, as such the safety of the robot application
depends on the tool/end effector, obstacles and other machines. The party performing
the integration must use ISO 12100 and ISO 10218-2 to conduct the risk assessment.
Technical Specification ISO/TS 15066 can provide additional guidance for collaborative
applications. The risk assessment shall consider all tasks throughout the lifetime of the
robot application, including but not limited to:
•   Teaching the robot during set-up and development of the robot application
•   Troubleshooting and maintenance
•   Normal operation of the robot application
A risk assessment must be conducted before the robot application is powered on for the
first time. The risk assessment is an iterative process. After physically installing the
robot, verify the connections, then complete the integration. A part of the risk
assessment is to determine the safety configuration settings, as well as the need for
additional emergency stops and/or other protective measures required for the specific
robot application.
User Manual
204
UR3e
16. Risk Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 204

Safety
configuration
settings
Identifying the correct safety configuration settings is a particularly important part of
developing robot applications. Unauthorized access to the safety configuration must be
prevented by enabling and setting password protection.
WARNING
Failure to set password protection can result in injury or death due to
purposeful or inadvertent changes to configuration settings.
•   Always set password protection.
•   Set up a program for managing passwords, so that access is
only by persons who understand the effect of changes.
Some safety functions are purposely designed for collaborative robot applications.
These are configurable through the safety configuration settings. They are used to
address risks identified in the application risk assessment.
The following limit the robot and as such can affect the energy transfer to a person by
the robot arm, end effector and workpiece.
•   Force and power limiting: Used to reduce clamping forces and pressures
exerted by the robot in the direction of movement in case of collisions between
the robot and the operator.
•   Momentum limiting: Used to reduce high transient energy and impact forces in
case of collisions between robot and operator by reducing the speed of the robot.
•   Speed limitation: Used to ensure the speed is less that the configured limit.
The following orientation settings are used to avoid movements and reduce exposure of
sharp edges and protrusions to a person.
•   Joint, elbow and tool/end effector position limiting: Used to reduce risks
associated with certain body parts: Avoid movement towards head and neck.
•   Tool/end effector orientation limiting: Used to reduce risks associated with
certain areas and features of the tool/end effector and work-piece: Avoid sharp
edges being pointed towards the operator, by turning the sharp edges inward
towards the robot.
Stopping
performance
risks
Some safety functions are purposely designed for any robot application. These features
are configurable through the safety configuration settings. They are used to address
risks associated with the stopping performance of the robot application.
The following limit the robot stopping time and stopping distance to ensure stopping will
occur before reaching the configured limits. Both settings automatically affect the speed
of the robot to ensure the limit is not exceeded.
•   Stopping Time Limit: Used to limit the stopping time of the robot.
•   Stopping Distance Limit: Used to limit the stopping distance of the robot.
If either of the above is used, there is no need for manually performed periodic stopping
performance testing. The robot safety control does continuous monitoring.
UR3e
205
User Manual
16. Risk Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 205

If the robot is installed in a robot application where hazards cannot be reasonably eliminated or
risks cannot be sufficiently reduced by use of the built-in safety-related functions (e.g. when
using a hazardous tool/end effector, or hazardous process), then safeguarding is required.
WARNING
Failure to conduct a application risk assessment can increase risks.
•   Always conduct an application risk assessment for foreseeable risks
and reasonably foreseeable misuse.
For collaborative applications, the risk assessment includes the
foreseeable risks due to collisions and to reasonably foreseeable
misuse.
The risk assessment shall address:
•   Severity of harm
•   Likelihood of occurrence
•   Possibility to avoid the hazardous situation
Potential
hazards
Universal Robots identifies the potential significant hazards listed below for consideration
by the integrator. Other significant hazards can be associated with a specific robot
application.
•   Penetration of skin by sharp edges and sharp points on tool/end effector or
tool/end effector connector.
•   Penetration of skin by sharp edges and sharp points on nearby obstacles.
•   Bruising due to contact.
•   Sprain or bone fracture due to impact.
•   Consequences due to loose bolts that hold the robot arm or tool/end effector.
•   Items falling out of, or flying from the tool/end effector, e.g. due to a poor grip or
power interruption.
•   Mistaken understanding of what is controlled by multiple emergency stop buttons.
•   Incorrect setting of the safety configuration parameters.
•   Incorrect settings due to unauthorized changes to the safety configuration
parameters.
User Manual
206
UR3e
16. Risk Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 206

16.1. Pinch Hazard
Description
You can avoid pinching hazards by removing obstacles in these areas, by placing the
robot differently, or by using a combination of safety planes and joint limits to eliminate
the hazards by preventing the robot moving into this area of its workspace.
CAUTION
Placing the robot in certain areas can create pinching hazards that can
lead to injury.
Due to the physical properties of the robot arm, certain workspace areas require
attention regarding pinching hazards. One area (left) is defined for radial motions when
the wrist 1 joint is at least 450 mm from the base of the robot. The other area (right) is
within 200 mm of the base of the robot, when moving tangentially.
UR3e
207
User Manual
16. Risk Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 207

16.2. Stopping Time and Stopping Distance
Description
NOTICE
You can set user-defined safety rated maximum stopping time and
distance.
If user-defined settings are used, the program speed is dynamically
adjusted to always comply with the selected limits.
The graphical data provided for Joint 0 (base), Joint 1 (shoulder) and Joint 2 (elbow) is
valid for stopping distance and stopping time:
•   Category 0
•   Category 1
•   Category 2
The Joint 0 test was carried out using a horizontal movement, where the rotational axis
was perpendicular to the ground. For the Joint 1 and Joint 2 tests, the robot followed a
vertical trajectory, where the rotational axes were parallel to the ground, and the stop
was done while the robot was moving downward.
The Y-axis is the distance from where the stop is initiated to the final position.
The payload CoG is at the tool flange.
Joint 0
(BASE)
Stopping
distance in
meters for
33% of 3kg
Stopping
distance in
meters for
66% of 3kg
User Manual
208
UR3e
16. Risk Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 208

Stopping
distance in
meters for
maximum
payload of 3kg
Joint 0
(BASE)
Stopping time
in seconds for
33% of 3kg
Stopping time
in seconds for
66% of 3kg
Stopping time
in seconds for
maximum
payload of 3kg
UR3e
209
User Manual
16. Risk Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 209

Joint 1
(SHOULDER)
Stopping
distance in
meters for 33%
of 3kg
Stopping
distance in
meters for
66% of 3kg
Stopping
distance in
meters for
maximum
payload of 3kg
Joint 1
(SHOULDER)
Stopping time in
seconds for 33%
of 3kg
User Manual
210
UR3e
16. Risk Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 210

Stopping time
in seconds for
66% of 3kg
Stopping time
in seconds for
maximum
payload of 3kg
Joint 2
(ELBOW)
Stopping
distance in
meters for
33% of 3kg
Stopping
distance in
meters for
66% of 3kg
UR3e
211
User Manual
16. Risk Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 211

Stopping
distance in
meters for
maximum
payload of 3kg
Joint 2
(ELBOW)
Stopping time
in seconds for
33% of 3kg
Stopping time
in seconds for
66% of 3kg
Stopping time
in seconds for
maximum
payload of 3kg
User Manual
212
UR3e
16. Risk Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 212

16.3. Commissioning
Descri
ption
The following tests must be conducted before using the robot application for the first time or after
making any modifications.
•   Verify all safety inputs and outputs are correctly connected.
•   Test all connected safety input and output, including devices common to multiple
machines or robots, are functioning as intended.
•   Test emergency stop buttons and inputs to verify the robot stops and the brakes engage.
•   Test safeguard inputs to verify the robot motion stops. If safeguard reset is configured,
check that it functions as intended.
•   Look at the initialization screen, activate the reduced input and verify the screen changes.
•   Change the operational mode to verify the mode icon changes in top right corner of
PolyScope screen.
•   Test the 3-position enabling device to verify that pressing to the center on position enables
motion in manual mode at a reduced speed.
•   If the Emergency Stop outputs are used, press the Emergency Stop push-button and
verify that there is a stop of the whole system.
•   Test the system connected to Robot Moving output, Robot Not Stopping output, Reduced
Mode output, or Not Reduced Mode output to verify the output changes are detected.
•   Determine the commissioning requirements of your robot application.
UR3e
213
User Manual
16. Risk Assessment
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 213

17. Declarations and Certificates (original
EN)
EU Declaration of Incorporation (DOI) (in accordance with 2006/42/EC Annex II B) original EN
Manufacturer
Universal Robots A/S
Energivej 51,
DK-5260 Odense S Denmark
Person in the Community
Authorized to Compile the
Technical File
David Brandt
Technology Officer, R&D
Universal Robots A/S, Energivej 51, DK-5260 Odense S
Description and Identification of the Partially-Completed Machine(s)
Product and Function:
Industrial robot multi-purpose multi-axis manipulator with control box &
with or without teach pendant function is determined by the completed
machine (robot application or cell with end-effector, intended use and
application program).
Model:
UR3e, UR5e, UR7e, UR10e, UR12e, UR16e (e-Series). This declaration
includes:
Effective October 2020: Teach Pendants with 3-Position Enabling (3PE TP) & standard
Teach Pendants (TP).
Effective May 2021: UR10e specification improvement to 12.5kg maximum payload.
Note: This Declaration of Incorporation is NOT applicable when the UR OEM Controller is used.
Serial Number:
Starting  XY 24 5 0 00000 and higher
Factory Variant year  e-Series  3=UR3e, 5=UR5e, 7=UR7e, 0=UR10e (10kg), 1=UR12e,
2=UR10e(12kg payload), 6=UR16e  sequential numbering, restarting at 0 each year
Incorporation:
Universal Robots e-Series (UR3e, UR5e, UR10e and UR16e) shall only
be put into service upon being integrated into a final complete machine
(robot application or cell), which conforms with the provisions of the
Machinery Directive and other applicable Directives.
It is declared that the above products fulfil, for what is supplied, the following directives as detailed below: When this incomplete
machine is integrated and becomes a complete machine, the integrator is responsible the completed machine fulfilling all
applicable Directives, applying the CE mark and providing the Declaration of Conformity (DOC).
I. Machinery Directive
2006/42/EC
II. Low-voltage Directive
2014/35/EU
III. EMC Directive 2014/30/EU
The following essential requirements have been fulfilled:
1.1.2, 1.1.3, 1.1.5, 1.2.1, 1.2.4.3, 1.2.5, 1.2.6, 1.3.2, 1.3.4, 1.3.8.1, 1.3.9, 1.5.1, 1.5.2,
1.5.5, 1.5.6, 1.5.10, 1.6.3, 1.7.2, 1.7.4, 4.1.2.3, 4.1.3 Annex VI.
It is declared the relevant technical documentation has been compiled in
accordance with Part B of Annex VII of the Machinery Directive.
Reference the LVD and the harmonized standards used below.
Reference the EMC Directive and the harmonized standards used below.
Reference to the harmonized standards used, as referred to in Article 7(2) of the MD & LV Directives and
Article 6 of the EMC Directive:
(I) EN ISO 10218-1:2011 Certification by TÜV
Rheinland (I) EN ISO 13732-1:2008 as
applicable (I) EN ISO 13849-1:2015 Certification
by TÜV Rheinland to 2015; 2023 edition has no
relevant changes (I) EN ISO 13849-2:2012 (I) EN
ISO 13850:2015
(I)(II) EN 60204-1:2018 as
applicable (II) EN
60529:1991+A1:2000+A2:2013 (I)
EN 60947-5-5:1997+A1:2005
+A11:2013+A2:2017 (I) EN 60947-
5-8:2020 (III) EN 61000-3-2:2019
(II) EN 60664-1:2007 (III) EN 61000-3-
3: 2013 (III) EN 61000-6-1:2019 UR3e
& UR5e ONLY (III) EN 61000-6-2:2019
(III) EN 61000-6-3:2007+A1: 2011
UR3e UR5e & UR7e ONLY (III) EN
61000-6-4:2019
Reference to other technical standards and technical specifications used:
User Manual
214
UR3e
17. Declarations and Certificates (original EN)
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 214

(I) ISO 9409-1:2004 [Type 50-4-M6] (I) ISO/TS
15066:2016 as applicable (III) EN 60068-2-1:
2007 (III) EN 60068-2-2:2007
(II) EN 60320-1:2021 (III) EN
60068-2-27:2008 (III) EN 60068-2-
64:2008+A1:2019
(II) EN 61784-3:2010 [SIL2] (III) EN
61326-3-1: 2017 [Industrial locations
SIL 2]
The manufacturer, or his authorised representative, shall transmit relevant information about the partly
completed machinery in response to a reasoned request by the national authorities. Approval of full quality
assurance system (ISO 9001), by the notified body Bureau Veritas, certificate #DK015892.
UR3e
215
User Manual
17. Declarations and Certificates (original EN)
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 215

18. Declarations and Certificates
EU Declaration of Incorporation (DOI) (in accordance with 2006/42/EC Annex II B) original EN
Manufacturer
Universal Robots A/S
Energivej 25,
DK-5260 Odense S Denmark
Person in the Community
Authorized to Compile the
Technical File
David Brandt
Technology Officer, R&D
Universal Robots A/S, Energivej 25, DK-5260 Odense S
Description and Identification of the Partially-Completed Machine(s)
Product and Function:
Industrial robot multi-purpose multi-axis manipulator with control box &
with or without teach pendant Function is determined by the completed
machine (robot application or cell with end-effector, intended use and
application program).
Model :
UR3e, UR5e, UR10e, UR16e (e-Series): Below cited certifications and
this declaration include:
•   Effective October 2020: Teach Pendants with 3-Position Enabling
(3PE TP) & standard Teach Pendants (TP).
•   Effective May 2021: UR10e specification improvement to 12.5kg
maximum payload.
Note: This Declaration of Incorporation is NOT applicable when the UR OEM Controller
is used.
Serial Number:
Starting  2023 5 0 00000 and higher
year  e-Series  3=UR3e, 5=UR5e, 3=UR3e, 0=UR10e (10kg), 2=UR10e(12.5),
6=UR16e  sequential numbering, restarting at 0 each year
Incorporation:
Universal Robots e-Series (UR3e, UR5e, UR10e and UR16e) shall only
be put into service upon being integrated into a final complete machine
(robot application or cell), which conforms with the provisions of the
Machinery Directive and other applicable Directives.
It is declared that the above products fulfil, for what is supplied, the following directives as detailed below:
When this incomplete machine is integrated and becomes a complete machine, the integrator is responsible
for determining that completed machine fulfils all applicable Directives and providing the Declaration of
Conformity.
I. Machinery Directive
2006/42/EC
The following essential requirements have been fulfilled: 1.1.2, 1.1.3,
1.1.5, 1.2.1, 1.2.4.3, 1.2.5, 1.2.6, 1.3.2, 1.3.4, 1.3.8.1, 1.3.9, 1.5.1, 1.5.2,
1.5.5, 1.5.6, 1.5.10, 1.6.3, 1.7.2, 1.7.4, 4.1.2.3, 4.1.3, Annex VI. It is
declared that the relevant technical documentation has been compiled in
accordance with Part B of Annex VII of the Machinery Directive.
II. Low-voltage Directive
2014/35/EU
III. EMC Directive 2014/30/EU
Reference the LVD and the harmonized standards used below.
Reference the EMC Directive and the harmonized standards used below.
Reference to the harmonized standards used, as referred to in Article 7(2) of the MD & LV Directives and
Article 6 of the EMC Directive:
User Manual
216
UR3e
18. Declarations and Certificates
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 216

(I) EN ISO 10218-1:2011 TÜV
Nord Certificate # 44 708
14097607
(I) EN ISO 13732-1:2008 as
applicable (I) EN ISO 13849-
1:2015 TÜV Nord Certificate #
44 207 14097610 (I) EN ISO
13849-2:2012 (I) EN ISO
13850:2015
(I) (II) EN 60204-1:2018 as
applicable (II) EN
60529:1991+A1:2000+A2:2013 (I)
EN 60947-5-5:1997+A1:2005
+A11:2013+A2:2017 (I) EN 60947-
5-8:2020 (III) EN 61000-3-2:2019
(II) EN 60664-1:2007 (III) EN 61000-3-
3: 2013 (III) EN 61000-6-1:2019 UR3e
& UR5e ONLY (III) EN 61000-6-2:2019
(III) EN 61000-6-3:2007+A1: 2011
UR3e & UR5e ONLY (III) EN 61000-6-
4:2019
Reference to other technical standards and technical specifications used:
(I) ISO 9409-1:2004 [Type 50-
4-M6] (I) ISO/TS 15066:2016
as applicable (III) EN 60068-2-
1: 2007 (III) EN 60068-2-
2:2007
(II) EN 60320-1:2021 (III) EN
60068-2-27:2008 (III) EN 60068-2-
64:2008+A1:2019
(II) EN 61784-3:2010 [SIL2] (III) EN
61326-3-1: 2017 [Industrial locations
SIL 2]
The manufacturer, or his authorised representative, shall transmit relevant information about the partly
completed machinery in response to a reasoned request by the national authorities.Approval of full quality
assurance system (ISO 9001), by the notified body Bureau Veritas, certificate #DK015892.
UR3e
217
User Manual
18. Declarations and Certificates
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 217

19. Certifications
Description
Third party certification is voluntary. However, to provide the best service to robot
integrators, Universal Robots chooses to certify its robots at the recognized test
institutes listed below.
You can find copies of all certificates in the chapter: Certificates.
Certification
TÜV Rheinland
Certificates by TÜV Rheinland to EN ISO
10218-1 and EN ISO 13849-1. TÜV
Rheinland stands for safety and quality in
virtually all areas of business and life.
Founded 150 years ago, the company is
one of the world’s leading testing service
providers.
TÜV Rheinland
of North America
In Canada, the Canadian Electrical
Code, CSA 22.1, Article 2-024 requires
equipment to be certified by a testing
organization approved by the Standards
Council of Canada.
CHINA RoHS
Universal Robots e-Series robots
conform to CHINA RoHS management
methods for controlling pollution by
electronic information products.
KCC Safety
Universal Robots e-Series robots have
been assessed and conform to KCC
mark safety standards.
KC Registration
The Universal Robots e-Series robots
have been evaluated for conformity
assessment for use in a work
environment. Therefore, there is a risk of
radio interference when used in a
domestic environment.
Delta
Universal Robots e-Series robots are
performance tested by DELTA.
Supplier Third
Party
Certification
Environment
As provided by our suppliers, Universal Robots e-
Series robots shipping pallets comply with the
ISMPM-15 Danish requirements for producing wood
packaging material and are marked in accordance
with this scheme.
User Manual
218
UR3e
19. Certifications
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 218

Manufacturer
Test
Certification
Universal
Robots
Universal Robots e-Series robots undergo
continuous internal testing and end of line test
procedures.
UR testing processes undergo continuous review
and improvement.
Declarations
according to
EU directives
Although EU directives are relevant for Europe, some countries outside Europe recognize
and/or require EU declarations. European directives are available on the official
homepage: http://eur-lex.europa.eu.
According to the Machinery Directive, Universal Robots’ robots are partly completed
machines, as such a CE mark is not to be affixed.
You can find the Declaration of Incorporation (DOI) according to the Machinery Directive
in the chapter: Declarations and Certificates.
EU REACH
Our product includes components, specifically the blue plastic lids (cups) and grey plastic
parts, that contain substances listed on the EU REACH Candidate List (>0.1% w/w).
For reference, please see the Global Compliance Document available for download on our
website.
This information is provided to comply with EU REACH obligations for articles placed on the
EU market. Please use our product as intended and follow all operational and safety
instructions provided in this manual. For further details, refer to the official REACH
Regulation (Consolidated Text: 32006R1907). If you have questions related to product
safety, please contact us at: ProductCompliance@teradyne-robotics.com.
UR3e
219
User Manual
19. Certifications
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 219

20. Certificates
TÜV Rheinland
User Manual
220
UR3e
20. Certificates
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 220

TÜV Rheinland
North America
UR3e
221
User Manual
20. Certificates
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 221

China
RoHS
铅
Lead (Pb)
汞
Mercury
(Hg)
镉
Cadmium
(Cd)
六价
Hexavalent
Chromium
(Cr+6)
多溴 联苯
Polybrominated
biphenyls (PBB)
多溴二苯 醚
Polybrominated
diphenyl ethers
(PBDE)
UR Robots
机器人：基本系 统
UR3 / UR5 / UR10 /
UR3e / UR5e /
UR10e   UR16e /
UR20 / UR30
X
O
X
O
X
X
有毒有害物 质或元素
Product/Part
Name
产品 / 部件名称
To the maximum extent permitted by law, Customer shall be solely responsible for complying with, and shall otherwise assume all liabilities that
may be imposed in connection with, any legal requirements adopted by any governmental authority related to the Management Methods for
Controlling Pollution by Electronic Information Products (Ministry of Information Industry Order #39) of the Peoples Republic of China otherwise
encouraging the recycle and use of electronic information products.  Customer shall defend, indemnify and hold Universal Robots harmless from
any damage, claim or liability relating thereto.  At the time Customer desires to dispose of the Products, Customer shall refer to and comply with
the specific waste management instructions and options set forth     at www.universal‐robots.com/about‐universal‐robots/social‐responsibility and
www.teradyne.com/company/corporate‐social‐responsibility, as the same may be amended by Teradyne or Universal Robots.
O: Indicates that this toxic or hazardous substance contained in all of the homogeneous materials for this part is below the limit
requirement in SJ/T11363‐2006.
O:  表示 该有毒有害物质在该部件所有均质材料中的含量均在 SJ/T 11363‐2006 规定的限量要求以下。
X: Indicates that this toxic or hazardous substance contained in at least one of the homogeneous materials used for this part is above
the limit requirement in SJ/T11363‐2006.
X:  表示 该有毒有害物质至少在该部件的某一均质材料中的含量超出 SJ/T 11363‐2006 规定的限量要求。
Universal Robots encourages that all Electronic Information Products be recycled but does not assume responsibility or liability.
Universal Robots  鼓励回收再循 环利用所有的电子信息产品 ,  但  Universal Robots  不 负任何责任或义务
（企 业可在此处，根据实际情况对上表中打 “X” 的技 术原因进行进一步说明。）
Items below are wear‐out items and therefore can have useful lives less than environmental use period:
下列 项目是损耗品 , 因而它 们的有用环境寿命可能短于基本系统和可选项目的使用时间 :
Drives, Gaskets, Probes, Filters, Pins, Cables, Stiffener, Interfaces
电子驱动器 ,   垫圈 ,  探 针 ,  过滤器 ,  别针 ,  缆绳 ,  加 强筋 ,  接口
Refer to product manual for detailed conditions of use.
详细使用情况请阅读产品手册 .
Toxic and Hazardous Substances and Elements
Management Methods for Controlling Pollution
by Electronic Information Products
Product Declaration Table For Toxic or Hazardous Substances
表 1  有毒有害物 质或元素名称及含量标识格式
User Manual
222
UR3e
20. Certificates
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 222

KC Safety
UR3e
223
User Manual
20. Certificates
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 223

KC
Registration
User Manual
224
UR3e
20. Certificates
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 224

Environment
DELTA  – a part of FORCE Technology - Venlighedsvej 4 - 2970 Hørsholm - Denmark - Tel. +45 72 19 40 00 - Fax +45 72 19 40 01 - www.delta.dk
Climatic and mechanical assessment
Client
Force Technology project no.
Universal Robots A/S
Energivej 25
5260 Odense S
Denmark
117-32120
Product identification
UR 3 robot arms
UR 3 control boxes with attached Teach Pendants.
UR 5 robot arms
UR5 control boxes with attached Teach Pendants.
UR10 robot arms:
UR10 control boxes with attached Teach Pendants.
See reports for details.
Force Technology report(s)
DELTA project no. 117-28266, DANAK-19/18069
DELTA project no. 117-28086, DANAK-19/17068
Other document(s)
Conclusion
The three robot arms UR3, UR5 and UR10 including their control boxes and Teach Pendants have been tested
according to the below listed standards. The test results are given in the Force Technology reports listed above. The
tests were carried out as specified and the test criteria for environmental tests were fulfilled in general terms with
only a few minor issues (see test reports for details).
IEC 60068-2-1, Test Ae; -5 ºC, 16 h
IEC 60068-2-2, Test Be; +35°C, 16h
IEC 60068-2-2, Test Be; +50ºC, 16 h
IEC 60068-2-64, Test Fh; 5 – 10 Hz: +12 dB/octave, 10-50 Hz 0.00042 g²/Hz, 50 – 100 Hz: -12 dB/octave, 1,66
grms, 3 x 1½ h
IEC 60068-2-27, Test Ea, Shock; 11 g, 11 ms, 3 x 18 shocks
Date
Assessor
Hørsholm, 25 August 2017
Andreas Wendelboe Højsgaard
M.Sc.Eng.
UR3e
225
User Manual
20. Certificates
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 225

21. Safety Functions Table
Description
Universal Robots safety functions and safety I/O are PLd Category 3 (ISO 13849-1),
where each safety function has a PFH D  value less than 1.8E-07.
The PFH D  values are updated to include greater design flexibility for supply chain
resilience.
For safety I/O the resulting safety function including the external device, or equipment, is
determined by the overall architecture and the sum of all PFH D s, including the UR robot
safety function PFH D .
NOTICE
The Safety Functions tables presented in this chapter are simplified.
You can find the comprehensive versions of them here:
https://www.universal-robots.com/support
SF1
Emergency
Stop
(according to
ISO 13850)
See footnotes
Description
What
happens?
Tolerance
and PFH D
Affects
Pressing the Estop PB on the pendant 1   or the
External Estop (if using the Estop Safety
Input) results in a Stop Cat 1   3 with power
removed from the robot actuators and the tool
I/O. Command 1   all joints to stop and upon all
joints coming to a monitored standstill state,
power is removed.
For the integrated functional safety rating with
an external safety-related control system or
an external emergency stop device that is
connected to the Emergency Stop input, add
the PFH D  of this safety-related input to the
PFH D  of this safety function’s PFH D  value
(less than 1.8E-07).
Category 1
stop (IEC
60204-1)
Tol: --
PFH D : 1.8E-
07
Robot
including
robot tool
I/O
User Manual
226
UR3e
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 226

SF2
Safeguard
Stop 4
(Robot Stop
according to
ISO 10218-1)
Description
What
happens?
Tolerance
and PFH D
Affects
This safety function is initiated by an external
protective device using safety inputs that initiate
a Cat 2 stop 3 . The tool I/O are unaffected by the
safeguard stop. Various configurations are
provided. If an enabling device is connected, it's
possible to configure the safeguard stop to
function in automatic mode ONLY. See the Stop
Time and Stop Distance Safety Functions 4 . For
the functional safety of the complete integrated
safety function, add the PFHd of the external
protective device to the PFHd of the Safeguard
Stop.
Category 2
stop (IEC
60204-1)
SS2 stop
(as
described in
IEC 61800-
5-2)
Tol: --
PFH D : 1.8E-
07
Robot
SF3 Joint
Position
Limit (soft
axis
limiting)
Description
What happens?
Tolerance
and PFH D
Affects
Sets upper and lower limits for the allowed
joint positions. Stopping time and distance is
not a considered as the limit(s) will not be
violated. Each joint can have its own limits.
Directly limits the set of allowed joint
positions that the joints can move within. It is
set in the safety part of the User Interface. It
is a means of safety-rated soft axis limiting
and space limiting, according to ISO 10218-
1:2011, 5.12.3.
Will not allow
motion to exceed
any limit settings.
Speed could be
reduced so
motion will not
exceed any limit.
A robot stop will
be initiated to
prevent
exceeding any
limit.
Tol: 5°
PFH D : 1.8E-
07
Joint
(each)
SF4 Joint
Speed
Limit
Description
What happens?
Tolerance
and PFH D
Affects
Sets an upper limit for the joint speed. Each
joint can have its own limit. This safety
function has the most influence on energy
transfer upon contact (clamping or
transient). Directly limits the set of allowed
joint speeds which the joints are allowed to
perform. It is set in the safety setup part of
the User Interface. Used to limit fast joint
movements, e.g. risks related to
singularities.
Will not allow
motion to exceed
any limit settings.
Speed could be
reduced so motion
will not exceed any
limit. A robot stop
will be initiated to
prevent exceeding
any limit.
Tol: 1.15 °/s
PFH D : 1.8E-
07
Joint
(each)
Joint
Torque
Limit
Exceeding the internal joint torque limit (each joint) results in a Cat 0 3 . This is not accessible
to the user; it is a factory setting. It is NOT shown as an e-Series safety function because
there are no user settings and no user configurations.
UR3e
227
User Manual
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 227

SF5 Called
various
names:   Pose
Limit, Tool
Limit,
Orientation
Limit, Safety
Planes,
Safety
Boundaries
Description
What
happens?
Tolerance
and PFH D
Affects
Monitors the TCP Pose (position and
orientation) and will prevent exceeding a
safety plane or TCP Pose Limit. Multiple
pose limits are possible (tool flange, elbow,
and up to 2 configurable tool offset points
with a radius) Orientation restricted by the
deviation from the feature Z direction of the
tool flange OR the TCP. This safety function
consists of two parts. One is the safety
planes for limiting the possible TCP
positions. The second is the TCP
orientation limit, which is entered as an
allowed direction and a tolerance. This
provides TCP and wrist inclusion/ exclusion
zones due to the safety planes.
Will not allow
motion to
exceed any
limit settings.
Speed or
torques could
be reduced so
motion will not
exceed any
limit. A robot
stop will be
initiated to
prevent
exceeding any
limit. Will not
allow motion to
exceed any
limit settings.
Tol: 3° 40
mm
PFH D : 1.8E-
07
TCP
Tool
flange
Elbow
SF6
Speed
Limit TCP
& Elbow
Description
What happens?
Tolerance
and PFH D
Affects
Monitors the
TCP and
elbow speed
to prevent
exceeding a
speed limit.
Will not allow motion to exceed any limit settings.
Speed or torques could be reduced so motion
will not exceed any limit. A robot stop will be
initiated to prevent exceeding any limit. Will not
allow motion to exceed any limit settings.
Tol:50 mm/s
PFH D : 1.8E-
07
TCP
SF7
Force
Limit
(TCP)
Description
What happens?
Tolerance
and PFH D
Affects
The Force Limit is the force exerted by the
robot at the TCP (tool center point) and
“elbow”. The safety function continuously
calculates the torques allowed for each joint to
stay within the defined force limit for both the
TCP & the elbow. The joints control their
torque output to stay within the allowed torque
range. This means that the forces at the TCP
or elbow will stay within the defined force limit.
When a monitored stop is initiated by the
Force Limit SF, the robot will stop, then “back-
off” to a position where the force limit was not
exceeded. Then it will stop again.
Will not allow
motion to exceed
any limit settings.
Speed or torques
could be reduced
so motion will not
exceed any limit.
A robot stop will
be initiated to
prevent
exceeding any
limit. Will not
allow motion to
exceed any limit
settings.
Tol: 25N
PFH D : 1.8E-
07
TCP
User Manual
228
UR3e
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 228

SF8
Momentum
Limit
Description
What happens?
Tolerance
and PFH D
Affects
The momentum
limit is very useful
for limiting
transient impacts.
The Momentum
Limit affects the
entire robot.
Will not allow motion to exceed any limit
settings. Speed or torques could be
reduced so motion will not exceed any
limit. A robot stop will be initiated to
prevent exceeding any limit. Will not
allow motion to exceed any limit settings.
Tol: 3kg m/s
PFH D : 1.8E-
07
Robot
SF9
Power
Limit
Description
What
happens?
Tolerance
and PFH D
Affects
This function monitors the mechanical work
(sum of joint torques times joint angular
speeds) performed by the robot, which also
affects the current to the robot arm as well as
the robot speed. This safety function
dynamically limits the current/ torque but
maintains the speed.
Dynamic
limiting of the
current/torque
Tol: 10W
PFH D :1.8E-
07
Robot
SF10 UR
Robot
Estop
Output
Description
What
Happens
PFH D
Affects
When configured for a Robot <Estop> output and
there is a robot stop, the dual outputs are LOW. If
there is no Robot <Estop> Stop initiated, dual
outputs are high. Pulses are not used but they are
tolerated.
These dual outputs change state for any external
Estop that is connected to configurable safety
inputs where this input is configured as an
Emergency Stop input.
For the integrated functional safety rating with an
external safety-related control system, add the
PFHD of this safety-related output to the PFHD of
the external safety-related control system.
For the Estop Output, validation is performed at
the external equipment, as the UR output is an
input to this external Estop safety function for
external equipment.
NOTE: If the IMMI (Injection Moulding Machine
Interface) is used, the UR Robot Estop output is
NOT connected to the IMMI. There is no Estop
output signal sent sent from the UR robot to the
IMMI.This is a feature to prevent an
unrecoverable stop condition.
Dual outputs
go low in event
of an Estop if
configurable
outputs are set
1.8E-
07
External
connection
to logic
and/or
equipment
UR3e
229
User Manual
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 229

SF11 UR
Robot
Moving:
Digital
Output
Description
What Happens
PFH D
Affects
Whenever the robot is moving (motion
underway), the dual digital outputs are
LOW. Outputs are HIGH when no
movement. The functional safety rating is
for what is within the UR robot. The
integrated functional safety performance
requires adding this PFHd to the PFHd of
the external logic (if any) and its
components.
If configurable
outputs are set:
•   When the
robot is
moving
(motion
underway),
the dual
digital
outputs are
LOW.
•   Outputs are
HIGH when
no
movement.
1.8E-
07
External
connection
to logic
and/or
equipment
SF12 UR
Robot Not
stopping:
Digital
Output
Description
PFH D
Affects
When the robot is STOPPING (in process of stopping or in a
stand-still condition) the dual digital outputs are HIGH. When
outputs are LOW, robot is NOT in the process or stopping and
NOT in a stand-still condition. The functional safety rating is for
what is within the UR robot. The integrated functional safety
performance requires adding this PFHd to the PFHd of the
external logic (if any) and its components.
1.8E-
07
External
connection
to logic
and/or
equipment
SF13 UR
Robot
Reduced
Mode:
Digital
Output
Description
PFH D
Affects
When the robot is in reduced mode (or reduced mode is
initiated), the dual digital outputs are LOW. See below. The
functional safety rating is for what is within the UR robot. The
integrated functional safety performance requires adding this
PFHd to the PFHd of the external logic (if any) and its
components.
1.8E-
07
External
connection
to logic
and/or
equipment
SF14   UR
Robot Not
Reduced
Mode:
Digital
Output
Description
PFH D
Affects
Whenever the robot is NOT in reduced mode (or the reduced
mode is not initiated), the dual digital outputs are LOW. The
functional safety rating is for what is within the UR robot. The
integrated functional safety performance requires adding this
PFHd to the PFHd of the external logic (if any) and its
components.
1.8E-
07
External
connection
to logic
and/or
equipment
User Manual
230
UR3e
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 230

SF15
Stopping
Time Limit
Description
What happens?
Tolerances
and PFH D :
Affects
Real time monitoring of conditions such that
the stopping time limit will not be exceeded.
Robot speed is limited to ensure that the
stop time limit is not exceeded.
The stopping capability of the robot in the
given motion(s) is continuously monitored
to prevent motions that would exceed the
stopping limit. If the time needed to stop the
robot is at risk of exceeding the time limit,
the speed of motion is reduced to ensure
the limit is not exceeded. A robot stop will
be initiated to prevent exceeding the limit.
The safety function performs the same
calculation of the stopping time for the
given motion(s) and initiates a cat 0 stop if
the stopping time limit will be or is
exceeded.
Will not allow the
actual stopping
time to exceed
the limit setting.
Causes
decrease in
speed or a robot
stop so as NOT
to exceed the
limit
TOL: 50 ms
PFH D : 1.8E-
07
Robot
SF16
Stopping
Distance
Limit
Description
What happens?
Tolerances
and PFH D :
Affects
Real time monitoring of conditions such that
the stopping distance limit will not be
exceeded. Robot speed is limited to ensure
that the stop distance limit will not be
exceeded.
The stopping capability of the robot in the
given motion(s) is continuously monitored
to prevent motions that would exceed the
stopping limit. If the time needed to stop the
robot is at risk of exceeding the time limit,
the speed of motion is reduced to ensure
the limit is not exceeded. A robot stop will
be initiated to prevent exceeding the limit.
The safety function performs the same
calculation of the stopping distance for the
given motion(s) and initiates a cat 0 stop if
stopping time limit will be or is exceeded.
Will not allow the
actual stopping
time to exceed
the limit setting.
Causes
decrease in
speed or a robot
stop so as NOT
to exceed the
limit
TOL: 40 mm
PFH D : 1.8E-
07
Robot
UR3e
231
User Manual
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 231

SF17 Safe
Home
Position
"monitored
position"
Description
What happens?
Tolerances
and PFH D :
Affects
Safety function which monitors a
safety rated output, such that it
ensures that the output can only be
activated when the robot is in the
configured and monitored “safe
home position”.
A stop cat 0 is initiated if the output
is activated when the robot is not in
the configured position.
The “safe home
output” can only be
activated when the
robot is in the
configured “safe
home position”
TOL: 1.7 °
PFH D : 1.8E-
07
External
connection
to logic
and/or
equipment
Table 1
footnotes
1 Communications between the Teach Pendant, controller and within the robot (between
joints) are SIL 2 for safety data, per IEC 61784-3.
2 Estop validation: the pendant Estop pushbutton is evaluated within the pendant, then
communicated¹ to the safety controller by SIL2 communications. To validate the pendant
Estop functionality, press the Pendant Estop pushbutton and verify that an Estop results.
This validates that the Estop is connected within the pendant, the estop functions as
intended, and the pendant is connected to the controller.
3 Stop Categories according to IEC 60204-1 (NFPA79). For the Estop, only stop category 0
and 1 are allowed according to IEC 60204-1.
•   Stop Category 0 and 1 result in the removal of drive power, with stop cat 0 being
IMMEDIATE and stop cat 1 being a controlled stop (e.g. decelerate to a stop then
removal of drive power). With UR robots, a stop category 1 is a controlled stop where
power is removed when a monitored standstill is detected.
•   Stop Category 2 is a stop where drive power is NOT removed. Stop category 2 is
defined in IEC 60204-1. Descriptions of STO, SS1 and SS2 are in IEC 61800-5-2.
With UR robots, a stop category 2 maintains the trajectory, then retains power to the
drives after stopping.
4 It is recommended to use the UR Stop Time and Stop Distance Safety Functions. These
limits should be used for your application stop time/ safety distance values.
5 Robot stop was previously known as "Protective stop" for Universal Robots robots.
User Manual
232
UR3e
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 232

21.1. Table 1a
Reduced
Mode SF
parameter
settings
change
Description
PFH D
Affects
Reduced Mode can be initiated by a safety plane/ boundary
(starts at 2cm of the plane and reduced mode settings are
achieved within 2cm of the plane) or by use of an input to initiate
(will achieve reduced settings within 500ms). When the external
connections are Low, Reduced Mode is initiated. Reduced Mode
means that ALL reduced mode limits are ACTIVE.
Reduced mode is not a safety function, rather it is a state change
affecting the settings of the following safety function limits: joint
position, joint speed, TCP pose limit, TCP speed, TCP force,
momentum, power, stopping time, and stopping distance.
Reduced mode is a means of parametrization of safety functions
in accordance with ISO 13849-1. All parameter values need to be
verified and validated as to whether they are appropriate for the
robot application.
Less
than
1.8E-
07
Robot
Safeguard
Reset
Description
PFH D
Affects
When configured for Safeguard Reset and the external connections
transition from low to high, the safeguard stop RESETS. Safety
input to initiate a reset of safeguard stop safety function.
Less
than
1.8E-
07
Input to
SF2
Robot
3-Position
Enabling
Device
INPUT
Description
PFH D
Affects
When the external Enabling Device connections are Low, a
Safeguard Stop (SF2) is initiated. Recommendation: Use with a
mode switch as a safety input. If a mode switch is not used and
connected to the safety inputs, then the robot mode will be
determined by the User Interface. If the User Interface is in:
•   “running mode”, the enabling device will not be active.
•   “programming mode”, the enabling device will be active. It is
possible to use password protection for changing the mode by
the User Interface.
Less
than
1.8E-
07
Input to
SF2
Robot
UR3e
233
User Manual
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 233

Mode
switch
INPUT
Description
PFH D
Affects
When the external connections are Low, Operation Mode (running/
automatic operation in automatic mode) is in effect. When High, mode
is programming/ teach. Recommendation: Use with an enabling
device, for example a UR e-Series Teach Pendant with an integrated
3-position enabling device.
When in teach/program, initially both TCP speed and elbow speed will
be limited to 250mm/s. The speed can manually be increased by using
the pendant user interface “speed-slider”, but upon activation of the
enabling device, the speed limitation will reset to 250mm/s.
Less
than
1.8E-
07
Input to
SF2
Robot
Freedrive
INPUT
Description
PFH D
Affects
Recommendation: Use with 3PE TP and/or 3 Position Enabling
Device INPUT. When Freedrive INPUT is High, the robot will only
enter Freedrive if the following conditions are satisfied:
•   3PE TP button is not pressed
•   3 Position Enabling Device INPUT either not configured or
not pressed (INPUT Low)
Less
than
1.8E-
07
Input to
SF2
Robot
21.2. Table 2
Description
UR e-Series robots comply with ISO 10218-1:2011 and the applicable portions of
ISO/TS 15066. It is important to note that most of ISO/TS 15066 is directed towards the
integrator and not the robot manufacturer. ISO 10218-1:2011, clause 5.10 collaborative
operation details 4 collaborative operation techniques as explained below. It is very
important to understand that collaborative operation is of the APPLICATION when in
AUTOMATIC mode.
Collaborative
Operation 2011
edition, clause
5.10.2
Technique
Explanation
UR e-Series
Safety-rated
monitored
stop
Stop condition where position is held at a
standstill and is monitored as a safety
function. Category 2 stop is permitted to
auto reset. In the case of resetting and
restarting operation after a safety -rated
monitored stop, see ISO 10218-2 and
ISO/TS 15066 as resumption shall not
cause hazardous conditions.
UR robots’ safeguard
stop is a safety-rated
monitored stop, See SF2
on page 1. It is likely, in
the future, that “safety-
rated monitored stop” will
not be called a form of
collaborative operation.
User Manual
234
UR3e
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 234

Collaborative
Operation 2011
edition, clause
5.10.3
Technique
Explanation
UR e-Series
Hand-
guiding
This is essentially individual
and direct personal control
while the robot is in automatic
mode. Hand guiding
equipment shall be located
close to the end-effector and
shall have:
•   an Emergency Stop
pushbutton
•   a 3-position enabling
device
•   a safety-rated
monitored stop
function
•   a settable safety-rated
monitored speed
function
UR robots do not provide hand-guiding
for collaborative operation. Hand-
guided teach (free drive) is provided
with UR robots but this is for
programming in manual mode and not
for collaborative operation in automatic
mode.
UR3e
235
User Manual
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 235

Collaborative
Operation 2011
edition, clause
5.10.4
Technique
Explanation
UR e-Series
Speed and
separation
monitoring
(SSM) safety
functions
SSM is the robot
maintaining a separation
distance from any
operator (human). This is
done by monitoring of the
distance between the
robot system and
intrusions to ensure that
the MINIMUM
PROTECTIVE
DISTANCE is assured.
Usually, this is
accomplished using
Sensitive Protective
Equipment (SPE), where
typically a safety laser
scanner detects intrusion
(s) towards the robot
system.
This SPE causes:
1.   dynamic changing
of the parameters
for the limiting
safety functions; or
2.   a safety-rated
monitored stop
condition.
Upon detection of the
intrusion exiting the
protective device’s
detection zone, the robot
is permitted to:
1.   resume the
“higher” normal
safety function
limits in the case of
1) above
2.   resume operation
in the case of 2)
above
In the case of 2) 2),
restarting operation after
a safety -rated monitored
stop, see ISO 10218-2
and ISO/TS 15066 for
requirements.
To facilitate SSM, UR robots have the
capability of switching between two sets of
parameters for safety functions with
configurable limits (normal and reduced).
See Reduced Mode on page 4. Normal
operation can be when no intrusion is
detected. It can also be caused by safety
planes/ safety boundaries. Multiple safety
zones can be readily used with UR robots.
For example, one safety zone can be used
for “reduced settings” and another zone
boundary is used as a safeguard stop input
to the UR robot. Reduced limits can also
include a reduced setting for the stop time
and stop distance limits – to reduce the
work area and floorspace.
User Manual
236
UR3e
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 236

Collaborative
Operation 2011
edition, clause
5.10.5
Technique
Explanation
UR e-Series
Power and
force limiting
(PFL) by
inherent
design or
control
How to accomplish PFL is left to the
robot manufacturer. The robot
design and/or safety functions will
limit the energy transfer from the
robot to a person. If any parameter
limit is exceeded, a robot stop
happens. PFL applications require
considering the ROBOT
APPLICATION (including the end-
effector and workpiece(s), so that
any contact will not cause injury. The
study performed evaluated
pressures to the ONSET of pain, not
injury. See Annex A. See ISO/TR
20218-1 End-effectors.
UR robots are power and force
limiting robots specifically
designed to enable
collaborative applications where
the robot could contact a person
and cause no injury. UR robots
have safety functions that can
be used to limit motion, speed,
momentum, force, power and
more of the robot. These safety
functions are used in the robot
application to thereby lessen
pressures and forces caused by
the end-effector and workpiece
(s).
UR3e
237
User Manual
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 237

User Manual
238
UR3e
21. Safety Functions Table
Copyright © 2009–2024 by Universal Robots A/S. All rights reserved.

### Page 238

Software Name: PolyScope 5
Software Version: 5.20
Document Version: 10.8.158