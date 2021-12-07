import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time
import copy
import sys
import argparse
import random

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-n', '--n', default=10)
    parser.add_argument ('-q', '--q', default=2)
    parser.add_argument ('-w', '--w', default=5)
    parser.add_argument ('-m', '--mode', default="inside")
 
    return parser

def det(u, v):
  return (u[0]*v[1] - u[1]*v[0])

def cart_to_pol(x, y, x_c = 0, y_c = 0, deg = False):
    complex_format = x - x_c + 1j * (y - y_c)
    return [np.abs(complex_format), np.angle(complex_format, deg = deg)]

def polar_to_cart(r, theta):
    x = r  * np.cos(theta)
    y = r  * np.sin(theta)
    return [x, y]

def sort(a):
    n = len(a)
    b = []
    res = []
    for i in range(n):
        b.append(cart_to_pol(a[i][0], a[i][1]))
    for i in range(n - 1):
        for j in range(n - i - 1):
            if b[j][1] > b[j + 1][1]:
                b[j], b[j + 1] = b[j + 1], b[j]
            elif  (b[j][1] == b[j + 1][1]) & (b[j][0] >= b[j + 1][0]):
                b[j], b[j + 1] = b[j + 1], b[j]
    for i in range(n):
        res.append(polar_to_cart(b[i][0], b[i][1]))
    return res

def heapify(arr, n, i):
    largest = i
    son1_idx = 3*i + 1
    son2_idx = 3*i + 2
    son3_idx = 3*i + 3
    if (son1_idx < n):
        largest_pol = cart_to_pol(arr[largest][0], arr[largest][1])
        son1_pol = cart_to_pol(arr[son1_idx][0], arr[son1_idx][1])
        if ((son1_pol[1] > largest_pol[1]) | ((son1_pol[1] == largest_pol[1]) & (son1_pol[0] >= largest_pol[0]))):
            largest = son1_idx

    if (son2_idx < n):
        if (largest != i):
            largest_pol = cart_to_pol(arr[largest][0], arr[largest][1])
        son2_pol = cart_to_pol(arr[son2_idx][0], arr[son2_idx][1])
        if ((son2_pol[1] > largest_pol[1]) | ((son2_pol[1] == largest_pol[1]) & (son2_pol[0] >= largest_pol[0]))):
            largest = son2_idx
    
    if (son3_idx < n):
        if (largest != i):
            largest_pol = cart_to_pol(arr[largest][0], arr[largest][1])
        son3_pol = cart_to_pol(arr[son3_idx][0], arr[son3_idx][1])
        if ((son3_pol[1] > largest_pol[1]) | ((son3_pol[1] == largest_pol[1]) & (son3_pol[0] >= largest_pol[0]))):
            largest = son3_idx

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def HeapSort(arr):
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, n, i)
    for i in range(n -1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def Merge(arr, i, m, j):
    b = []
    i1 = i
    i2 = m + 1
    while(i1+i2 < j+m+2):
        if (i1 <= m) & (i2 < (j+1)):
            a_i1_pol = cart_to_pol(arr[i1][0], arr[i1][1])
            a_i2_pol = cart_to_pol(arr[i2][0], arr[i2][1])
        if(((i1 <= m) & (i2 < (j+1)) & ((a_i1_pol[1] < a_i2_pol[1]) | ((a_i1_pol[1] == a_i2_pol[1]) & (a_i1_pol[0] <= a_i2_pol[0])))) | (i2 == (j + 1))):
            b.append(arr[i1])
            i1 = i1+1
        else:
            b.append(arr[i2])
            i2 = i2+1
   
    arr[i:j+1] = b

def MergeSort(arr, i, j):
    if (j - i + 1 < 5):
        arr[i:j+1] = sort(arr[i:j+1])
    else:
        step = (j - i + 1) // 5
        for numb in range(5):
            if numb < 4:
                MergeSort(arr, i+step*numb, i+step*(numb+1)-1)
            else:
                MergeSort(arr, i+4*step, j)
        for numb in range(4):
            if numb < 3:
                Merge(arr, i, i+step*(numb+1) - 1, i+step*(numb+2)-1)
            else:
                Merge(arr, i, i+4*step-1, j)

def draw_stack(x, y, center, stack):
    #time.sleep(0.5)
    plt.clf()
    plt.scatter(x, y, s=10, c='blue') 
    plt.scatter(center[0], center[1], s=25, c='red')
    plt.plot([x[0]+center[0] for x in stack],
        [x[1]+center[1] for x in stack],
        linewidth=2.0) 
    plt.axis([min(x) - 1.0, max(x) + 1.0, min(y) - 1.0, max(y) + 1.0])
    plt.draw()
    plt.gcf().canvas.flush_events()



if __name__ == '__main__':
    start_time = datetime.now()
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    plt.ion()

    n = int(namespace.n)
    x = []
    y = []
    q = float(namespace.q)
    w = float(namespace.w)
    mode = namespace.mode

    if (mode == "inside"):
        for i in range(n):
            x.append(random.uniform(0.0, w))
            y.append(random.uniform(0.0, q))
    else:
        for i in range(int(n/2)):
            x.append(random.choice([0.0, w]))
            y.append(random.uniform(0.0, q))
        for i in range(int(n/2), n):
            x.append(random.uniform(0.0, w))
            y.append(random.choice([0.0, q]))

    a = []
    for i in range(n):
        row = []
        row.append(x[i])
        row.append(y[i])
        a.append(row)

    center = copy.deepcopy(a[0])
    m = 0
    for i in range(n):
        if a[i][0] < center[0]:
            center = copy.deepcopy(a[i])
            m = i
        elif a[i][0] == center[0]:
            if a[i][1] < center[1]:
                center = copy.deepcopy(a[i])
                m = i

    plt.clf()
    plt.scatter(x, y, s=10, c='blue') 
    plt.scatter(center[0], center[1], s=25, c='red')
    plt.axis([min(x) - 1.0, max(x) + 1.0, min(y) - 1.0, max(y) + 1.0])
    plt.draw()
    plt.gcf().canvas.flush_events()

    if (n > 1):
        a[0], a[m] = a[m], a[0]
        m = 0
        
        for i in range(n):
            a[i][0] = a[i][0] - center[0]
            a[i][1] = a[i][1] - center[1]

        new_a = a[1:]
        new_a = sort(new_a)

        a = a[1:]
        #MergeSort(a, 0, n-2)
        HeapSort(a)
        
        stack = []
        stack.append([0, 0])
        stack.append(a[0])
        draw_stack(x, y, center, stack)
        for i in range(1, n - 1):
            top = stack.pop()
            next_to_top = stack.pop()
            stack.append(next_to_top)
            stack.append(top)
            while((len(stack) >= 1) & (det([top[0] - next_to_top[0], top[1] - next_to_top[1]], [a[i][0] - top[0], a[i][1] - top[1]]) < 0)):
                stack.pop()
                if (len(stack) >= 2):
                    top = stack.pop()
                    next_to_top = stack.pop()
                    stack.append(next_to_top)
                    stack.append(top)
            stack.append(a[i])
            draw_stack(x, y, center, stack)
        
        stack.append([0, 0])
        draw_stack(x, y, center, stack)

        print(datetime.now() - start_time)
        plt.ioff()
        plt.show()

    else:
        print(datetime.now() - start_time)