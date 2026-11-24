import cv2
import numpy as np

def four_point_transform(image, points):
    # put the 4 corners in a consistent order: top-left, top-right, bottom-right, bottom-left

    rectangle = np.zeros((4,2), dtype="float32")


    coordinate_sums = points.sum(axis=1)
    rectangle[0] = points[np.argmin(coordinate_sums)]
    rectangle[2] = points[np.argmax(coordinate_sums)]

    coordinate_differences = np.diff(points, axis=1)
    rectangle[1] = points[np.argmin(coordinate_differences)]
    rectangle[3] = points[np.argmax(coordinate_differences)]

    (top_left, top_right, bottom_right, bottom_left) = rectangle

    # next we wanna estimate the width of the top and bottom edges
    width_bottom = np.linalg.norm(bottom_right - bottom_left)
    width_top = np.linalg.norm(top_right - top_left)
    width = max(int(width_bottom), int(width_top))

    # next we wanna estimate the height of the left and right edges
    height_right = np.linalg.norm(top_right - bottom_right)
    height_left = np.linalg.norm(top_left - bottom_left)
    height = max(int(height_right), int(height_left))

    if width < 2 or height < 2:
        raise ValueError("Detected document is too small to transform.")

    # These are the corners of the straightened output image.
    destination = np.array([
        [0,0],
        [width -1, 0],
        [width -1, height -1],
        [0, height -1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(rectangle, destination)

    return cv2.warpPerspective(image, matrix, (width, height))
