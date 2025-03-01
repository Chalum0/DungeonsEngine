from packages.environment.cameras.CameraSettings import *
import numpy as np


class Camera:
    def __init__(self, name_camera, pos_camera):
        self._name = name_camera
        self._pos = np.array(pos_camera, dtype=np.float32)

        self._front = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self._up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        self._yaw = default_yaw
        self._pitch = default_pitch
        self._speed = default_speed
        self._rotation_speed = default_rotation_speed

        self._mouse_sensitivity = default_mouse_sensitivity

    def _set_pos(self, pos):
        self._pos = np.array(pos, dtype=np.float32)

    def on_scroll(self, xoffset, yoffset):
        pass
