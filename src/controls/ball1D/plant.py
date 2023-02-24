import numpy as np
import scipy as sp

from controls.state_space import StateSpace
from controls.ball1D.types import Input, State


class Plant:
    def __init__(self, _state_space, _state: State):
        self.state_space = _state_space
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
            args=(u, self.state_space),
            vectorized=True,
        )

        return State.create_from_array(solution.y[:, -1])

    @staticmethod
    def dynamics(t, x, u: Input, ss: StateSpace) -> np.ndarray:
        return ss.A @ x.reshape((-1, 1)) + ss.B @ u.get_vector()
