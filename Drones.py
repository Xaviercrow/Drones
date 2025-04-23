import djitellopy
import pygame
import threading
import cv2
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))

# Movement variables
updown = 0
leftright = 0
forwardback = 0
rotation = 0
running = True

# Variables
detected_ring_color = None
flash_message = ""
flash_start_time = 0
saved_colors = set()

# Connect to Tello drone
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
    global running, detected_ring_color, flash_message, flash_start_time

    while running:
        frame = me.get_frame_read().frame
        img = cv2.resize(frame, (600, 400))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Improved HSV ranges
        color_ranges = {
            "Red": [((0, 100, 100), (6, 255, 255)), ((170, 100, 100), (180, 255, 255))],
            "Orange": [((5, 100, 100), (25, 255, 255))],
            "Yellow": [((21, 100, 100), (35, 255, 255))],
            "Green": [((40, 70, 70), (80, 255, 255))],
            "Blue": [((100, 150, 0), (140, 255, 255))],
            "Purple": [((130, 50, 50), (170, 255, 255))] 
        }

        detected_ring_color = None
        output = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)

        for color, ranges in color_ranges.items():
            mask = None
            for lower, upper in ranges:
                if mask is None:
                    mask = cv2.inRange(hsv, lower, upper)
                else:
                    mask |= cv2.inRange(hsv, lower, upper)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 3000:
                    x, y, w, h = cv2.boundingRect(cnt)
                    aspect_ratio = w / float(h)

                    if 0.5 < aspect_ratio < 2.0:
                        detected_ring_color = color
                        muted = cv2.bitwise_and(output, output, mask=cv2.bitwise_not(mask))  # black & white
                        highlight = cv2.bitwise_and(img, img, mask=mask)                      # color
                        output = cv2.add(muted, highlight)  # Merge

                        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(output, f"{detected_ring_color}", (x + 5, y - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        break
            if detected_ring_color:
                break

        # Flash overlay
        if flash_message:
            if time.time() - flash_start_time < 1.5:
                cv2.putText(output, flash_message, (150, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            else:
                flash_message = ""

        cv2.imshow("Tello Camera", output)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            running = False
            break

    cv2.destroyAllWindows()

# Save color
def save_color_to_file(detected_ring_color, saved_colors):
    global flash_message, flash_start_time
    if detected_ring_color and detected_ring_color not in saved_colors:
        print(f"Detected Ring Color: {detected_ring_color}")
        with open("colors.txt", "a") as f:
            f.write(f"{detected_ring_color}\n")  # Write the color to the file
        saved_colors.add(detected_ring_color)  # Add to the set of saved colors

        flash_message = f"Color Saved: {detected_ring_color}"  # Set the flash message
        flash_start_time = time.time()  # Update flash start time

# Start Threads
moving_thread = threading.Thread(target=moving)
camera_thread = threading.Thread(target=show_camera)

moving_thread.start()
camera_thread.start()

# Main Control Loop
saved_colors = set()  # Initialize an empty set to track saved colors

while True:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LSHIFT:
                running = False
                me.land()
                break
            elif e.key == pygame.K_t:
                me.takeoff()
            elif e.key == pygame.K_a:
                leftright = -25
            elif e.key == pygame.K_d:
                leftright = 25
            elif e.key == pygame.K_q:
                updown = 60
            elif e.key == pygame.K_e:
                updown = -60
            elif e.key == pygame.K_w:
                forwardback = 25
            elif e.key == pygame.K_s:
                forwardback = -25
            elif e.key == pygame.K_l:
                rotation = 75
            elif e.key == pygame.K_BACKSPACE:
                me.emergency()
            elif e.key == pygame.K_f:
                me.flip_forward()
            elif e.key == pygame.K_p:
                save_color_to_file(detected_ring_color, saved_colors)  # Pass the saved_colors set

        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_LSHIFT:
                me.land()
                quit()
            elif e.key in [pygame.K_a, pygame.K_d]:
                leftright = 0
            elif e.key in [pygame.K_q, pygame.K_e]:
                updown = 0
            elif e.key in [pygame.K_w, pygame.K_s]:
                forwardback = 0
            elif e.key == pygame.K_l:
                rotation = 0