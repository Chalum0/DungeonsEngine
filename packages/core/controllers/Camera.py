from packages.core.controllers import CameraControls
from packages.core.controllers.Settings import *
from pyrr import Matrix44, Vector3
import numpy as np
import glfw

class Camera:
    def __init__(self, width, height, window, player):
        self.width = width
        self.height = height
        self.window = window
        self.controls = CameraControls.Controls(self.window)

        self.pos = np.array([-1.83, 7.42, 6.61], dtype=np.float32)
        self.front = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        self.player = player
        self.free_cam = False

        self.third_person = False  # Toggle if you'd like
        self.distance = 5.0
        self.min_distance = 1.0
        self.max_distance = 20.0

        self.yaw = -77.6  # Initialize yaw so that front is initially -z
        self.pitch = -45.0
        self.speed = speed
        self.rotation_speed = 40

        self.mouse_sensitivity = mouse_sensitivity

        # Vertical "height" offset so the camera aims at the player's head or torso
        self.player_offset = np.array([0.0, 1.5, 0.0], dtype=np.float32)

        # “Up” vector remains the same
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        # If you still want a “pos” for debugging or references
        self.pos = np.array([0.0, 0.0, 0.0], dtype=np.float32)

    def on_scroll(self, yoffset: float):
        """Called from main.py scroll_callback. Zoom in/out by changing self.distance."""
        self.distance -= yoffset  # can add multiplier if desired
        if self.distance < self.min_distance:
            self.distance = self.min_distance
        if self.distance > self.max_distance:
            self.distance = self.max_distance

    def update(self, dt):
        if self.third_person:
            return self._update_third_person(dt)
        else:
            return self._update_free_cam(dt)

    def _update_third_person(self, dt):
        mouse_pos_x, mouse_pos_y = self.controls.get_mouse_position()
        center_x, center_y = self.width / 2, self.height / 2
        offset_x = mouse_pos_x - center_x
        offset_y = mouse_pos_y - center_y

        if glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS:
            self.pitch += offset_y * self.mouse_sensitivity
            self.yaw += offset_x * self.mouse_sensitivity

            # Clamp pitch to avoid flipping the camera upside down
            self.pitch = max(-89.0, min(89.0, self.pitch))

        # re-center the mouse
        self.controls.set_mouse_position(center_x, center_y)

        # Adjust if your player's pivot is really at the feet
        # Suppose you want the midpoint around y=1.5
        target = np.array(self.player.pos) + np.array([0.0, 0.5, 0.0], dtype=np.float32)

        # Spherical coords
        rad_yaw = np.radians(self.yaw)
        rad_pitch = np.radians(self.pitch)
        horizontal_dist = self.distance * np.cos(rad_pitch)
        vertical_dist = self.distance * np.sin(rad_pitch)

        offset_x = horizontal_dist * np.sin(-rad_yaw)
        offset_z = horizontal_dist * np.cos(-rad_yaw)

        camera_x = target[0] + offset_x
        camera_y = target[1] + vertical_dist
        camera_z = target[2] + offset_z
        self.pos = np.array([camera_x, camera_y, camera_z], dtype=np.float32)

        return Matrix44.look_at(self.pos, target, self.up)


    def _update_free_cam(self, dt):
        """Your old free-fly code, used if self.third_person = False."""
        # Example of reusing your existing approach
        mouse_pos_x, mouse_pos_y = self.controls.get_mouse_position()
        center_x, center_y = self.width / 2, self.height / 2
        offset_x = mouse_pos_x - center_x
        offset_y = mouse_pos_y - center_y

        if self.free_cam:
            self.yaw += offset_x * self.mouse_sensitivity
            self.pitch -= offset_y * self.mouse_sensitivity
            self.pitch = max(-89.0, min(89.0, self.pitch))

        # Update front vector
        front = Vector3([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.controls.set_mouse_position(center_x, center_y)
        self.front = front.normalized

        return Matrix44.look_at(
            self.pos,
            self.pos + self.front,
            self.up
        )

    def move_forwards(self, dt):
        if self.free_cam:
            self.pos += self.speed * self.front * dt
        else:
            self.pos = np.array([self.pos[0], self.pos[1], self.pos[2]-self.speed*dt], dtype=np.float32)

    def move_backwards(self, dt):
        if self.free_cam:
            self.pos -= self.speed * self.front * dt
        else:
            self.pos = np.array([self.pos[0], self.pos[1], self.pos[2]+self.speed*dt], dtype=np.float32)

    def move_left(self, dt):
        if self.free_cam:
            self.pos -= np.cross(self.front, self.up) * self.speed * dt
        else:
            self.pos = np.array([self.pos[0]-self.speed*dt, self.pos[1], self.pos[2]], dtype=np.float32)

    def move_right(self, dt):
        if self.free_cam:
            self.pos += np.cross(self.front, self.up) * self.speed * dt
        else:
            self.pos = np.array([self.pos[0]+self.speed*dt, self.pos[1], self.pos[2]], dtype=np.float32)
