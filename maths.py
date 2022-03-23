import numpy as np

vertical = np.arange(-168, 198, 19.26)
horizontal = np.arange(-107, 111, 36.33)
vertical = np.around(vertical, 2)
horizontal = np.around(horizontal, 2)
vertical = np.flip(vertical)


coords = np.zeros((140, 2))

for i, j in enumerate(vertical):
    for n, m in enumerate(horizontal):
        coords[i * 7 + n] = [m, j]
print(np.size(coords, 0))
for i in range(np.size(coords, 0)):
    # print(coords[i])
    if i % 5 == 0:
        print(coords[i])
x = 5
y = [i for i in range(x, 10)] + [i for i in range(x)]
print(y)
