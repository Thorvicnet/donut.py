import numpy as np
import sys
import os
from time import sleep

# ## Variables ## #

stepTorus = 90 # Number of circles in the torus
step = int(stepTorus / np.pi) # Number of points in the circle

circleR = 1 # Radius of the circle used to make the torus
circleX = 2 # X position of the circle

dt = 0.1 # Time between each frames in the animation

screenWidth, screenHeight = os.get_terminal_size() # Size of the terminal
distanceFromScreen = 5
distanceOfDonutFromScreen = 100 # Change this to zoom in or out

scaleY = 0.5 # Scale the Y axis to make the donut look better

# ## End of variables ## #


rotationX = 1 # Starting rotations
rotationZ = 1

K = screenWidth * distanceFromScreen * 3 / (8 * (circleR + circleX)) - distanceOfDonutFromScreen


def frame(rotationX: float, rotationZ: float) -> [str, str]: # Returns the points of the circle in a frame
    output = [[" "] * screenHeight for _ in range(screenWidth)]
    zbuffer = [[0] * screenHeight for _ in range(screenWidth)]
    cosRotationZ = np.cos(rotationZ)
    sinRotationZ = np.sin(rotationZ)
    cosRotationX = np.cos(rotationX)
    sinRotationX = np.sin(rotationX)
    for i in range(0, step):
        theta = i * 2 * np.pi / step
        sinThetaCircleR = np.sin(theta) * circleR
        cosTheta = np.cos(theta)
        sinTheta = np.sin(theta)
        r2r1 = circleR * cosTheta + circleX
        for j in range(0, stepTorus):
            alpha = j * 2 * np.pi / stepTorus
            sinAlpha = np.sin(alpha)
            cosAlpha = np.cos(alpha)
            x = r2r1 * (cosRotationZ * cosAlpha + sinRotationX * sinRotationZ * sinAlpha) - cosRotationX * sinRotationZ * sinThetaCircleR
            y = r2r1 * (sinRotationZ * cosAlpha - sinRotationX * cosRotationZ * sinAlpha) + cosRotationX * cosRotationZ * sinThetaCircleR
            z = distanceFromScreen + cosRotationX * r2r1 * sinAlpha + sinRotationX * sinThetaCircleR
            zm1 = 1 / z # z^-1 precomputed

            # Projecting the points on the screen
            xs = int(screenWidth / 2 + x * K * zm1)
            ys = int((screenHeight / 2 + y * K * zm1) * scaleY)
            if xs >= screenWidth or xs < 0 or ys >= screenHeight or ys < 0: # If the point is outside the screen
                continue

            # Lighting
            light = cosAlpha * cosTheta * sinRotationZ - cosRotationX * cosTheta * sinAlpha - sinRotationX * sinTheta + cosRotationZ * (cosRotationX * sinTheta - cosTheta * sinRotationX * sinAlpha)
            if light > 0:
                if zm1 > zbuffer[xs][ys]: # If the point is closer to the screen than the previous one
                    zbuffer[xs][ys] = zm1
                    output[xs][ys] = ".,-~:;=!*#$@"[int(light * 8)] # Change the characters to change the donut's look
    return output


def printFrame(frame: [str, str]):
    for y in range(len(frame[0])):
        for x in range(len(frame)):
            sys.stdout.write(frame[x][y])
        sys.stdout.write("\n")


if __name__ == "__main__":
    while True:
        printFrame(frame(rotationX, rotationZ))
        rotationX += dt
        rotationZ += dt
        sleep(dt)
        sys.stdout.flush() # Flush the terminal
