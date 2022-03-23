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
wn.register_shape("scanner.gif")
wn.register_shape("water.gif")


class Windows(turtle.Turtle):
    def __init__(self, shape):
        turtle.Turtle.__init__(self, visible=False)
        self.penup()
        self.shape(shape)
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
            status_shapes[i - 5].color("green")
        self.setpos(coords[i])

    def finish(self, i, j):
        status_shapes[i - 5 + j].color("green")
        self.setpos(-200 + 50 * j, -280)

    def reclean(self, i):
        status_shapes[i - 4].color("green")
        self.setpos(coords[i - len(players) - 2])


class Waterdrone(Drone):
    def __init__(self):
        super().__init__()
        self.shape("water.gif")

    def move(self, i):
        if i > 0:
            status_shapes[i - 1].color("orange")
        self.setpos(coords[i])
        status_shapes[i].color("blue")

    def finish(self, i):
        status_shapes[i - 1].color("orange")
        self.setpos(150, -280)

    def reclean(self, i):
        status_shapes[i].color("orange")
        self.setpos(coords[i - len(players) - 2])
        status_shapes[i - len(players) - 2].color("blue")
    
    def end_reclean(self,i):
        status_shapes[i - len(players) - 2].color("orange")
        self.setpos(coords[i+1])
        status_shapes[i+1].color("blue")

class Scanner(Drone):
    def __init__(self):
        super().__init__()
        self.shape("scanner.gif")

    def move(self, i):
        self.setpos(coords[i])

    def finish(self):
        self.setpos(75, -280)

    def dirty(self, i):
        status_shapes[i].color("red")
        

# How system reacts to a window scan being dirty
def dirty_scan(i, x, t):
    scan.dirty(i - len(players) - 2)
    time.sleep(t)
    water.reclean(i)
    time.sleep(t)
    if x == 4:
        x = 0
    else:
        x += 1
    players[x].move(i)
    scan.move(i - len(players))
    time.sleep(t)
    water.end_reclean(i)
    time.sleep(t)
    if x == 4:
        x = 0
    else:
        x += 1
    players[x].reclean(i)
    scan.move(i - len(players) + 1)

points = np.size(coords, 0)
# points = 16

# initialise shapes
status_shapes = list()
dirtiness = np.random.random_sample(points)
shape = [''] * points
for i in range(len(dirtiness)):
    if dirtiness[i] <= 0.85 :
        shape[i] = "circle"
    elif dirtiness[i] <= 0.95 and dirtiness[i] > 0.85 :
        shape[i] = "square"
    else:
        shape[i] = "triangle"
for i in range(points):
    status_shapes.append(Windows(shape[i]))

for i in range(len(status_shapes)):
    status_shapes[i].start_position(coords[i, 0], coords[i, 1])

# initialise drones
players = list()
for i in range(5):
    players.append(Drone())

for i in range(len(players)):
    players[i].start_position(-200 + 50 * i)

water = Waterdrone()
water.start_position(150)

scan = Scanner()
scan.start_position(75)

t = 0.3  # waiting time

dirty_windows = [10, 16, 22]
iter = [i for i in range(points + 1)]
for i in dirty_windows:
    iter.remove(i+1)
dirty_windows_remove = list(map(lambda n: n + 2 , dirty_windows))

for i in iter:
    x = i % len(players)
    if i < points:
        water.move(i)
        if i > 0:
            players[x].move(i - 1)
        if i > len(players) :
            scan.move(i - len(players) - 1)
        if i in dirty_windows:
           dirty_scan(i, x, t)
        if i in dirty_windows_remove:
            status_shapes[i - len(players) - 4].color("green")

    else:
        water.finish(i)
        time.sleep(t)
        players[x].move(i - 1)
        scan.move(i - len(players) - 1)
        time.sleep(t)
        if x == 4:
            x = 0
        else:
            x += 1
        order = [k for k in range(x, len(players))] + [k for k in range(x)]
        for j, m in enumerate(order):
            players[m].finish(i, j)
            scan.move(i + j - len(players))
            time.sleep(t)
        scan.finish()

    time.sleep(t)

wn.mainloop()
