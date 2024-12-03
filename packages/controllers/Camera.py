from packages.controllers.Controls import Controls
from packages.controllers.Settings import *
from pyrr import Matrix44, Vector3
import numpy as np
import glfw

class Camera:
    def __init__(self, width, height, window, player):
        self.width = width
        self.height = height
        self.window = window
        self.controls = Controls(self.window)

        self.pos = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        self.player = player
        self.follow = False

        self.yaw = -90.0  # Initialize yaw so that front is initially -z
        self.pitch = 0.0
        self.speed = speed
        self.rotation_speed = 40

        self.mouse_sensitivity = mouse_sensitivity

    def update(self, dt):
        if glfw.get_key(self.window, keys["FORWARDS"]) == glfw.PRESS:
            self.pos += self.speed * self.front * dt
        if glfw.get_key(self.window, keys["BACKWARDS"]) == glfw.PRESS:
            self.pos -= self.speed * self.front * dt
        if glfw.get_key(self.window, keys["LEFT"]) == glfw.PRESS:
            self.pos -= np.cross(self.front, self.up) * self.speed * dt
        if glfw.get_key(self.window, keys["RIGHT"]) == glfw.PRESS:
            self.pos += np.cross(self.front, self.up) * self.speed * dt

        if glfw.get_key(self.window, glfw.KEY_F1) == glfw.PRESS:
            print("Toggled Camera Follow")
            self.follow = not self.follow

        if self.follow:
            self.player.update_pos(self.pos)
            # self.pos = np.array([self.player.pos[0], self.player.pos[1], self.player.pos[2]], dtype=np.float32)

        # Rotate camera with mouse
        mouse_pos_x, mouse_pos_y = self.controls.get_mouse_position()
        center_x, center_y = self.width / 2, self.height / 2

        # Calculate mouse offsets
        offset_x = mouse_pos_x - center_x
        offset_y = mouse_pos_y - center_y

        # Apply mouse sensitivity
        self.yaw += offset_x * self.mouse_sensitivity
        self.pitch -= offset_y * self.mouse_sensitivity

        # Clamp the pitch
        self.pitch = max(-89.0, min(89.0, self.pitch))

        # Update front vector
        front = Vector3([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.front = front.normalized

        # Reset mouse position to center
        self.controls.set_mouse_position(center_x, center_y)

        return Matrix44.look_at(
            self.pos,
            self.pos + self.front,
            self.up
        )
