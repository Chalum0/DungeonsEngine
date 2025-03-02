from packages.environment.cameras.CameraSettings import *
from packages.environment.cameras.Camera import Camera
from packages.environment.Cursor import Cursor
from packages.entities.Entity import Entity

from typing import override
from pyrr import Matrix44
import numpy as np

class TPSCamera(Camera):
    def __init__(self, name_camera, pos_camera, entity: Entity):
        Camera.__init__(self, name_camera, pos_camera)
        self._entity = entity
        self._current_distance_from_target = default_current_distance_from_target
        self._min_distance_from_target = default_min_distance_from_target
        self._max_distance_from_target = default_max_distance_from_target
        if self._entity is None:
            raise NoEntitySet()


    def update(self, delta_time, width, height, cursor: Cursor):
        mouse_pos_x, mouse_pos_y = cursor.get_position()
        center_x, center_y = width / 2, height / 2
        offset_x = mouse_pos_x - center_x
        offset_y = mouse_pos_y - center_y

        if cursor.get_pressed()[2]:
            self._pitch += offset_y * self._mouse_sensitivity
            self._yaw += offset_x * self._mouse_sensitivity

            # Clamp pitch to avoid flipping the camera upside down
            self._pitch = max(-89.0, min(89.0, self._pitch))

        # re-center the mouse
        cursor.set_position(center_x, center_y)

        # Adjust if your player's pivot is really at the feet
        # Suppose you want the midpoint around y=1.5
        target = np.array(self._entity.get_pos()) + np.array([0.0, 0.5, 0.0], dtype=np.float32)

        # Spherical coords
        rad_yaw = np.radians(self._yaw)
        rad_pitch = np.radians(self._pitch)
        horizontal_dist = self._current_distance_from_target * np.cos(rad_pitch)
        vertical_dist = self._current_distance_from_target * np.sin(rad_pitch)

        offset_x = horizontal_dist * np.sin(-rad_yaw)
        offset_z = horizontal_dist * np.cos(-rad_yaw)

        camera_x = target[0] + offset_x
        camera_y = target[1] + vertical_dist
        camera_z = target[2] + offset_z
        self._pos = np.array([camera_x, camera_y, camera_z], dtype=np.float32)

        return Matrix44.look_at(self._pos, target, self._up)

    @override
    def on_scroll(self, xoffset, yoffset: float):
        self._current_distance_from_target -= yoffset  # can add multiplier if desired
        if self._current_distance_from_target < self._min_distance_from_target:
            self._current_distance_from_target = self._min_distance_from_target
        if self._current_distance_from_target > self._max_distance_from_target:
            self._current_distance_from_target = self._max_distance_from_target


    # GETTERS AND SETTERS
    def _set_current_distance_from_target(self, distance=default_current_distance_from_target):
        self._current_distance_from_target = distance
    def _reset_current_distance_from_target(self):
        self._current_distance_from_target = default_current_distance_from_target

    def _set_min_distance_from_target(self, distance=default_min_distance_from_target):
        self._min_distance_from_target = distance
    def _reset_min_distance_fro_target(self):
        self._min_distance_from_target = default_min_distance_from_target

    def _set_max_distance_from_target(self, distance=default_max_distance_from_target):
        self._max_distance_from_target = distance
    def _reset_max_distance_from_target(self):
        self._max_distance_from_target = default_max_distance_from_target

    def _set_entity(self, entity: Entity):
        self._entity = entity

class NoEntitySet(Exception):
    def __init__(self):
        super().__init__(
            f'No entity has been set to follow.'
        )
