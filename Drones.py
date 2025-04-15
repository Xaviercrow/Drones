import djitellopy
import pygame
import threading
import time
pygame.init()
screen = pygame.display.set_mode((600,400))
updown = 0
leftright = 0
forwardback = 0
rotation = 0
takeoff = 0
me = djitellopy.Tello()
me.connect()
me.takeoff()
def moving():
    while True:
        me.send_rc_control(leftright, forwardback, updown, rotation)
movingthread = threading.Thread(target= moving)
movingthread.start()
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