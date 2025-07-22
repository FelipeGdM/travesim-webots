"""camera_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
import cv2
import matplotlib.pyplot as plt
import numpy as np
from controller import Camera, Supervisor

# create the Robot instance.
robot = Supervisor()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

camera = robot.getDevice("camera")
camera.enable(timestep)

# Get camera dimensions
width = camera.getWidth()
height = camera.getHeight()

# Setup matplotlib for live updating
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
ax.set_title("Webots Camera Feed")
image_plot = ax.imshow(np.zeros((height, width, 3)))
plt.tight_layout()
plt.show(block=False)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    img = camera.getImage()
    if img:
        # Convert image to numpy array
        np_image = np.frombuffer(img, dtype=np.uint8)
        np_image = np_image.reshape((height, width, 4))

        # Update plot data
        image_plot.set_data(cv2.cvtColor(np_image, cv2.COLOR_BGRA2RGB))

        # Refresh matplotlib display
        fig.canvas.flush_events()
    else:
        print("Warning: No image data received")

# Enter here exit cleanup code.
plt.ioff()
plt.close()
print("Controller terminated")
