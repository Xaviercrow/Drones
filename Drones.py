import djitellopy
import pygame
import threading
import cv2
import time
# Initializing
pygame.init()
screen = pygame.display.set_mode((600,400))
# Movement
updown = 0
leftright = 0
forwardback = 0
rotation = 0
running = True
# Connect
me = djitellopy.Tello()
me.connect()
me.streamon()
# Movement Thread
def moving():
    global running
    while running:
        me.send_rc_control(leftright, forwardback, updown, rotation)
        time.sleep(0.05)
# Camera Function 
def show_camera():
    global running
    saved_colors = set()
    while running:
        frame = me.get_frame_read().frame
        img = cv2.resize(frame, (600, 400))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# HSV Ranges
        color_ranges = {
            "Red": [((0, 120, 70), (10, 255, 255)), ((170, 120, 70), (180, 255, 255))],
            "Orange": [((10, 100, 100), (25, 255, 255))],
            "Yellow": [((25, 100, 100), (35, 255, 255))],
            "Green": [((40, 70, 70), (80, 255, 255))],
            "Blue": [((100, 150, 0), (140, 255, 255))],
            "Purple": [((140, 100, 100), (160, 255, 255))]
        }

        detected_ring_color = None

        for color, ranges in color_ranges.items():
            mask = None
            for lower, upper in ranges:
                if mask is None:
                    mask = cv2.inRange(hsv, lower, upper)
                else:
                    mask |= cv2.inRange(hsv, lower, upper)

            center_mask = mask[100:300, 200:400]
            contours, _ = cv2.findContours(center_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
           
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 1000:  
                    detected_ring_color = color 
# File Saving
                    if detected_ring_color and detected_ring_color not in saved_colors:
                        print(f"Detected Ring Color: {detected_ring_color}")
                        with open("colors.txt", "a") as f:
                            f.write(f"{detected_ring_color}\n")
                        saved_colors.add(detected_ring_color)
        cv2.imshow("Tello Camera", img)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            running = False
            break
    cv2.destroyAllWindows()
# Start Threads
movingthread = threading.Thread(target= moving)
camera_thread = threading.Thread(target=show_camera)

movingthread.start()
camera_thread.start()
# Main Loop
while True:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SHIFT:
                running = False
                me.land()
                break
            elif e.key == pygame.K_t:
                me.takeoff() 
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
                me.emergency()
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
                
