import turtle
import time
import numpy as np


# Coordinates of windows in a 140 x 2 matrix
# 20 x 7 windows
# gap is 19.26 x 36.33
vertical = np.arange(-168, 198, 19.26)
horizontal = np.arange(-107, 111, 36.33)
vertical = np.around(vertical, 2)
horizontal = np.around(horizontal, 2)
vertical = np.flip(vertical)

coords = np.zeros((140, 2))

for i, j in enumerate(vertical):
    for n, m in enumerate(horizontal):
        coords[i * 7 + n] = [m, j]

# Create screen with background
wn = turtle.Screen()
wn.setup(width=470, height=660)
wn.bgpic("building.gif")
wn.title("Animation Demo")
wn.bgcolor("white")


# Register shapes
wn.register_shape("quadcopter.gif")
# wn.register_shape("quadcopter2.gif")
wn.register_shape("water.gif")


class Windows(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self, visible=False)
        self.penup()
        self.shape("circle")
        self.color("red")
        self.shapesize(0.4, 0.4)

    def start_position(self, x, y):
        self.speed(0)          # set its movement speed to instant
        self.setpos(x, y)  # figure those out first...
        self.showturtle()


class Drone(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self, visible=False)
        self.penup()
        self.shape("quadcopter.gif")
        self.speed(9)
        # self.frame = 0
        # self.frames = ["quadcopter.gif", "quadcopter2.gif"]

    def animate(self):
        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0
        self.shape(self.frames[self.frame])
        # Set timer
        wn.ontimer(self.animate, 500)

    def start_position(self, x):
        initial_speed = self.speed()         # store its initial speed
        self.speed(0)          # set its movement speed to instant

        self.setpos(x, -280)  # figure those out first...

        self.speed(initial_speed)  # set turtle's speed to initial value
        self.showturtle()          # make turtle appear in desired position

    def move(self, i):
        if i > 4:
            status_circles[i - 5].color("green")
        self.setpos(coords[i])

    def finish(self, i, j):
        status_circles[i - 5 + j].color("green")
        self.setpos(-200 + 50 * j, -280)


class Waterdrone(Drone):
    def __init__(self):
        super().__init__()
        self.shape("water.gif")

    def move(self, i):
        if i > 0:
            status_circles[i - 1].color("orange")
        self.setpos(coords[i])
        status_circles[i].color("blue")

    def finish(self, i):
        status_circles[i - 1].color("orange")
        self.setpos(150, -280)


points = np.size(coords, 0)
# points = 9

# initialise circles
status_circles = list()
for i in range(points):
    status_circles.append(Windows())

for i in range(len(status_circles)):
    status_circles[i].start_position(coords[i, 0], coords[i, 1])

# initialise drones
players = list()
for i in range(5):
    players.append(Drone())

for i in range(len(players)):
    players[i].start_position(-200 + 50 * i)

water = Waterdrone()
water.start_position(150)

t = 0.3  # waiting time

for i in range(points + 1):
    x = i % len(players)
    if i < points:
        water.move(i)
        if i > 0:
            players[x].move(i - 1)
    else:
        water.finish(i)
        time.sleep(t)
        players[x].move(i - 1)
        time.sleep(t)
        if x == 4:
            x = 0
        else:
            x += 1
        order = [k for k in range(x, len(players))] + [k for k in range(x)]
        for j, m in enumerate(order):
            players[m].finish(i, j)
            time.sleep(t)

    time.sleep(t)

wn.mainloop()
