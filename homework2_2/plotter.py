import matplotlib.pyplot as plt
import numpy as np
import math 

def f(s,b,r):
    """
    this function is f(s) = 1 - 1(1 - s^r)^b
    """
    return 1 - np.power(1 - np.power(s, r), b) 

def plot_s_curve(b,r):
    t = np.arange(0.0, 1.0, 0.01)
    s = f(t,10,10)
    fig, ax = plt.subplots()
    ax.plot(t,s)
    ax.set(xlabel='Jaccard similarity of documents', ylabel='Probability of becoming a candidate', title='S-curve')

    ax.grid()

    plt.show()


