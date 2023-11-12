import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

stepTorus = 50 # Number of circles in the torus
step = int(stepTorus / np.pi) # Number of points in the circle
rotationX = 0.5 # Starting rotations
rotationZ = 0.5
circleR = 2 # Radius of the circle
circleX = 10 # X position of the circle
dt = 0.1 # Time between each frames in the animation
numberFrames = 10000 # Number of frames before the animation stops


def frame(rotationX: float, rotationZ: float) -> (list, list, list): # Returns the points of the circle in a frame
    x = []
    y = []
    z = []
    cosRotationZ = np.cos(rotationZ)
    sinRotationZ = np.sin(rotationZ)
    cosRotationX = np.cos(rotationX)
    sinRotationX = np.sin(rotationX)
    for i in range(0, step):
        theta = i * 2 * np.pi / step
        sinThetaCircleR = np.sin(theta) * circleR
        r2r1 = circleR * np.cos(theta) + circleX
        for j in range(0, stepTorus):
            alpha = j * 2 * np.pi / stepTorus
            sinAlpha = np.sin(alpha)
            cosAlpha = np.cos(alpha)
            x.append(r2r1 * (cosRotationZ * cosAlpha + sinRotationX * sinRotationZ * sinAlpha) - cosRotationX * sinRotationZ * sinThetaCircleR)
            y.append(r2r1 * (sinRotationZ * cosAlpha - sinRotationX * cosRotationZ * sinAlpha) + cosRotationX * cosRotationZ * sinThetaCircleR)
            z.append(cosRotationX * r2r1 * sinAlpha + sinRotationX * sinThetaCircleR)
    return x, y, z


def animate(i): # Animation function
    t = i * dt
    ax.clear()
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_zlim(-20, 20)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    rotationX = t
    rotationZ = t
    x, y, z = frame(rotationX, rotationZ)
    ax.scatter(x, y, z)
    return ax,


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x, y, z = frame(rotationX, rotationZ)
    ax.scatter(x, y, z)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ani = animation.FuncAnimation(fig, animate, frames=numberFrames, interval=1, blit=True, repeat=False)

    plt.show()
