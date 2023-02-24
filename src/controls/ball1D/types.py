import copy
import numpy as np


class State:
    def __init__(self, _position: float, _velocity: float):
        self.position = _position
        self.velocity = _velocity

    def __repr__(self):
        return "Position:\t{position}\nVelocity:\t{velocity}".format(
            position=self.position, velocity=self.velocity
        )

    def __add__(self, rhs):
        return State(self.position + rhs.position, self.velocity + rhs.velocity)

    def __sub__(self, rhs):
        return State(self.position - rhs.position, self.velocity - rhs.velocity)

    def get_list(self):
        return [self.position, self.velocity]

    def get_vector(self):
        return np.array([[self.position], [self.velocity]])

    @staticmethod
    def create_from_array(array):
        array_copy = _process_array(copy.deepcopy(array), 2)
        return State(array_copy[0], array_copy[1])


class Input:
    def __init__(self, _force):
        self.force = _force

    def get_list(self):
        return [self.force]

    def get_vector(self):
        return np.array([[self.force]])

    @staticmethod
    def create_from_array(array):
        array_copy = _process_array(copy.deepcopy(array), 1)
        return Input(array_copy[0])


def _process_array(array, array_size):
    if isinstance(array, np.ndarray):
        array = np.reshape(array, -1).tolist()

    if len(array) != array_size:
        raise ValueError(
            "The provided array has length: {length}. The array must be of length 1 (one value for each input).".format(
                length=len(array)
            )
        )

    if not all([isinstance(x, float) for x in array]):
        raise ValueError(
            "All values in the array must be of type double".format(length=len(array))
        )

    return array
