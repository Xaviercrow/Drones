# Drones
Members: Peyton And Xavier
Controls: WASD, P, T, F, Q, E, and Shift
T- takeoff
w- forward
A- left
S- backward
D- right
Q- up
E- down
F- flip
P- print color
Shift- land

This project uses a Tello drone controlled via Python to autonomously or manually detect and identify colored rings in its flight path. The drone streams live video, which is processed using OpenCV to detect specific ring colors based on HSV color filtering. Detected rings are highlighted with bounding boxes, and the corresponding color name is overlaid on the video feed. Users can save detected colors to a text file using a keybind, with a flash overlay confirming the save.

Key features include:

Real-time color detection with HSV masking
Visual overlay of detected ring colors and HSV values
Manual drone control using Pygame
Color logging with flash feedback
Adjustable HSV thresholds for accurate color recognition in varying lighting conditions

