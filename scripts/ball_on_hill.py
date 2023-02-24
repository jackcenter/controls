#!/usr/bin/env python
from typing import Tuple

from matplotlib import pyplot as plt
import numpy as np
import scipy as sp

from controls.state_space import StateSpace
from controls.ball1D.plant import Plant
from controls.ball1D.types import Input, State


def main():
    mass = 1.0
    b = 0.5
    A = np.array([[0.0, 1.0], [0.0, -(b / mass)]])
    B = np.array([[0.0], [1.0 / mass]])
    plant_ss = StateSpace(A, B)
    print(sp.signal.place_poles(A, B, np.array([-0.5, -1.0])).gain_matrix)

    initial_gains = sp.signal.place_poles(A, B, np.array([-0.5, -1.0])).gain_matrix
    print(initial_gains)

    mass = 1.0
    b = 0.0
    A = np.array([[0.0, 1.0], [0.0, -(b / mass)]])
    B = np.array([[0.0], [1.0 / mass]])
    model_ss = StateSpace(A, B)

    x_ref = State(1.0, 0.0)
    x = State(0.0, 1.0)
    u = Input(0.0)
    plant = Plant(plant_ss, x)
    model = Plant(model_ss, x)
    t_step = 0.1
    t_sim = 10

    t = 0.0
    t_history = [t]
    x_history = [x]
    u_history = [u]

    model_error_history = [x]

    for _ in range(0, int(t_sim / t_step)):
        t += t_step
        u = controller(x_ref, x, initial_gains)
        x = plant.cycle(t_step, u)

        t_history.append(t)
        x_history.append(x)
        u_history.append(u)

    _, axs = plt.subplots(4, 1, sharex=True)
    axs[0].plot(t_history, [x.position for x in x_history], ls='--')
    axs[1].plot(t_history, [x.velocity for x in x_history], ls='--')
    axs[2].plot(t_history, [u.force for u in u_history], ls='--')


    x_ref = State(1.0, 0.0)
    x = State(0.0, 1.0)
    u = Input(0.0)
    plant = Plant(plant_ss, x)
    model = Plant(model_ss, x)
    t_step = 0.1
    t_sim = 10

    t = 0.0
    t_history = [t]
    x_history = [x]
    u_history = [u]
    gains = np.array([[0.0, 0.0]])
    for _ in range(0, int(t_sim / t_step)):
        t += t_step
        u = controller(x_ref, x, gains)
        x_model = model.simulate(t_step, x, u)
        x = plant.cycle(t_step, u)

        model_error = x - x_model
        gains = adaptation_law(model_error, x, gains)

        t_history.append(t)
        x_history.append(x)
        u_history.append(u)

        model_error_history.append(model_error)

    print(gains)
    axs[0].plot(t_history, [x.position for x in x_history])
    axs[0].set_ylabel('Position')
    axs[0].minorticks_on()
    axs[0].grid(visible=True, which='both')

    axs[1].plot(t_history, [x.velocity for x in x_history])
    axs[1].set_ylabel('Velocity')
    axs[1].minorticks_on()
    axs[1].grid(visible=True, which='both')

    axs[2].plot(t_history, [u.force for u in u_history])
    axs[2].set_ylabel('Input')
    axs[2].minorticks_on()
    axs[2].grid(visible=True, which='both')

    axs[3].plot(t_history, [x.position for x in model_error_history])
    axs[3].plot(t_history, [x.velocity for x in model_error_history])
    axs[3].set_ylabel('Model Error')
    axs[3].minorticks_on()
    axs[3].grid(visible=True, which='both')

    axs[-1].set_xlabel('Time [s]')
    
    plt.show()


def controller(x_ref: State, x: State, k) -> Input:
    error = x_ref.get_vector() - x.get_vector()
    return Input.create_from_array(k @ error)


def adaptation_law(e, y, gains):
    gamma = 8
    gain_change = -1 * gamma * (e.get_vector().T @ y.get_vector())
    return gains + gain_change


def model(t, u):
    pass


if __name__ == "__main__":
    main()
