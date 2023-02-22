
import numpy as np
import scipy as sp

from controls.ball1D.types import Input, State

class Plant:
    A = np.array([
            [0.0, 1.0],
            [0.0, -0.5]
        ])

    B = np.array([
            [0.0],
            [1.0]
        ])

    def __init__(self, _state: State):
        self.state = _state

    def cycle(self, t: float, u: Input) -> State:
        self.update(t, u)
        return self.read()

    def update(self, t: float, u: Input):
        solution = sp.integrate.solve_ivp(self.dynamics, (0, t), self.state.get_list(), args=(u,), vectorized=True)
        self.state = State.create_from_array(solution.y[:,-1])

    def read(self) -> State:
        return self.state

    @staticmethod
    def dynamics(t, x, u) -> np.ndarray:
        return Plant.A @ x.reshape((-1, 1)) + Plant.B @ u.get_vector()
