#!/usr/bin/env python

from matplotlib import pyplot as plt
import numpy as np
import scipy as sp

def main():
    print("Hello World!")

    x = np.array([1, 2, 3])
    plt.plot(x, x)
    plt.show()
    
    y = sp.fft.fft(x)


if __name__ == "__main__":
    main()
