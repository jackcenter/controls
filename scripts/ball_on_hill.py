#!/usr/bin/env python
from typing import Tuple

from matplotlib import pyplot as plt
import numpy as np
import scipy as sp

from controls.ball1D.plant import Plant
from controls.ball1D.types import Input, State

def main():

    # sp.linalg.eig(Plant.A)
    print(sp.signal.place_poles(Plant.A, Plant.B, np.array([-2.5, -4.0])).gain_matrix)

    x_ref = State(1.0, 0.0)
    x = State(0.0, 1.0)
    u = Input(0.0)
    plant = Plant(x)
    t_step = 0.1
    t_sim = 30

    t = 0.0
    t_history = [t]
    x_history = [x]
    u_history = [u]

    for _ in range(0, int(t_sim / t_step)):
        t += t_step 
        u = controller(x_ref, x)
        x = plant.cycle(t_step, u)
 
        t_history.append(t)
        x_history.append(x)
        u_history.append(u)

    _, axs = plt.subplots(2)
    axs[0].plot(t_history, [x.position for x in x_history])
    axs[0].plot(t_history, [x.velocity for x in x_history])
    axs[1].plot(t_history, [u.force for u in u_history])
    plt.show()


def controller(x_ref: State, x: State) -> Input:
    error = x_ref.get_vector() - x.get_vector()
    k = np.array([
        [0.5, 1.0]
    ])

    return Input.create_from_array(k @ error)


if __name__ == '__main__':
    main()