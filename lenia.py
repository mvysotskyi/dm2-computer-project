"""
Lenia modele.
"""

import numpy as np
from scipy.signal import convolve2d
from scipy import ndimage

class Lenia:
    """
    Lenia model.
    """
    patterns = {
        "orbium": {"name":"Orbium","R":13,"T":10,"m":0.15,"s":0.015,"b":[1],
        "cells":[[0,0,0,0,0,0,0.1,0.14,0.1,0,0,0.03,0.03,0,0,0.3,0,0,0,0], [0,0,0,0,0,0.08,0.24,0.3,0.3,0.18,0.14,0.15,0.16,0.15,0.09,0.2,0,0,0,0], [0,0,0,0,0,0.15,0.34,0.44,0.46,0.38,0.18,0.14,0.11,0.13,0.19,0.18,0.45,0,0,0], [0,0,0,0,0.06,0.13,0.39,0.5,0.5,0.37,0.06,0,0,0,0.02,0.16,0.68,0,0,0], [0,0,0,0.11,0.17,0.17,0.33,0.4,0.38,0.28,0.14,0,0,0,0,0,0.18,0.42,0,0], [0,0,0.09,0.18,0.13,0.06,0.08,0.26,0.32,0.32,0.27,0,0,0,0,0,0,0.82,0,0], [0.27,0,0.16,0.12,0,0,0,0.25,0.38,0.44,0.45,0.34,0,0,0,0,0,0.22,0.17,0], [0,0.07,0.2,0.02,0,0,0,0.31,0.48,0.57,0.6,0.57,0,0,0,0,0,0,0.49,0], [0,0.59,0.19,0,0,0,0,0.2,0.57,0.69,0.76,0.76,0.49,0,0,0,0,0,0.36,0], [0,0.58,0.19,0,0,0,0,0,0.67,0.83,0.9,0.92,0.87,0.12,0,0,0,0,0.22,0.07], [0,0,0.46,0,0,0,0,0,0.7,0.93,1,1,1,0.61,0,0,0,0,0.18,0.11], [0,0,0.82,0,0,0,0,0,0.47,1,1,0.98,1,0.96,0.27,0,0,0,0.19,0.1], [0,0,0.46,0,0,0,0,0,0.25,1,1,0.84,0.92,0.97,0.54,0.14,0.04,0.1,0.21,0.05], [0,0,0,0.4,0,0,0,0,0.09,0.8,1,0.82,0.8,0.85,0.63,0.31,0.18,0.19,0.2,0.01], [0,0,0,0.36,0.1,0,0,0,0.05,0.54,0.86,0.79,0.74,0.72,0.6,0.39,0.28,0.24,0.13,0], [0,0,0,0.01,0.3,0.07,0,0,0.08,0.36,0.64,0.7,0.64,0.6,0.51,0.39,0.29,0.19,0.04,0], [0,0,0,0,0.1,0.24,0.14,0.1,0.15,0.29,0.45,0.53,0.52,0.46,0.4,0.31,0.21,0.08,0,0], [0,0,0,0,0,0.08,0.21,0.21,0.22,0.29,0.36,0.39,0.37,0.33,0.26,0.18,0.09,0,0,0], [0,0,0,0,0,0,0.03,0.13,0.19,0.22,0.24,0.24,0.23,0.18,0.13,0.05,0,0,0,0], [0,0,0,0,0,0,0,0,0.02,0.06,0.08,0.09,0.07,0.05,0.01,0,0,0,0,0]]
        }
    }

    def __init__(self, pattern="orbium", size=64, scale=1, cx=20, cy=20):
        self.pattern = self.patterns[pattern]
        self.size = size
        self.scale = scale
        self.cx = cx
        self.cy = cy

        self.world = np.zeros((size, size))
        self.__init_pattern()

        self.kernel = self.__smooth_ring_kernel(self.pattern["R"])
        self.period = self.pattern["T"]

    def __init_pattern(self):
        cells = self.pattern["cells"]
        cells = ndimage.zoom(cells, self.scale, order=0)
        self.world[self.cx:self.cx+cells.shape[0], self.cy:self.cy+cells.shape[1]] = cells

        cells = self.pattern["cells"]
        cells = ndimage.zoom(cells, self.scale, order=0)
        self.cx = self.size // 2 - cells.shape[0] // 2
        self.cy = self.size // 2 - cells.shape[1] // 2

        self.world[self.cx:self.cx+cells.shape[0], self.cy:self.cy+cells.shape[1]] = cells

    def __bell_function(self, x, m, s):
        return np.exp(-((x-m)/s)**2 / 2)

    def __smooth_ring_kernel(self, radius):
        X, Y = np.ogrid[-radius:radius, -radius:radius]
        # Increase X  and Y by 1 to avoid division by zero
        X += 1;  Y += 1

        D = np.sqrt(X**2 + Y**2) / radius
        K = (D < 1) * self.__bell_function(D, 0.5, 0.15)
        K = K / np.sum(K)
        return K

    def __growth(self, U):
        m, s = self.pattern["m"], self.pattern["s"]
        return self.__bell_function(U, m, s) * 2 - 1

    def __update(self):
        convoluted = convolve2d(self.world, self.kernel, mode='same', boundary='wrap')
        self.world = np.clip(self.world + 1 / self.period * self.__growth(convoluted), 0, 1)

    def next(self):
        """
        Update the world and return it.
        """
        self.__update()
        return self.world
