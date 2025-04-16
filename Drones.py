import djitellopy
import pygame
import threading
<<<<<<< HEAD
import cv2
# Initializing
=======
import time
import cv2
>>>>>>> 36e5613aa1b6f9ec7e5888e9cdb7a0f5144a9567
pygame.init()
screen = pygame.display.set_mode((600,400))
# Movement
updown = 0
leftright = 0
forwardback = 0
rotation = 0
takeoff = 0
<<<<<<< HEAD
# Connect
=======
cameraoff = 0
>>>>>>> 36e5613aa1b6f9ec7e5888e9cdb7a0f5144a9567
me = djitellopy.Tello()
me.connect()
me.streamon()
me.takeoff()
# Movement Function
def moving():
    while True:
        me.send_rc_control(leftright, forwardback, updown, rotation)
# Camera Function 
def show_camera():
    while True:
        frame = me.get_frame_read().frame
        img = cv2.resize(frame, (600, 400))
        cv2.imshow("Tello Camera", img)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    cv2.destroyAllWindows()
# Start Threads
movingthread = threading.Thread(target= moving)
movingthread.start()
# Main Loop
while True:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if (e.key == pygame.K_SPACE):
                me.land()
                quit()
            if(e.key == pygame.K_t):
                takeoff
            elif (e.key == pygame.K_a):
                leftright = -25
            elif(e.key ==pygame.K_d):
                leftright = 25 
            elif(e.key == pygame.K_q):
                updown = 60
            elif(e.key == pygame.K_e):
                updown = -60
            elif(e.key == pygame.K_w):
                forwardback = 25
            elif(e.key == pygame.K_s):
                forwardback = -25
            elif(e.key == pygame.K_l):
                rotation = 75
            elif(e.key == pygame.K_BACKSPACE):
                me.emergency
        if e.type == pygame.KEYUP:
             if (e.key == pygame.K_SPACE):
                me.land()
                quit()
             elif (e.key == pygame.K_a):
                leftright = 0
             elif(e.key ==pygame.K_d):
                leftright = 0
             elif(e.key == pygame.K_q):
                updown = 0
             elif(e.key == pygame.K_e):
                updown = 0
             elif(e.key == pygame.K_w):
                forwardback = 0
             elif(e.key == pygame.K_s):
                forwardback = 0
             elif(e.key == pygame.K_l):
                rotation = 0
                
