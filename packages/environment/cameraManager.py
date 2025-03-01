from packages.environment.cameras import TPSCamera

import glfw

class CameraManager:

    TPS_CAMERA = "CAMERA-MANAGER-TPS-CAMERA"

    def __init__(self):
        self._camera = None
        self._cameras = []

    def _set_camera(self, camera):
        self._camera = camera
        glfw.set_scroll_callback(self.window, self._camera.on_scroll)

    def _create_tps_camera(self, name, pos, entity):
        new_camera = TPSCamera.TPSCamera(name, pos, entity)
        self._cameras.append(new_camera)
        return new_camera

    def create_camera(self, camera_type, name, pos, entity=None):
        if camera_type == self.TPS_CAMERA:
            return self._create_tps_camera(name, pos, entity)

