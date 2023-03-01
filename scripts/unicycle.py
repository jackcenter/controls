#!/usr/bin/env python
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import scipy as sp
from scipy.optimize import Bounds, minimize

from controls.unicycle.types import Input, State
from controls.unicycle.plant import Plant

def main():
    t_sim = 15.0
    t_step = 0.1

    t = 0.0
    x = State(0.0, 0.0, 0.0, 1.0, 1.0)
    u = Input(0.0, 0.0)

    plant = Plant(x)

    t_history = [t]
    x_history = [x]
    u_history = [u]

    

    for _ in range(0, int(t_sim / t_step)):
        t += t_step

        bounds = Bounds(-np.inf, -x.angular_rate / 2)
        k = get_curvature(x)
        res = minimize(cost_function, np.array([k]), args=k, bounds=bounds)

        u = Input(res.x[0], 0.0)
        x = plant.cycle(t_step, u)

        t_history.append(t)
        x_history.append(x)
        u_history.append(u)

        print(k)
        print(res.x[0])
        print()

    # _, axs = plt.subplots(5, 1, sharex=True)
    # axs[0].plot(t_history, [x.x_position for x in x_history])
    # axs[1].plot(t_history, [x.y_position for x in x_history])
    # axs[2].plot(t_history, [x.angle for x in x_history])
    # axs[3].plot(t_history, [x.angular_rate for x in x_history])
    # axs[4].plot(t_history, [x.speed for x in x_history])
    # plt.show()

    x = np.arange(10)
    y = np.random.random(10)

    fig = plt.figure()
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.grid()
    graph, = plt.plot([], [], 'o')

    def animate(i):
        graph.set_data(x_history[i+1].x_position, x_history[i+1].y_position)
        return graph

    _ = FuncAnimation(fig, animate, frames=150, interval=100)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.show()


def get_curvature(x: State) -> float:
    return x.angular_rate / x.speed


def cost_function(u: float, x: float) -> float:
    return u**2


def controller(x_hat: State):
    k_hat = (-x_hat.speed /2) * (x_hat.angular_rate / x_hat.speed)


if __name__ == "__main__":
    main()
