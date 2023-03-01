import copy
import numpy as np


class State:
    def __init__(
        self, x_position: float, y_position: float, angle: float, angular_rate: float, speed: float
    ):
        self.x_position = x_position
        self.y_position = y_position
        self.angle = angle
        self.angular_rate = angular_rate
        self.speed = speed

    def __repr__(self):
        return "X Position:\t{x_position}\nY Position:\t{y_position}\nAngle:\t\t{angle}\nAngular Rate:\t{angular_rate}\nSpeed:\t\t{speed}".format(
            x_position=self.x_position, y_position=self.y_position, angle=self.angle, angular_rate=self.angular_rate, speed=self.speed
        )

    def __add__(self, rhs):
        return State(
            self.x_position + rhs.x_position,
            self.y_position + rhs.y_position,
            self.angle + rhs.angle,
            self.angular_rate + rhs.angular_rate,
            self.speed + rhs.speed
        )

    def __sub__(self, rhs):
        return State(
            self.x_position - rhs.x_position,
            self.y_position - rhs.y_position,
            self.angle - rhs.angle,
            self.angular_rate - rhs.angular_rate,
            self.speed - rhs.speed
        )

    def get_list(self):
        return [self.x_position, self.y_position, self.angle, self.angular_rate, self.speed]

    def get_vector(self):
        return np.array([[self.x_position], [self.y_position], [self.angle], [self.angular_rate], [self.speed]])

    @staticmethod
    def create_from_array(array):
        array_copy = _process_array(copy.deepcopy(array), 5)
        return State(array_copy[0], array_copy[1], array_copy[2], array_copy[3], array_copy[4])


class Input:
    def __init__(self, angular_acceleration, acceleration):
        self.angular_acceleration = angular_acceleration
        self.acceleration = acceleration

    def __repr__(self):
        return "Angular Accleration:\t{angular_acceleration}\nAcceleration:\t\t{acceleration}".format(
            angular_acceleration=self.angular_acceleration, acceleration=self.acceleration
        )

    def get_list(self):
        return [self.angular_acceleration, self.acceleration]

    def get_vector(self):
        return np.array([[self.angular_acceleration], [self.acceleration]])

    @staticmethod
    def create_from_array(array):
        array_copy = _process_array(copy.deepcopy(array), 2)
        return Input(array_copy[0], array_copy[1])


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