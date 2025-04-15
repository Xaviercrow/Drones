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
            elif (e.key == pygame.K_a):
                leftright = -25
            elif(e.key ==pygame.K_d):
                leftright = 25 