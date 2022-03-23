dirty_windows = [8,3,5]
dirty_windows_remove = list(map(lambda n: n +1 , dirty_windows))
print(dirty_windows_remove)
x = range(15)
y = [i for i in x]
for i in dirty_windows:
    y.remove(i+1)
for i in y:
    if i in dirty_windows:
        print(i)

