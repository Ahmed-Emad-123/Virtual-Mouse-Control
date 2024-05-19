import numpy as np

def get_angle_finger(a, b, c):

    # ---------------- getting angle between ab and bc to + x-axis ---------------- #
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])

    # ---------------- convert from radians to degrees ---------------- #
    angle = np.abs(np.degrees(radians))

    return angle

def get_distance_finger(landmark_list):
    # ---------------- check for min landmarks ---------------- #
    if len(landmark_list) < 2:
        return

    # ---------------- Calculate distance ---------------- #
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    length = np.hypot(x2 - x1, y2 - y1)

    # ---------------- scale distance ---------------- #
    return np.interp(length, [0, 1], [0, 1000])



"""
* np.arctan2(c[1] - b[1], c[0] - b[0]) calculates the angle between the positive x-axis and the vector from b to c.
* np.arctan2(a[1] - b[1], a[0] - b[0]) calculates the angle between the positive x-axis and the vector from b to a.

* In the code, a, b, and c are likely representing points in two-dimensional space. The index [0] 
refers to the x-coordinate of the point, and the index [1] refers to the y-coordinate. 
So, a[0] represents the x-coordinate of point a, a[1] represents the y-coordinate of point a, and so on.
"""