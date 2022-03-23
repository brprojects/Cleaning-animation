import numpy as np

x = np.random.random_sample(5)
y = ['']*5
print(y)
print(x)

for i in range(len(x)):
    if x[i] <= 0.6 :
        y[i] = "circle"
    elif x[i] <= 0.8 and x[i] > 0.6 :
        y[i] = "square"
    else:
        y[i] = "triangle"
print(y)