import math

import numpy as np
import scipy as sp

from controls.unicycle.types import Input, State

class Plant:
    def __init__(self, _state):
        self.state = _state

    def cycle(self, t: float, u: Input) -> State:
        self.update(t, u)
        return self.read()
    
    def update(self, t: float, u: Input):
        self.state = self.simulate(t, self.state, u)

    def read(self) -> State:
        return self.state

    def simulate(self, t, x_0, u):
        solution = sp.integrate.solve_ivp(
            self.dynamics,
            (0, t),
            x_0.get_list(),
            args=(u,)
        )

        return State.create_from_array(solution.y[:,-1])
    
    @staticmethod
    def dynamics(t, x, u: Input) -> np.ndarray:
        x_dot = [0.0] * 5

        x_dot[0] = x[4] * math.cos(x[2])
        x_dot[1] = x[4] * math.sin(x[2])
        x_dot[2] = x[3]
        x_dot[3] = u.angular_acceleration
        x_dot[4] = u.acceleration

        return x_dot
