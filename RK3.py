import numpy as np
import pandas as pd


# Variant 2
# RK coeffs with padding zeros
a = [[0, 0, 0, 0],
     [0, 1/3, 0, 0],
     [0, 0, 2/3, 0],
     [0, 0, 0, 0]]
c = [0, 0, 1/3, 2/3]
b = [0, 1/4, 0, 3/4]

a = np.array(a)
b = np.array(b)
c = np.array(c)

def f(x, y):
    return (1 - x * y * y) / (x * x * y - 1)

def ff(i, h):
    def F(x, y):
        X = x + c[i] * h
        Y = y
        for j in range(1, i):
            Y += h * a[i][j] * ff(j, h)(x, y)
        return f(x, y)
    return F

def RK(x0, y0, n, x_L, x_R):
    x = [x0]
    y = [y0]
    h = (x_R - x_L)/n
    for i in range(n+1):
        if (i != 0):
            x.append(x[0] + i*h)
        yi = y[i] + h / 4 * (ff(1, h)(x[i], y[i]) + 3 * ff(3, h)(x[i], y[i]))
        y.append(yi)
    return x, y

x1, y1 = RK(0, 0, 20, 0, 1) # x в отрезке (0, 1), количество точек 20, y(0) = 0
for i in range(20):
    x1[i] = round(x1[i], 4)
    y1[i] = round(y1[i], 4)
data1 = pd.DataFrame((x1, y1), index=['x1', 'y1']).dropna(axis=1)
print(data1)

x2, y2 = RK(0, 0, 10, 0, 1) # x в отрезке (0, 1), количество точек 10, y(0) = 0
for i in range(10):
    x2[i] = round(x2[i], 4)
    y2[i] = round(y2[i], 4)
data2 = pd.DataFrame((x2, y2), index=['x2', 'y2']).dropna(axis=1)
print(data2)

def error(rk1, rk2):
    x1, y1 = rk1
    x2, y2 = rk2
    error = []
    for i in range(len(x1)):
        for j in range(len(x2)):
            if(x1[i] == x2[j]):
                error.append(abs(y1[i] - y2[j]))
    return max(np.array(error))

rk0 = RK(0, 0, 300, 0, 1)
for i in range(1, 6):
    print("Error between 300 and %i points:" % (300 - 5 * i), round(error(rk0, RK(0, 0, 300 - 5 * i, 0, 1)), 7))
