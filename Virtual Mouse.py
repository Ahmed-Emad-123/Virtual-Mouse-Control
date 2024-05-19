import random
import cv2 as cv
import mediapipe.python.solutions.drawing_utils
import numpy as np
from mediapipe.python import *
import mediapipe.python.solutions as solutions
import os
import uuid
import mouse_module
import pyautogui
from pynput.mouse import Button, Controller

mous = Controller()
screen_w, screen_h = pyautogui.size()

# ---------------- Moving mouse Function ---------------- #
def mouse_move(index_finger):
    if index_finger is not None:

        # ---------------- fit screen of frame to laptop ---------------- #
        x = int(index_finger.x * screen_w)
        y = int(index_finger.y * screen_h)

        # ---------------- moving mouse function to limited screen (frame) ---------------- #
        pyautogui.moveTo(x, y)


# ---------------- left click mouse function ---------------- #
def left_click(landmarks_list, thumb_distance):
    return (mouse_module.get_angle_finger(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
            mouse_module.get_angle_finger(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90 and
            thumb_distance > 50
            )

# ---------------- right click mouse function ---------------- #
def right_click(landmarks_list, thumb_distance):
    return (mouse_module.get_angle_finger(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            mouse_module.get_angle_finger(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and
            thumb_distance > 50
            )

# ---------------- double click mouse function ---------------- #
def double_click(landmarks_list, thumb_distance):
    return (mouse_module.get_angle_finger(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
            mouse_module.get_angle_finger(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            thumb_distance > 50
            )

# ---------------- screen shot function ---------------- #
def screen_shot(frame, landmarks_list, thumb_distance):
    return (mouse_module.get_angle_finger(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
            mouse_module.get_angle_finger(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            thumb_distance < 50
            )

# ---------------- Finger Tips Function ---------------- #
def find_finger_tip(results):
    # ---------------- check landmarks  ---------------- #
    if results.multi_hand_landmarks:

        # ---------------- access landmarks  ---------------- #
        hand_lm = results.multi_hand_landmarks[0]

        # ---------------- return index of each finger  ---------------- #
        return hand_lm.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]

    return None


# ---------------- Gestures Function ---------------- #
def detect_gestures(frame, landmarks_list, results):
    if len(landmarks_list) >= 21:

        index_finger = find_finger_tip(results)
        thumb_distance = mouse_module.get_distance_finger([landmarks_list[4], landmarks_list[5]])

        # ---------------- thumb position and mouse moving  ---------------- #
        if thumb_distance < 50 and mouse_module.get_angle_finger(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90:
            mouse_move(index_finger)

        elif left_click(landmarks_list, thumb_distance):
            mous.press(Button.left)
            mous.release(Button.left)
            cv.putText(frame, 'left click', (50,50), cv.FONT_HERSHEY_PLAIN, 1, color=(255,0,255), thickness=1)

        elif right_click(landmarks_list, thumb_distance):
            mous.press(Button.right)
            mous.release(Button.right)
            cv.putText(frame, 'right click', (50,50), cv.FONT_HERSHEY_PLAIN, 1, color=(255,0,255), thickness=1)

        elif double_click(landmarks_list, thumb_distance):
            pyautogui.doubleClick()
            cv.putText(frame, 'double click', (50,50), cv.FONT_HERSHEY_PLAIN, 1, color=(255,0,255), thickness=1)

        elif screen_shot(frame, landmarks_list, thumb_distance):
            img = pyautogui.screenshot()
            label = random.randint(1, 1000)
            # img.save(f'my screen shot {label}.png')
            cv.imwrite(os.path.join(f'saved images', f'screen_shot {label}.png'), frame)
            cv.putText(frame, 'screen shot', (50,50), cv.FONT_HERSHEY_PLAIN, 1, color=(255,0,255), thickness=1)


# ---------------- Initialize hand pose  ---------------- #
mp_hand = mediapipe.python.solutions.hands
mp_draw = mediapipe.python.solutions.drawing_utils

hands = mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1)

def main():

    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        # ---------------- Flag the image ---------------- #
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image.flags.writeable = False

        # ---------------- Detection process ---------------- #
        results = hands.process(image)

        # ---------------- Flag the image ---------------- #
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        # ---------------- Rendering results (landmarks) ---------------- #
        landmarks_list = []

        if results.multi_hand_landmarks:
            for id, hand_lm in enumerate(results.multi_hand_landmarks):
                mp_draw.draw_landmarks(image, hand_lm, mp_hand.HAND_CONNECTIONS)

                # ---------------- Rendering each (landmarks) ---------------- #
                for lm in hand_lm.landmark:
                    landmarks_list.append((lm.x, lm.y))

        # ---------------- detect the gestures ---------------- #
        detect_gestures(image, landmarks_list, results)

        cv.imshow('frame', image)

        if cv.waitKey(1) == ord('q'):
            break


    cap.release()
    cv.destroyWindow()

if __name__ == '__main__':
    main()


"""
Usage :: import pyautogui
1- Mouse Control -> Moving the Mouse - Clicking and Scrolling - Dragging and Dropping

* Moving the Mouse          => pyautogui.moveTo(x, y): Moves the mouse pointer to the specified coordinates (x, y).
pyautogui.moveRel(xOffset, yOffset): Moves the mouse pointer relative to its current position.

* Clicking and Scrolling    => pyautogui.click(x=None, y=None, button='left', clicks=1, interval=0): Clicks the mouse at the specified coordinates or the current position.
pyautogui.scroll(clicks): Scrolls the mouse wheel up or down by the specified number of clicks.

* Dragging and Dropping     => pyautogui.dragTo(x, y, duration=0.0): Drags the mouse to the specified coordinates over a specified duration.
pyautogui.dragRel(xOffset, yOffset, duration=0.0): Drags the mouse relative to its current position.

2- Keyboard Control -> Typing Text - Hotkeys and Shortcuts

* Typing Text               => pyautogui.typewrite(text, interval=0.0): Types the given text with a specified interval between keystrokes.
pyautogui.press(keys): Presses the specified keys (e.g., 'enter', 'ctrl', 'shift').

* Hotkeys and Shortcuts     => pyautogui.hotkey(*args): Simulates pressing multiple keys simultaneously (e.g., 'ctrl+c', 'alt+tab').

3- Screenshot and Pixel Manipulation -> Capturing Screenshots - Pixel Analysis

* Capturing Screenshots     => pyautogui.screenshot(imageFilename=None): Captures a screenshot of the entire screen or a specified region.

4- Other Useful Features -> Time Control - Error Handling

* Time Control              => pyautogui.PAUSE: Pauses the script execution for a specified duration.
pyautogui.sleep(secs): Waits for a specified number of seconds before continuing.
"""